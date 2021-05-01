import argparse
import requests
from bs4 import BeautifulSoup
from xlwt import Workbook
import os


apt_base_url = 'https://www.apartments.com/'
loc_base_url = 'http://dev.virtualearth.net/REST/v1/Locations/US/'
commute_base_url = 'https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?'
with open("api_key.txt") as file:
    api_key = file.readline().rstrip()

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
excel_headers = ['Name', 'Address', 'Price', 'Beds', 'Link', 'Driving Time (min)', 'Transit Time (min)', 'Walking Time (min)']

parser = argparse.ArgumentParser()
# add command line args
parser.add_argument("-city", type=str, required=True)
parser.add_argument("-state", type=str, required=True)
parser.add_argument("-price", type=str, required=False, default="")
parser.add_argument("-beds", type=str, required=False, default="min-1-bedrooms")
parser.add_argument("-bathrooms", type=str, required=False, default="1-bathrooms")
parser.add_argument("-features", type=str, required=False, default="")
parser.add_argument("-work", type=str, required=False, default="")


def create_sheet(input_list, file_loc, work_address):
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
        apt_info = get_info(apt, work_address)
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
    return soup.find('div', class_='placardContainer').find_all('article', class_='placard')


def get_info(apt, work_address):
    # get apartment details
    name = apt.find('span', class_='js-placardTitle title')
    address = apt.find('div', class_='property-address js-url')
    price = apt.find('div', class_='price-range')
    beds = apt.find('div', class_='bed-range')
    link = apt.find('a', class_='property-link')
    # get commute times
    if work_address != "":
        commute_times = get_commute_times(address, work_address)
        return [name, address, price, beds, link, commute_times['driving'], commute_times['transit'], commute_times['walking']]
    return [name, address, price, beds, link]


def get_commute_times(address, work_address):
    org_latitude, org_longitude = get_coordinates(address.contents[0])
    dest_latitude, dest_longitude = get_coordinates(work_address)
    commute_times = {}
    modes = ['driving', 'transit', 'walking']
    for travel_mode in modes:
        commute_url = commute_base_url + 'origins=' + str(org_latitude) + ',' + str(org_longitude) + '&destinations=' + str(dest_latitude) + ',' + str(dest_longitude) + '&travelMode=' + travel_mode + '&key=' + api_key
        response = requests.get(commute_url).json()
        commute_time = response['resourceSets'][0]['resources'][0]['results'][0]['travelDuration']
        commute_times[travel_mode] = commute_time
    return commute_times


def get_coordinates(address):
    state, zipcode, city, street_address = parse_address(address)
    location_url = loc_base_url + state + '/' + zipcode + '/' + city + '/' + street_address + '?key=' + api_key
    response = requests.get(location_url).json()
    coordinates = response['resourceSets'][0]['resources'][0]['point']['coordinates']
    return coordinates[0], coordinates[1]


def parse_address(address):
    split_address = list(address.split(" "))
    zipcode = split_address[len(split_address) - 1]
    state = split_address[len(split_address) - 2]
    city = str.rstrip(split_address[len(split_address) - 3][:-1])
    street_address = str.rstrip('%20'.join(split_address[:-3])[:-1])
    return state, zipcode, city, street_address

# parse command line args
args = parser.parse_args()
inputs = {'city': args.city,
          'state': args.state,
          'price':  args.price,
          'beds': args.beds,
          'bathrooms': args.bathrooms,
          'features': args.features,
          'work_address': args.work}

create_sheet(inputs, 'aptmts.xls', inputs['work_address'])
print(os.path.realpath('aptmts.xls'))