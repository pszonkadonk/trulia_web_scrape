import requests, re
from bs4 import BeautifulSoup
import csv

def fetchhtml(url):
    PRETEND_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0'
    content = requests.get(url, headers={'User-Agent': PRETEND_AGENT}).content
    soup = BeautifulSoup(content, "html.parser")
    return soup

def geturl(url,page):
    url = url + str(page) + '_p/'
    return url

def write_to_csv(data): 
    print("writing data to file...")
    with open('home_detail.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)   

def scrapeData():
    count = 1
    home_inventory = []

    #For iterating through pages just set limitPage to number of pages you want to iterate
    limitPage = 60

    #Property count, will give you the total number of user properties scraped
    homeCount = 1

    url = "https://www.trulia.com/for_sale/40.692466103506,40.79703022221,-74.294922954219,-74.075196391719_xy/12_zm/"

    while (count < limitPage):
        soup = fetchhtml(geturl(url,count))

        homeLink = ["https://www.trulia.com" + x.get("href") for x in soup.find_all('a', {'class': "tileLink"})]

        for link in homeLink:
            user =  fetchhtml(link.strip())
            attributes = []
            home_detail = []

            street = user.find_all('span', {'class': "headingDoubleSuper h2 typeWeightNormal mvn ptn"})[0].text.replace("\n","").strip()
            address = user.find_all('span', {'class': "headlineDoubleSub typeWeightNormal typeLowlight man"})[0].text.replace("\n", "").strip()
            address = re.sub('\s+', ' ', address)
            city = address.split(",")[0]
            state = address.replace(" ","").split(",")[1][0:2]
            zip_code = address.replace(" ","").split(",")[1][2:7]
                        
            details = user.find('ul', {'class': "listBulleted mbn"}).findAll('li')
            
            for li in details:
                attributes.append(str(li).replace("<li>","")
                                        .replace("</li>","")
                                        .replace("Price: $",""))

            home_detail = [link, street, city, state, zip_code]
            home_detail.extend(attributes)
            home_inventory.append(home_detail)

            homeCount += 1
        count += 1

        write_to_csv(home_inventory)



if __name__=='__main__':
    scrapeData()