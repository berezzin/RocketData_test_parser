from bs4 import BeautifulSoup
import requests
import json

urls = ['https://api.kfc.com/api/store/v2/store.get_restaurants?showClosed=true',
        'https://www.ziko.pl/lokalizator/',
        '']

def first_parser(url):
    req = requests.get(url).json()
    items = req['searchResults']
    for item in items:
        address = item['storePublic']['contacts']['streetAddress']['ru']
        latlon = item['storePublic']['contacts']['coordinates']['geometry']['coordinates']
        phones = item['storePublic']['contacts']['phoneNumber']
        if item['storePublic']['status'] == 'Closed':
            working_hours = 'Closed'
        else:
            working_hours = item['storePublic']['openingHours']['regularDaily']




def second_parser(url):
    print('Начался парсинг второго сайт')
    req = requests.get(url).text
    soup = BeautifulSoup(req, 'lxml')

    data_to_export = []

    items = soup.find_all('tr', class_='mp-pharmacy-element')
    for item in items:
        item_link = 'https://www.ziko.pl' + item.find(class_='morepharmacy').a['href']

        working_hours = []
        working_hours_table = item.find('td', class_='mp-table-hours').find_all('span')
        for working_hours_item in working_hours_table:
            if working_hours_table.index(working_hours_item) % 2 == 0:
                working_hours.append(working_hours_item.text)
            else:
                working_hours[-1] += working_hours_item.text

        request_item_text = requests.get(item_link).text
        item_soup = BeautifulSoup(request_item_text, 'lxml')

        contact_data = item_soup.find('div', class_='leftdetailsbox')
        address = ''
        name = ''
        phones = ''
        for item in contact_data:
            if item.find('strong').text.strip() == 'Placówka':
                name = item.find('span').text.strip()
            elif item.find('strong').text.strip() == 'Adres':
                address = item.find('span').text.strip()
            elif item.find('strong').text.strip() == 'Miasto':
                address += ', ' + item.find('span').text.strip()
            elif item.find('strong').text.strip().strip() == 'Telefon':
                phones = item.find('a').text.strip()

        coordinates = []
        coordinate_data = item_soup.find('div', class_='coordinates').find_all('span')
        for item in coordinate_data:
            if item.text.strip().startswith('Szerokość geograficzna:'):
                coordinates.append(item.text.strip().removeprefix('Szerokość geograficzna: '))
            elif item.text.strip().startswith('Długość geograficzna:'):
                coordinates[-1] += ', ' + item.text.strip().removeprefix('Długość geograficzna: ')

        data = {
            "address": address,
            "latlon": coordinates,
            "name": name,
            "phones": phones,
            "working_hours": working_hours
        }

        data_to_export.append(data)

    with open(f"parsing_data/second_site.json", 'w', encoding='utf-8') as file:
        json.dump(data_to_export, file, indent=4, ensure_ascii=False)

    print('Парсинг второго сайта завершён, данные доступны в папке parsing_data')


if __name__ == '__main__':
    first_parser(urls[0])
    # second_parser(urls[1])
