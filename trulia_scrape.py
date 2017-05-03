from bs4 import BeautifulSoup
import requests
import pandas as pd

def write_street_address(addresses, city):
    with open("trulia-street-addresses-"+city+".txt", "w") as street_file:
        for home in addresses:
            street_file.write(home)
            street_file.write('\n')


def get_street_addresses(city):
    count = 1
    limit_page = 3
    home_addresses = []
    url = "https://www.trulia.com/NJ/" + city + "/"

    while(count < limit_page):
        url = url + str(count) + "_p"
        trulia_content = requests.get(url).content
        soup = BeautifulSoup(trulia_content, "html.parser")
        for home in soup.find_all('a', class_='tileLink phm'):
            home_addresses.append(home.get('alt'))

        count+=1
    print(home_addresses)
    write_street_address(home_addresses, city)



    

get_street_addresses("Jersey City")