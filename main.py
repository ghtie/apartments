import argparse
import requests
from bs4 import BeautifulSoup
from xlwt import Workbook
import os


apt_base_url = 'https://www.apartments.com/'
walkscore_base_url = 'https://www.walkscore.com/score/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
excel_headers = ['Name', 'Address', 'Price', 'Beds', 'Link', 'Walk Score', 'Transit Score', 'Bike Score']

parser = argparse.ArgumentParser()
# add command line args
parser.add_argument("-city", type=str, required=True)
parser.add_argument("-state", type=str, required=True)
parser.add_argument("-price", type=str, required=False, default="")
parser.add_argument("-beds", type=str, required=False, default="min-1-bedrooms")
parser.add_argument("-bathrooms", type=str, required=False, default="1-bathrooms")
parser.add_argument("-features", type=str, required=False, default="")


def create_sheet(input_list, file_loc):
    url = create_apt_search_url(input_list)

    # create Excel sheet
    wb = Workbook()
    sheet = wb.add_sheet('Apartment Listings')

    # add headers
    col_cnt = 0
    for header in excel_headers:
        sheet.write(0, col_cnt, header)
        col_cnt += 1

    # get apartment info
    row_cnt = 1
    apt_listing = get_listings(url)
    for apt in apt_listing:
        apt_info = get_info(apt)
        write_info(apt_info, row_cnt, sheet)
        row_cnt += 1
    wb.save(file_loc)


def create_apt_search_url(input_dict):
    if input_dict['price'] != '':
        input_dict['price'] = '-' + input_dict['price']
    return apt_base_url + input_dict['city'] + '-' + input_dict['state'] + '/' + input_dict['beds'] + '-' \
           + input_dict['bathrooms'] + input_dict['price'] + '/' + input_dict['features']


def write_info(apt_info, row_cnt, sheet):
    # write info to spreadsheet
    for i in range(len(apt_info)):
        if apt_info[i] is not None:
            if i < 4:
                info = apt_info[i].contents[0]
            elif i == 4:  # get hyperlink
                info = apt_info[i].get('href')
            else:
                info = apt_info[i]
        else:
            info = ""
        sheet.write(row_cnt, i, info)


def get_listings(url):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup.find(id='placardContainer').find_all('article', class_='placard')


def get_info(apt):
    # get apartment details
    name = apt.find('span', class_='js-placardTitle title')
    address = apt.find('div', class_='property-address js-url')
    price = apt.find('div', class_='price-range')
    beds = apt.find('div', class_='bed-range')
    link = apt.find('a', class_='property-link')
    # get walk/transit scores
    walkscores = get_walk_transit_scores(address.contents[0])
    return [name, address, price, beds, link, walkscores['walk'], walkscores['transit'], walkscores['bike']]


def get_walk_transit_scores(address):
    formatted_address = address.replace(' ', '-').replace('.', '-')
    page = requests.get(walkscore_base_url+formatted_address, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    score_container = soup.find_all('div', class_='clearfix score-div')
    scores = {'walk': None, 'transit': None, 'bike': None}
    for score_info in score_container:
        score = score_info.find('img')['src']
        if 'walk/score' in score:
            scores['walk'] = int(score.replace('//pp.walk.sc/badge/walk/score/', '').replace('.svg', ''))
        elif 'transit/score' in score:
            scores['transit'] = int(score.replace('//pp.walk.sc/badge/transit/score/', '').replace('.svg', ''))
        else:
            scores['bike'] = int(score.replace('//pp.walk.sc/badge/bike/score/', '').replace('.svg', ''))
    return scores


# parse command line args
args = parser.parse_args()
inputs = {'city': args.city,
          'state': args.state,
          'price':  args.price,
          'beds': args.beds,
          'bathrooms': args.bathrooms,
          'features': args.features}
create_sheet(inputs, 'aptmts.xls')
print(os.path.realpath('aptmts.xls'))

