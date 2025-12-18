async function search_products() {
    let search_bar = document.getElementById("search-bar");

    let requestURL = `http://localhost:1234/search/?search_query=${search_bar.value}`;
    let request = new Request(requestURL);

    let response = await fetch(request, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    });

    let products_data = await response.json();

    let products_grid = document.querySelector(".products-grid");

    if (products_data.length !== 0) {
        products_grid.innerHTML = "";

        for (let product of products_data) {
            let product_item = document.createElement("div");
            product_item.className = "product-item";
            product_item.dataset.productId = product.id;

            let product_name = document.createElement("div");
            product_name.className = "product-name";
            product_name.innerHTML = `<p><b>${product.name}</b></p>`;

            product_item.appendChild(product_name);

            let image_container = document.createElement("div");
            image_container.className = "product-image";
            let img = document.createElement("img");
            img.src = product.img_url;
            img.alt = product.name;
            image_container.appendChild(img);

            product_item.appendChild(image_container);

            let buttons_container = document.createElement("div");
            buttons_container.className = "buttons-container";

            let offers_button = document.createElement("button");
            offers_button.className = "offers-button";
            offers_button.innerText = "Все предложения";

            let attributes_button = document.createElement("button");
            attributes_button.className = "attributes-button";
            attributes_button.innerText = "Характеристики";

            buttons_container.appendChild(offers_button);
            buttons_container.appendChild(attributes_button);
            product_item.appendChild(buttons_container);

            offers_button.onclick = async function() {
                let opened_offers = product_item.querySelector(".offers-grid");
                let opened_attributes = product_item.querySelector(".attributes-grid");

                if (opened_offers) {
                    opened_offers.remove();
                    offers_button.innerText = "Все предложения";
                    return;
                }

                if (opened_attributes) {
                    opened_attributes.remove();
                    attributes_button.innerText = "Характеристики";
                }

                let offers_requestURL = `http://localhost:1234/product/offers/id/?product_id=${product.id}`;
                let offers_response = await fetch(offers_requestURL, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                });
                
                let offers_data = await offers_response.json();

                let offers_grid = document.createElement("div");
                offers_grid.className = "offers-grid";
                
                offers_grid.innerHTML = `<div class="offers-list"></div>`;

                let offers_list = offers_grid.querySelector(".offers-list");
                
                for (let offer of offers_data) {
                    let offer_item = document.createElement("div");
                    offer_item.className = "offer-item";
                    offer_item.innerHTML = `
                        <div class="offer-shop"><b>${offer.shop}</b></div>
                        <div class="offer-price"><b>${offer.price} ₽</b></div>
                        <b><a href="${offer.url}" target="_blank" class="offer-link">купить</a></b>
                    `;
                    offers_list.appendChild(offer_item);
                }

                product_item.appendChild(offers_grid);

                offers_button.innerText = "Скрыть предложения";
            };

            attributes_button.onclick = async function() {
                let opened_attributes = product_item.querySelector(".attributes-grid");
                let opened_offers = product_item.querySelector(".offers-grid");

                if (opened_offers) {
                    opened_offers.remove();
                    offers_button.innerText = "Все предложения";
                }

                if (opened_attributes) {
                    opened_attributes.remove();
                    attributes_button.innerText = "Характеристики";
                    return;
                }

                let attributes_requestURL = `http://localhost:1234/product/attributes/id?product_id=${product.id}`;
                let attributes_response = await fetch(attributes_requestURL, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                });

                let attributes_data = await attributes_response.json();

                let attributes_grid = document.createElement("div");
                attributes_grid.className = "attributes-grid";

                attributes_grid.innerHTML = `<div class="attributes-list"></div>`;
                
                let attributes_list = attributes_grid.querySelector(".attributes-list");

                let attribute = attributes_data[0];
                attributes_list.innerHTML = `
                    <div class="attribute-item"><span class="attribute-label">Страна:</span> <span class="attribute-value">${attribute.country == "NULL" ? "Не указано" : attribute.country}</span></div>
                    <div class="attribute-item"><span class="attribute-label">Тип:</span> <span class="attribute-value">${attribute.type == "NULL" ? "Не указано" : attribute.type}</span></div>
                    <div class="attribute-item"><span class="attribute-label">Дизайн:</span> <span class="attribute-value">${attribute.design == "NULL" ? "Не указано" : attribute.design}</span></div>
                    <div class="attribute-item"><span class="attribute-label">Материал корпуса:</span> <span class="attribute-value">${attribute.body_material == "NULL" ? "Не указано" : attribute.body_material}</span></div>
                    <div class="attribute-item"><span class="attribute-label">Материал грифа:</span> <span class="attribute-value">${attribute.neck_material == "NULL" ? "Не указано" : attribute.neck_material}</span></div>
                    <div class="attribute-item"><span class="attribute-label">Количество струн:</span> <span class="attribute-value">${attribute.number_of_strings == "NULL" ? "Не указано" : attribute.number_of_strings}</span></div>
                    <div class="attribute-item"><span class="attribute-label">Звукосниматели:</span> <span class="attribute-value">${attribute.pickups == "NULL" ? "Не указано" : attribute.pickups}</span></div>
                    <div class="attribute-item"><span class="attribute-label">Количество ладов:</span> <span class="attribute-value">${attribute.number_of_frets == "NULL" ? "Не указано" : attribute.number_of_frets}</span></div>
                `;
                product_item.appendChild(attributes_grid);

                attributes_button.innerText = "Скрыть характеристики";
            }

            products_grid.appendChild(product_item);
        }
    }

    else {
        products_grid.innerHTML = "<p>No products found </3</p>";
    }
}