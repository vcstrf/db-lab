from bs4 import BeautifulSoup
import requests
import json


def write_json(new_data, filename='output.json'):
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
    url = 'https://muzikroom.ru/shop/gitary/?sorting=6'
    if (i > 1):
        url = 'https://muzikroom.ru/shop/gitary/' + 'page-' + str(i) + '/?sorting=6&'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    base_url = 'https://muzikroom.ru'
    for link in soup.find_all('div', {'class': 'name'}):
        href = base_url + link.find('a').get('href')
        links.append(href)

    for link in links:
        item_response = requests.get(link)
        item_soup = BeautifulSoup(item_response.text, 'html.parser')
        count += 1

        g_type = item_soup.find('span', {'class': 'type'})
        if (g_type):
            g_type = item_soup.find('span', {'class': 'type'}).text
        else:
            g_type = 'NULL'

        g_name = item_soup.find('div', {'class': 'h1 visible-pda'})
        if (g_name):
            g_name = item_soup.find('div', {'class': 'h1 visible-pda'}).text
        else:
            g_name = 'NULL'
        
        g_desc = item_soup.find('div', {'class': 'descr content-text'})
        if (g_desc):
            g_desc = item_soup.find('div', {'class': 'descr content-text'}).find('p').text
        else:
            g_desc = 'NULL'

        g_price = item_soup.find('div', {'class': 'price'})
        if (g_price):
            g_price = item_soup.find('div', {'class': 'price'}).text
        else:
            g_price = 'NULL'

        g_img = item_soup.find('meta', {'itemprop': 'image'})
        if (g_img):
            g_img = item_soup.find('meta', {'itemprop': 'image'}).get('content')[20:]
        else:
            g_img = 'NULL'

        guitar_data = {
                'article': 'NULL',
                'name': g_name,
                'type': g_type,
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
            'Производитель': 'manufacturer',
            'Корпус (тип)': 'design',
            'Страна производства': 'country',
            'Корпус (материал)': 'body_material',
            'Гриф (материал)': 'neck_material',
            'Количество струн': 'number_of_strings',
            'Звукосниматели (вид)': 'pickups',
            'Звукосниматель': 'pickups',
            'Количество ладов': 'number_of_frets'
        }

        params_list = item_soup.find_all('div', {'class': 'params-row'})
        for param in params_list:
            param_name = param.find('div', {'class': 'param-name'}).text
            param_val = param.find('div', {'class': 'param-val'}).text
            if (param_name in param_map):
                if (param_val.isnumeric()):
                    param_val = int(param_val)
                guitar_data[param_map[param_name]] = param_val

        write_json(guitar_data)
        
        print(count, 'logs')
