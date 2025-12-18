from bs4 import BeautifulSoup
import requests
import json

def write_json(new_data, filename='output1.json'):
    with open(filename, 'r+', encoding='utf-8') as outfile:
        try:
            file_data = json.load(outfile)
            file_data.append(new_data)
            outfile.seek(0)
        except json.decoder.JSONDecodeError:
            file_data = []
            file_data.append(new_data)
        json.dump(file_data, outfile, ensure_ascii=False, indent=4)


def parse_electric():
    count = 0
    for i in range(19, 33):
        url = 'https://www.muztorg.ru/category/elektrogitary'
        if (i > 1):
            url = url + '?page=' + str(i)
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        links = []

        base_url = 'https://www.muztorg.ru'
        for link in soup.find_all('div', {'class': 'catalog-card__info'}):
            href = base_url + link.find('a', {'class': 'catalog-card__name'}).get('href') + '?view_tab=characteristics'
            links.append(href)

        for link in links:
            item_response = requests.get(link)
            item_soup = BeautifulSoup(item_response.text, 'html.parser')

            if not item_soup.find('div', {'class': 'mt-product-characteristics__item'}):
                continue

            count += 1

            g_type = 'Электрогитара'

            g_name = item_soup.find('h1', {'class': 'title-1'})
            if (g_name):
                g_name = g_name.text
            else:
                g_name = 'NULL'

            g_desc = item_soup.find('div', {'class': 'tab-pane product-tab product-description active'})
            if (g_desc):
                g_desc = g_desc.find('p')
                if (g_desc):
                    g_desc = g_desc.text
                else:
                    g_desc = 'NULL'

            g_price = item_soup.find('div', {'class': 'product-header-price__default-value'})
            if (g_price):
                g_price = g_price.text
            else:
                g_price = item_soup.find('div', {'class': 'mt-product-price__discounted-old'})
                if (g_price):
                    g_price = g_price.text
                else:
                    g_price = 'NULL'

            g_img = item_soup.find('div', {'class': 'mt-product-gallery__image'})
            if (g_img):
                g_img = g_img.find('img').get('src')
            else:
                g_img = 'NULL'

            g_article = item_soup.find('div', {'class': 'mt-product-head__item'})
            if (g_article):
                g_article = g_article.find('span').text
            else:
                g_article = 'NULL'

            g_manufacturer = item_soup.find('a', {'class': 'breadcrumbs__link', 'position': '4'})
            if (g_manufacturer):
                g_manufacturer = g_manufacturer.find('span').text
            else:
                g_manufacturer = 'NULL'


            guitar_data = {
                    'article': g_article,
                    'name': g_name,
                    'type': g_type,
                    'description': g_desc,
                    'price': g_price,
                    'manufacturer': g_manufacturer,
                    'country': 'NULL',
                    'design': 'NULL',
                    'body_material': 'NULL',
                    'neck_material': 'NULL',
                    'number_of_strings': 'NULL',
                    'pickups': 'NULL',
                    'number_of_frets': 'NULL',
                    'img': g_img,
                    'url': link[:-25]
            }

            param_map = {
                'Форма корпуса': 'design',
                'Страна производитель': 'country',
                'Материал корпуса': 'body_material',
                'Материал грифа': 'neck_material',
                'Количество струн': 'number_of_strings',
                'Конфигурация звукоснимателей': 'pickups',
                'Звукосниматель': 'pickups',
                'Количество ладов (диапазон)': 'number_of_frets'
            }

            params_list = item_soup.find_all('div', {'class': 'mt-product-characteristics__item'})
            for param in params_list:
                param_name = param.find('div', {'class': 'mt-product-characteristics__title'}).find('div').text
                param_val = param.find('div', {'class': 'mt-product-characteristics__value'}).text[21:-16]
                if (param_name in param_map):
                    if (param_val.isnumeric()):
                        param_val = int(param_val)
                    guitar_data[param_map[param_name]] = param_val

            write_json(guitar_data)
            
            print(count, 'logs')

