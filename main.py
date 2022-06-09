from bs4 import BeautifulSoup
import requests

urls = ['', 'https://www.ziko.pl/lokalizator/', '']


def second_pasrser(url):
    # req = requests.get(url).text
    # soup = BeautifulSoup(req, 'lxml')
    # with open('parsing_data/pl.txt', 'w', encoding='utf8') as file:
    #     file.write(req)

    with open('parsing_data/pl.txt', encoding='utf8') as file:
        req_text = file.read()
    soup = BeautifulSoup(req_text, 'lxml')

    items = soup.find_all('tr', class_='mp-pharmacy-element')
    for item in items:
        item_link = 'https://www.ziko.pl' + item.find(class_='morepharmacy').a['href']

        working_hours = []
        working_hours_data = item.find('td', class_='mp-table-hours')
        for working_hours_item in working_hours_data.next_elements('span'):
            if working_hours_data.index(working_hours_item) % 2 == 0:
                working_hours.append(working_hours_item.text)
            else:
                working_hours[-1] += working_hours_item.text

        print(working_hours)


if __name__ == '__main__':
    second_pasrser(urls[1])
