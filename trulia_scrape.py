from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_home_urls(url):
    home_urls = []
    trulia_content = requests.get(url).content
    soup = BeautifulSoup(trulia_content, "html.parser")
    for home in soup.find_all('a', class_='tileLink'):
        home_urls.append("https://www.trulia.com/" + home['href'])
    
    print(home_urls)

    return home_urls

def get_home_info(home_url):
    trulia_content = requests.get(home_url).content
    soup = BeautifulSoup(trulia_content, "html.parser")
    print(soup.prettify())

    



# home_urls = get_home_urls("https://www.trulia.com/NJ/Jersey_City/")
# get_home_urls("https://www.trulia.com/NJ/Jersey_City/2_p/") #page 2
# get_home_urls("https://www.trulia.com/NJ/Jersey_City/3_p/") #page 3
# get_home_urls("https://www.trulia.com/NJ/Jersey_City/x_p/") #page etc


home_data = get_home_info("https://www.trulia.com/property/3039415415-67-Bright-St-1-Jersey-City-NJ-07302")