def parse_acoustic():
    count = 0
    for i in range(6, 27):
        url = 'https://www.muztorg.ru/category/akusticheskie-gitary'
        if (i > 1):
            url = url + '?page=' + str(i)
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        links = []

        base_url = 'https://www.muztorg.ru'
        for link in soup.find_all('div', {'class': 'catalog-card__info'}):
            href = base_url + link.find('a', {'class': 'catalog-card__name'}).get('href') + '?view_tab=characteristics'
            links.append(href)

        for link in links:
            item_response = requests.get(link)
            item_soup = BeautifulSoup(item_response.text, 'html.parser')

            if not item_soup.find('div', {'class': 'mt-product-characteristics__item'}):
                continue

            count += 1

            g_name = item_soup.find('h1', {'class': 'title-1'})
            if (g_name):
                g_name = g_name.text
            else:
                g_name = 'NULL'

            g_type = 'NULL'
            
            g_desc = item_soup.find('div', {'class': 'tab-pane product-tab product-description active'})
            if (g_desc):
                g_desc = g_desc.find('p')
                if (g_desc):
                    g_desc = g_desc.text
                else:
                    g_desc = 'NULL'

            g_price = item_soup.find('div', {'class': 'product-header-price__default-value'})
            if (g_price):
                g_price = g_price.text
            else:
                g_price = item_soup.find('div', {'class': 'mt-product-price__discounted-old'})
                if (g_price):
                    g_price = g_price.text
                else:
                    g_price = 'NULL'

            g_img = item_soup.find('div', {'class': 'mt-product-gallery__image'})
            if (g_img):
                g_img = g_img.find('img').get('src')
            else:
                g_img = 'NULL'

            g_article = item_soup.find('div', {'class': 'mt-product-head__item'})
            if (g_article):
                g_article = g_article.find('span').text
            else:
                g_article = 'NULL'

            g_manufacturer = item_soup.find('a', {'class': 'breadcrumbs__link', 'position': '4'})
            if (g_manufacturer):
                g_manufacturer = g_manufacturer.find('span').text
            else:
                g_manufacturer = 'NULL'


            guitar_data = {
                    'article': g_article,
                    'name': g_name,
                    'type': g_type,
                    'description': g_desc,
                    'price': g_price,
                    'manufacturer': g_manufacturer,
                    'country': 'NULL',
                    'design': 'NULL',
                    'body_material': 'NULL',
                    'neck_material': 'NULL',
                    'number_of_strings': 'NULL',
                    'pickups': 'NULL',
                    'number_of_frets': 'NULL',
                    'img': g_img,
                    'url': link[:-25]
            }

            param_map = {
                'Форма корпуса': 'design',
                'Страна производитель': 'country',
                'Материал корпуса': 'body_material',
                'Материал грифа': 'neck_material',
                'Количество струн': 'number_of_strings',
                'Тип акустической гитары': 'pickups',
                'Количество ладов (диапазон)': 'number_of_frets'
            }

            params_list = item_soup.find_all('div', {'class': 'mt-product-characteristics__item'})
            for param in params_list:
                param_name = param.find('div', {'class': 'mt-product-characteristics__title'}).find('div').text
                param_val = param.find('div', {'class': 'mt-product-characteristics__value'}).text[21:-16]
                if (param_name in param_map):
                    if (param_val.isnumeric()):
                        param_val = int(param_val)
                    guitar_data[param_map[param_name]] = param_val
            if (guitar_data[param_map['Тип акустической гитары']] == 'без звукоснимателя'):
                guitar_data['type'] = 'Акустическая гитара'
            elif (guitar_data[param_map['Тип акустической гитары']] == 'со звукоснимателем'):
                guitar_data['type'] = 'Электроакустическая гитара'

            write_json(guitar_data)
            
            print(count, 'logs')
        

def parse_classical():
    count = 0
    for i in range(1, 11):
        url = 'https://www.muztorg.ru/category/klassicheskie-gitary'
        if (i > 1):
            url = url + '?page=' + str(i)
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        links = []

        base_url = 'https://www.muztorg.ru'
        for link in soup.find_all('div', {'class': 'catalog-card__info'}):
            href = base_url + link.find('a', {'class': 'catalog-card__name'}).get('href') + '?view_tab=characteristics'
            links.append(href)

        for link in links:
            item_response = requests.get(link)
            item_soup = BeautifulSoup(item_response.text, 'html.parser')

            if not item_soup.find('div', {'class': 'mt-product-characteristics__item'}):
                continue

            count += 1

            g_name = item_soup.find('h1', {'class': 'title-1'})
            if (g_name):
                g_name = g_name.text
            else:
                g_name = 'NULL'

            g_type = 'Классическая гитара'
            
            g_desc = item_soup.find('div', {'class': 'tab-pane product-tab product-description active'})
            if (g_desc):
                g_desc = g_desc.find('p')
                if (g_desc):
                    g_desc = g_desc.text
                else:
                    g_desc = 'NULL'

            g_price = item_soup.find('div', {'class': 'product-header-price__default-value'})
            if (g_price):
                g_price = g_price.text
            else:
                g_price = item_soup.find('div', {'class': 'mt-product-price__discounted-old'})
                if (g_price):
                    g_price = g_price.text
                else:
                    g_price = 'NULL'

            g_img = item_soup.find('div', {'class': 'mt-product-gallery__image'})
            if (g_img):
                g_img = g_img.find('img').get('src')
            else:
                g_img = 'NULL'

            g_article = item_soup.find('div', {'class': 'mt-product-head__item'})
            if (g_article):
                g_article = g_article.find('span').text
            else:
                g_article = 'NULL'

            g_manufacturer = item_soup.find('a', {'class': 'breadcrumbs__link', 'position': '4'})
            if (g_manufacturer):
                g_manufacturer = g_manufacturer.find('span').text
            else:
                g_manufacturer = 'NULL'


            guitar_data = {
                    'article': g_article,
                    'name': g_name,
                    'type': g_type,
                    'description': g_desc,
                    'price': g_price,
                    'manufacturer': g_manufacturer,
                    'country': 'NULL',
                    'design': 'NULL',
                    'body_material': 'NULL',
                    'neck_material': 'NULL',
                    'number_of_strings': 'NULL',
                    'pickups': 'NULL',
                    'number_of_frets': 'NULL',
                    'img': g_img,
                    'url': link[:-25]
            }

            param_map = {
                'Форма корпуса': 'design',
                'Страна производитель': 'country',
                'Материал корпуса': 'body_material',
                'Материал грифа': 'neck_material',
                'Количество струн': 'number_of_strings',
                'Тип классической гитары': 'pickups',
                'Количество ладов (диапазон)': 'number_of_frets'
            }

            params_list = item_soup.find_all('div', {'class': 'mt-product-characteristics__item'})
            for param in params_list:
                param_name = param.find('div', {'class': 'mt-product-characteristics__title'}).find('div').text
                param_val = param.find('div', {'class': 'mt-product-characteristics__value'}).text[21:-16]
                if (param_name in param_map):
                    if (param_val.isnumeric()):
                        param_val = int(param_val)
                    guitar_data[param_map[param_name]] = param_val

            write_json(guitar_data)
            
            print(count, 'logs')

parse_classical()