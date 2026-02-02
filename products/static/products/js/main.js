function get_new_product_entry(product_image, product_title, product_url, product_price, product_desired_price) {
    var price_color = "black"

    product_price = Number(product_price)
    product_desired_price = Number(product_desired_price).toFixed(2) // allowing only 2 decimal digits
    if (product_price <= product_desired_price) {
        price_color = 'green'
    }

    console.log("product_title:", product_title)
    console.log("product_price:", product_price)

    var maxLength = 40; // gewünschte Zeichen
    var short_url = product_url.length > maxLength ? product_url.slice(0, maxLength) + "..." : product_url;


    var product_tag = `
        <tr style="text-align: center">
            <td>
                <img style='size height:200px; background-color: transparent; width:125px' class="product-img" src=${product_image}>
            </td>
            <td>
                ${product_title}
            </td>
            <td>
                <a href=${product_url} style="word-wrap:break-word;">${short_url}</a>
            </td>
            <td>
                <font face='cursive,serif' style="color:${price_color}" size="8px">${product_price}€</font>
            </td>
            <td>
                <font face='cursive,serif' size="8px">${product_desired_price}€</font>
            </td>
            <td>
                <button type='submit' value='delete' id='delete_btn'>
                    Delete
                </button>
            </td>
        </tr>
    `
    return product_tag
}


$(document).ready(function () {
    // shows website and refresh it every 20 seconds to scrape data
    // send a GET request to build the list of todos
    function refresh() {
        $.ajax({
            type: 'GET',
            url: '/product_list/',
            dataType: 'json',
            success: function (response) {
                $('.product_body').empty();  // remove old products
                if (response['status'] == "data_not_found") {
                    if ($("#product_message").html().trim() === "") {
                        $('#product_message').text("data cannot be updated");
                    }
                } else {
                    // show all products
                    for (var product of response['products']) {
                        console.log("product['url']", product['url'], product['price'])
                        var product_entry = get_new_product_entry(
                            product['image_url'],
                            product['title'],
                            product['url'],
                            product['price'],
                            product['desired_price']);
                        $('.product_body').append(product_entry);
                    }
                }
                setTimeout(refresh, 20000); // refresh website every 20 seconds while runserver is running
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
        $("#product_message").html("Checking url...");

        var amzn_url = $('#amzn_url').val();
        var desired_price = $('#desired_price').val();

        $.ajax({
            url: '/add_product/',
            type: 'POST',
            dataType: 'json',
            data: {
                'amzn_url': amzn_url,
                'desired_price': desired_price
            },
        }).done(function (product) {
            console.log("Product:", product)
            message = ""
            const status = product['status']
            const statusMessages = {
                is_already_in_list: "This product is already in your list.",
                already_under_limit_price:
                    "The price is already below your desired price.",
                only_numbers: "Only valid numbers in price field.",
                empty_url_field: "Url field is empty.",
                not_existing: "Website does not exist.",
            };

            if (product['status'] == 'new_product_created') {
                // check if product contains all attributes (later)
                const np = product['new_product'];
                const new_product = get_new_product_entry(
                    np['image_url'],
                    np['title'],
                    np['url'],
                    np['price'],
                    np['desired_price'])
                console.log("NEW PRODUCT:", new_product)
                $('.product_body').append(new_product)
            } else {
                message = statusMessages[status] || "Unknown error";

                if (status === "already_under_limit_price") {
                    document.getElementById("product_message").style =
                        "font-size: 20px; color:#0000ff;";
                }
            }
            // writes message
            //document.getElementById('product_message').innerHTML = message
            $("#product_message").html(message);
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
