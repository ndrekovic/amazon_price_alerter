import re
from decimal import Decimal, InvalidOperation, ROUND_DOWN

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# import utils
from products.utils import scrape_amazon_price_alerter
from .emails import send_price_alert
from .models import Product


HEADERS = ({
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 44.0.2403.157 Safari / 537.36',
    'Accept': 'text/html',
})
cookies = dict(language='de')

def show_webpage(request):
    """ Renders template which presents the actual website to the user."""
    return render(request, 'products/product_list.html')

@csrf_exempt
def product_list(request):
    """
    Updates product data after each get request.

    :param request: contains data about the current request
    :return: Jsonresponse that returns the generated response
    """
    status = ""
    for product in Product.objects.all().values():
        if not product['mail_has_been_sent']:
            Product.objects.filter(url=product['url']).update(mail_has_been_sent=True)
        Product.objects.filter(url=product['url']).update(price=product['price'])

    products = list(Product.objects.all().values())
    return JsonResponse({'products': products, 'status': status})

def extract_asin(url):
    """
    Extracts the ASIN from the passed url.
    :param url: the passed url
    :return:
    """
    match = re.search(r'/dp/([A-Z0-9]{10})', url)
    if not match:
        match = re.search(r'/gp/product/([A-Z0-9]{10})', url)
    return match.group(1) if match else None

def parse_price(raw_price: str) -> Decimal:
    """
    Cleans and validates a price input.
    Returns Decimal rounded DOWN to 2 decimals or None if invalid.
    """

    if not raw_price:
        return None

    # remove symbols and spaces
    cleaned = (
        raw_price
        .replace('€', '')
        .replace(' ', '')
        .replace(',', '.')
        .strip()
    )

    try:
        value = Decimal(cleaned)

        # negative prices not allowed
        if value < 0:
            return None

        # round DOWN to 2 decimals
        return value.quantize(Decimal("0.01"), rounding=ROUND_DOWN)

    except InvalidOperation:
        return None

def product_exists_already(url):
    """
    Checks if the product already exists in the database.

    :param url: url for the product to be checked.
    :return: True if the product already exists in the database, False otherwise.
    """
    asin = extract_asin(url)
    if not asin:
        return False
    return Product.objects.filter(asin=asin).exists()

def create_new_product(url, desired_price, data):
    """
    Creates a new product and returns a dictionary containing the data.

    :param url: url for the product to be created.
    :param desired_price: desired price for the new product.
    :param data: additional data for the new product including asin and image_url.
    :return: a dictionary containing the product data.
    """
    new_product = Product.objects.create(
        asin=data['asin'],
        url=url,
        desired_price=desired_price,
        title=data['title'],
        price=data['price'],
        image_url=data['image_url'],
    )
    # define new data
    return {
        'asin': new_product.asin,
        'url': new_product.url,
        'desired_price': new_product.desired_price,
        'title': new_product.title,
        'price': new_product.price,
        'image_url': new_product.image_url,
        'mail_has_been_sent': new_product.mail_has_been_sent
    }

@csrf_exempt
def add_prod(request):
    """
    Handles the adding of a product to the list after submitting the 'add' button.

    :param request: containts data about the current request
    :return: Jsonresponse containing information either about the created product data or a report for its non-creation
    """
    if request.method == 'POST':
        url = request.POST.get('amzn_url')
        raw_price = request.POST.get('desired_price')
        desired_price = parse_price(raw_price)

        # validating input price
        if desired_price is None:
            return JsonResponse({'status': 'only_numbers'})

        # validating input url
        if not url:
            return JsonResponse({'status': 'empty_url_field'})

        # extract asin and check if product is already in list
        if product_exists_already(url):
            return JsonResponse({'status': 'is_already_in_list'})

        # scrape data
        data = scrape_amazon_price_alerter(url)
        if not data:
            return JsonResponse({'status': 'not_existing'})

        try:
            # get here only if all conditions for creating an object are met
            new_product_data = create_new_product(url, desired_price, data)
            if new_product_data['price'] <= desired_price:
                send_price_alert(url, round(new_product_data['price'], 2), round(desired_price, 2))
            # update product list once after adding the product
            return JsonResponse({'status': 'new_product_created', 'new_product': new_product_data})
        except Exception:
            return JsonResponse({'status': 'only_numbers'})  # only_numbers

    return show_webpage(request)

@csrf_exempt
def delete_prod(request):
    """
    Handles the deleting process of each product

    :param request: containts data about the current request
    :return: Jsonresponse that returns the generated response for the status update
    """
    if request.method == 'POST':
        url = request.POST.get('current_product_link')
        Product.objects.filter(url=url).delete()
        return JsonResponse({'status': 'deleted'})
