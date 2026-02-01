import re

import requests
from bs4 import BeautifulSoup


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...'
}


def extract_asin(url, html=None):
    """
    Extract ASIN from HTML response.
    :param url: URL to extract.
    :param html: HTML response.
    :return: asin
    """
    match = re.search(r'/dp/([A-Z0-9]{10})', url)
    if not match:
        match = re.search(r'/gp/product/([A-Z0-9]{10})', url)
    asin = match.group(1) if match else None

    if not asin and html:
        soup = BeautifulSoup(html, 'html.parser')
        asin_tag = soup.find('input', {'id': 'ASIN'})
        if asin_tag:
            asin = asin_tag.get('value')
    return asin


def extract_price(soup):
    """
    Extract price from HTML response parser.
    :param soup: HTML response.
    :return: price of the product.
    """
    selectors = [
        '#priceblock_ourprice',  # normaler Preis
        '#priceblock_dealprice',  # Angebotspreis
        '.a-price .a-offscreen',  # neue Layouts
        '.a-price-whole',  # Backup
    ]
    for sel in selectors:
        tag = soup.select_one(sel)
        if tag:
            text = tag.get_text(strip=True)
            # clean text
            text = text.replace('€', '').replace(',', '.')
            try:
                return float(text)
            except ValueError:
                continue
    return None  # Preis nicht gefunden


def scrape_amazon_price_alerter(url):
    """
    Scrape Amazon price from product.
    :param url: URL to scrape.
    :return: dict with product data containing title, price, image_url and asin
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()  # wirft HTTPError bei 4xx/5xx
    except Exception:
        # alles abfangen: Timeout, ConnectionError, HTTPError etc.
        return None

    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.select_one('#productTitle')
    title = title.get_text(strip=True) if title else ""

    price = extract_price(soup)
    if price is None:
        price = 0  # optional: Default

    image_tag = soup.find('img', id='landingImage')
    image_url = image_tag['src'] if image_tag else ""

    asin = extract_asin(url, html)

    return {'asin': asin, 'title': title, 'price': price, 'image_url': image_url}
