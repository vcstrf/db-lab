from bs4 import BeautifulSoup
import requests
import json


def write_json(new_data, filename='output2.json'):
    with open(filename, 'r+', encoding='utf-8') as outfile:
        try:
            file_data = json.load(outfile)
            file_data.append(new_data)
            outfile.seek(0)
        except json.decoder.JSONDecodeError:
            file_data = []
            file_data.append(new_data)
        json.dump(file_data, outfile, ensure_ascii=False, indent=4)

count = 0

for i in range(1, 41):
    url = 'https://skifmusic.ru/catalog/gitaryi-1'
    if (i > 1):
        url = 'https://skifmusic.ru/catalog/gitaryi-1' + '/page' + str(i)
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    for link in soup.find_all('a', {'class': 'product-card__link'}):
        href = link.get('href')
        links.append(href)

    for link in links:
        item_response = requests.get(link)
        item_soup = BeautifulSoup(item_response.text, 'html.parser')
        count += 1

        g_name = item_soup.select_one('.breadcrumbs__item:nth-of-type(6)')
        if (g_name):
            g_name = g_name.text
        else:
            g_name = 'NULL'

        g_price = item_soup.find('p', {'class': 'product-card-info__price'})
        if (g_price):
            g_price = g_price.text[9:-12]
        else:
            g_price = 'NULL'

        img_flag = item_soup.find('h1', {'class': 'product-card-info__title'}).text
        g_img = item_soup.find('img', {'alt': img_flag})
        if (g_img):
            g_img = g_img.get('src')
        else:
            g_img = 'NULL'

        g_desc = item_soup.find('div', {'id': 'description'})
        if (g_desc):
            g_desc = g_desc.find('p')
            if (g_desc):
                g_desc = g_desc.text
            else:
                g_desc = 'NULL'

        guitar_data = {
                'article': 'NULL',
                'name': g_name,
                'type': 'NULL',
                'description': g_desc,
                'price': g_price,
                'manufacturer': 'NULL',
                'country': 'NULL',
                'design': 'NULL',
                'body_material': 'NULL',
                'neck_material': 'NULL',
                'number_of_strings': 'NULL',
                'pickups': 'NULL',
                'number_of_frets': 'NULL',
                'img': g_img,
                'url': link
        }

        param_map = {
            'Артикул': 'article',
            'Тип': 'type',
            'Производитель': 'manufacturer',
            'Форма корпуса': 'design',
            'Страна производства': 'country',
            'Дека': 'body_material',
            'Верхняя дека': 'body_material',
            'Гриф': 'neck_material',
            'Количество струн': 'number_of_strings',
            'Звукосниматели': 'pickups',
            'Количество ладов': 'number_of_frets'
        }

        params_list = item_soup.select('ul.ps-3.pb-0 li')
        for param in params_list:
            param_name = param.select_one('span:first-child').text[:-2]
            param_val = param.select_one('span:nth-of-type(2)').text
            if (param_val == 'NULL'):
                param_val = param.find('span:nth-of-type(2)').find('a').text
            if (param_name in param_map):
                if (param_val.isnumeric()):
                    param_val = int(param_val)
                guitar_data[param_map[param_name]] = param_val

        write_json(guitar_data)
        
        print(count, 'logs')
