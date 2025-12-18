import json
import pymysql
import re

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='guitardb',
    charset='utf8mb4'
)

cursor = connection.cursor()

def format_price(price):
    numbers = re.findall(r'\d+', price)
    formatted = ''.join(numbers)
    return int(formatted)

def format_website(url):
    if 'muzikroom' in url:
        return 'muzikroom'
    if 'muztorg' in url:
        return 'muztorg'
    if 'skifmusic' in url:
        return 'skifmusic'

with open('general.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
    for obj in data:
        name = obj.get('name')
        brand = obj.get('manufacturer')
        type = obj.get('type')
        description = obj.get('description')
        img_url = obj.get('img')
            
        sql_products = "INSERT INTO Products (name, brand, type, description, img_url) VALUES (%s, %s, %s, %s, %s)"
        values_products = (name, brand, type, description, img_url)
        
        cursor.execute(sql_products, values_products)
        connection.commit()

        product_id = cursor.lastrowid

        price = obj.get('price')
        formatted_price = format_price(price)
        url = obj.get('url')
        formatted_website = format_website(url)

        sql_offers = "INSERT INTO Offers (product_id, name, website_name, price, url) VALUES (%s, %s, %s, %s, %s)"
        values_offers = (
            product_id, name, formatted_website, formatted_price, url
        )

        cursor.execute(sql_offers, values_offers)
        connection.commit()

        article = obj.get('article')
        country = obj.get('country')
        design = obj.get('design')
        body_material = obj.get('body_material')
        neck_material = obj.get('neck_material')
        number_of_strings = obj.get('number_of_strings')
        if (not isinstance(number_of_strings, int)):
            number_of_strings = None
        pickups = obj.get('pickups')
        number_of_frets = obj.get('number_of_frets')
        if (not isinstance(number_of_frets, int)):
            number_of_frets = None
        
        sql_attributes = "INSERT INTO Attributes (product_id, article, country, design, body_material, neck_material, number_of_strings, pickups, number_of_frets) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values_attributes = (
            product_id, article, country, design, body_material, neck_material,
            number_of_strings, pickups, number_of_frets
        )
        
        cursor.execute(sql_attributes, values_attributes)
        connection.commit()
        
        print(f'inserted product with id {product_id}')
        

cursor.close()
connection.close()