from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import os

def write_street_address(addresses, county):
    filename = "trulia-street-addresses-"+county+".csv"
    path = os.getcwd() + '/more_trulia_housing_data'
    fullpath = os.path.join(path, filename)
    with open(fullpath, "w") as street_file:
          for home in addresses:
            street=home.split('|')[0]
            city = home.split('|')[1]
            writer=csv.writer(street_file)
            writer.writerow([street,city])


def get_street_addresses(county):
    count = 10
    limit_page = 20
    home_addresses = []

    while(count < limit_page):
        url = "https://www.trulia.com/sold/" + county + "/"
        url += str(count) + "_p"
        print(url)
        trulia_content = requests.get(url).content
        soup = BeautifulSoup(trulia_content, "html.parser")
        for home in soup.find_all('a', class_='tileLink phm'):
            city = home['href'].split('/')[3]
            home_addresses.append(home.get('alt') + "|" + city)
        
        count+=1
    write_street_address(home_addresses, county)

counties = {
    "bergen": "34003_c",
    "essex": "34013_c",
    "hudson": "34017_c",
    "morris": "34027_c",
    "passaic": "34031_c",
    "union": "34039_c",
    "warren": "34041_c"
}


for county, county_id in counties.items():
    get_street_addresses(county_id)

