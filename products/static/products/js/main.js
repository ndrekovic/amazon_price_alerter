function load() {
    // refresh page every x seconds
    //var refresh_time_seconds = 60;
    //setTimeout("window.open('http://127.0.0.1:' + port.toString(), '_self');", refresh_time_seconds * 1000);
}

function get_new_product_entry(product_image, product_title, product_url, product_price, product_desired_price) {
    var price_color = "black"

    product_price = Number(product_price)
    product_desired_price = Number(product_desired_price).toFixed(2) // allowing only 2 decimal digits
    if (product_price <= product_desired_price) {
        price_color = 'green'
    }

    console.log("product_title:", product_title)

    var product_tag = `
        <tr style="text-align: center">
            <td>
                <img style='size height:200px; width:125px' src=${product_image}>
                <!-- <img src="${product_image}" style="height:200px; width:125px;"> -->

            </td>
            <td>
                ${product_title}
            </td>
            <td>
                <a href=${product_url} style="word-wrap:break-word;">${product_url}</a>
            </td>
            <td>
                <font face='cursive,serif' style="color:${price_color}" size="8px">${product_price}€</font>
            </td>
            <td>
                <font face='cursive,serif' size="8px">${product_desired_price}€</font>
            </td>
            <td>
                <button type='submit' value='delete' id='delete_btn'>
                    Entfernen
                </button>
            </td>
        </tr>
    `
    return product_tag
}


$(document).ready(function () {
    // shows website and refresh it every 20 seconds to scrape data
    function refresh() {
        $.ajax({
            type: 'GET',
            url: '/product_list/',
            dataType: 'json',
            success: function (response) {
                $('.product_body').empty();  // Alte Produkte entfernen
                if (response['status'] == "data_not_found") {
                    $('#product_message').text("Daten konnten nicht geupdatet werden. Bitte erneut versuchen.");
                } else {
                    for (var product of response['products']) {
                        var product_entry = get_new_product_entry(
                            product['image_url'], product['title'], product['url'], product['price'], product['desired_price']);
                        $('.product_body').append(product_entry);
                    }
                }
                setTimeout(refresh, 20000); // in 20 Sekunden erneut
            }
        });
    }

    $(function () {
        refresh();
    });


    // add button event
    $('#add_product_to_list').click(function (e) {
        /* Event after clicking button to add product */
        e.preventDefault();
        var amzn_url = $('#amzn_url').val();
        var desired_price = $('#desired_price').val();

        // send a GET request to build the list of todos
        $.ajax({
            url: '/add_product/',
            type: 'POST',
            dataType: 'json',
            data: {
                'amzn_url': amzn_url,
                'desired_price': desired_price
            },
        }).done(function (product) {
            message = ""

            if (product['status'] == 'new_product_created') {
                // check if product contains all attributes (later)
                const np = product['new_product'];
                new_product = get_new_product_entry(
                    np['image_url'], np['title'], np['url'], np['price'], np['desired_price'])
                // console.log(product['image_url'], product['title'], product['url'], product['price'], product['desired_price'])
                console.log("Product:", np)
                $('.product_body').append(new_product)
            } else {
                if (product['status'] == 'is_already_in_list') {
                    message = "This product is already in your list."
                } else if (product['status'] == "already_under_limit_price") {
                    message = "The price of the product is already below your desired price. Click on the link to buy."
                    document.getElementById('product_message').style = 'font-size: 20px; color:#0000ff;'
                } else if (product['status'] == "only_numbers") {
                    message = 'Only valid numbers in price field.'
                } else if (product['status'] == "empty_url_field") {
                    message = 'Url field is empty.'
                } else if (product['status'] == 'not_existing') {
                    message = 'Website does not exist.'
                }
            }
            // writes message
            document.getElementById('product_message').innerHTML = message
        })
        $('#amzn_url').val('') // reset the input field
        $('#desired_price').val('') // reset the input field
    });

    // delete button event
    $('tbody').on('click', '#delete_btn', function (event) {
        event.stopPropagation()
        var current_product = $(this).parent().parent()
        var current_product_link = current_product.find('a').text() // find unique element which is the url link

        // read csrf token from cookies
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let cookie of cookies) {
                    cookie = cookie.trim();
                    if (cookie.startsWith(name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        const csrftoken = getCookie('csrftoken');

        $.ajax({
            url: "/delete_product/",
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'current_product_link': current_product_link,
            },
        }).done(function (response) {
            if (response['status'] === 'deleted') {
                current_product.remove()
            }
        })
    })
})
