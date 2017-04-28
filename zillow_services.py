import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree
import xml.dom.minidom
import pandas as pd
import numpy as np
import csv

def get_home_addresses():
    home_data = pd.read_csv("foo.csv")
    home_addressess = pd.DataFrame()
    home_addressess['street'] = home_data['street']
    home_addressess['city_state'] = home_data.city + ", " + home_data.state

    return home_addressess

def write_to_csv(data): 
    print("writing data to file...")
    with open('zillow-data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)   

def pretty_print(xml_content):
    content = xml.dom.minidom.parseString(xml_content)
    pretty_xml = content.toprettyxml()

    print(pretty_xml)

def property_deep_search(address, city_state_zip):


    endpoint = "http://www.zillow.com/webservice/GetDeepSearchResults.htm?"
    
    #citystatezip format: "city, state zip"
    params = {
        "zws-id": "X1-ZWz199a3t11kwb_2doog",
        "address": address,
        "citystatezip": city_state_zip
    }

    response = requests.get(endpoint, params=params)
    root = ElementTree.fromstring(response.content)

    # pretty_print(response.content)


    # RESPONSE
    try:
        results= root[2][0]
        result = results[0]

        zpid = result[1]

        # ADDRESS
        address = result.find('address')
        street = address.find('street').text
        zip_code = address.find('zipcode').text
        city = address.find('city').text
        state = address.find('state').text
        latitude = address.find('latitude').text
        longitude = address.find('longitude').text
    except Exception:
        pass
        # HOUSE INFO
    try:    
        use_code = result.find('useCode').text if result.find('useCode') != None else "N/A"
        tax_assessment_year = result.find('taxAssessmentYear').text if result.find('taxAssessmentYear') != None else "N/A"
        tax_assessment = result.find('taxAssessment').text if result.find('taxAssessment') != None else "N/A"
        year_built = result.find('yearBuilt').text if result.find('yearBuilt') != None else "N/A"
        lot_size_sqft = result.find('lotSizeSqFt').text if result.find('lotSizeSqFt') != None else "N/A"
        finished_sqft = result.find('finishedSqFt').text if result.find('finishedSqFt') != None else "N/A"
        bathroom = result.find('bathrooms').text if result.find('bathrooms') != None else "N/A"
        bedrooms = result.find('bedrooms').text if result.find('bedrooms') != None else "N/A"
        last_sold_date = result.find('lastSoldDate').text if result.find('lastSoldDate') != None else "N/A"
        last_sold_price = result.find('lastSoldPrice ').text if result.find('lastSoldPrice ') != None else "N/A"

        zestimate_amount = result.find('zestimate')

        # LOCAL REAL ESTATE

        local_real_estate = result.find('localRealEstate')
        region = local_real_estate.find('region')
        # neighborhood_type = result[15][1]
        # neighborhood_name = result[15][2]

        region_id = region.get('id')
        region_type = region.get('type')
        region_name = region.get('name')
    except Exception:
        pass

    zillow_home_data = [street, zip_code, city, state, latitude, longitude, use_code, tax_assessment_year, tax_assessment,
                        year_built, lot_size_sqft, finished_sqft, bathroom, bedrooms, last_sold_date, last_sold_price, region_id,
                        region_type, region_name]

    write_to_csv(zillow_home_data)



        

    
home_addresses = get_home_addresses()

for index, row in home_addresses.iterrows():
    property_deep_search(row['street'], row['city_state'])
    




# property_deep_search("270 Harrison Ave", "Jersey City, NJ")
