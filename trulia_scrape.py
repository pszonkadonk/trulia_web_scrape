from bs4 import BeautifulSoup
import requests



def get_home_urls(url):
    home_urls = []
    trulia_content = requests.get(url).content
    soup = BeautifulSoup(trulia_content, "html.parser")
    for home in soup.find_all('a', class_='tileLink'):
        home_urls.append("https://www.trulia.com/" + home['href'])

    return home_urls

def get_home_info(home_url):
    trulia_content = requests.get(home_url).content
    soup = BeautifulSoup(trulia_content, "html.parser")
    print(soup.prettify())

    return



# home_urls = get_home_urls("https://www.trulia.com/NJ/Jersey_City/")
# get_home_urls("https://www.trulia.com/NJ/Jersey_City/2_p/") #page 2
# get_home_urls("https://www.trulia.com/NJ/Jersey_City/3_p/") #page 3
# get_home_urls("https://www.trulia.com/NJ/Jersey_City/x_p/") #page etc


home_data = get_home_info("https://www.trulia.com//property/3262926259-30-Freedomway-404-Jersey-City-NJ-07305")
