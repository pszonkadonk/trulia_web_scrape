import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree
import xml.dom.minidom
import pandas as pd
import numpy as np
import csv
import os

def get_home_addresses(county):
    filename="trulia-street-addresses-" + county + ".csv"
    path = os.getcwd() + '/housing_data'
    fullpath = os.path.join(path, filename)
    home_data = pd.read_csv(fullpath)
    home_addresses = pd.DataFrame()
    home_addresses['street'] = home_data['street']
    home_addresses['city'] = home_data.city


    return home_addresses

def write_to_csv(data, county): 
    filename = "sales-"+county+".csv"
    path = os.getcwd() + '/zillow_sales'
    fullpath = os.path.join(path, filename)

    print("writing data to file...")
    with open(fullpath, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)   

def pretty_print(xml_content):
    content = xml.dom.minidom.parseString(xml_content)
    pretty_xml = content.toprettyxml()

    print(pretty_xml)

def property_deep_search(address, city_state_zip, county):


    endpoint = "http://www.zillow.com/webservice/GetDeepSearchResults.htm?"
    
    #citystatezip format: "city, state zip"
    params = {
        "zws-id": "X1-ZWz199a3t11kwb_2doog",
        "address": address,
        "citystatezip": city_state_zip
    }

    response = requests.get(endpoint, params=params)
    root = ElementTree.fromstring(response.content)

    pretty_print(response.content)
    status_code = root[1][1]

    if(status_code.text == '0'):  # request succeeded
        # RESPONSE
        try:
            results= root[2][0]
            result = results[0]

            zpid = result[1]

            # ADDRESS
            address = result.find('address')
            street = address.find('street').text if address.find('street') != None else "N/A"
            zip_code = address.find('zipcode').text if address.find('zipcode') != None else "N/A"
            city = address.find('city').text if address.find('city') != None else "N/A"
            state = address.find('state').text if address.find('state') != None else "N/A"
            latitude = address.find('latitude').text if address.find('latitude') != None else "N/A"
            longitude = address.find('longitude').text if address.find('longitude') != None else "N/A"
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
            last_sold_price = result.find('lastSoldPrice').text if result.find('lastSoldPrice') != None else "N/A"

            zestimate_amount = result.find('zestimate')

            # LOCAL REAL ESTATE

            local_real_estate = result.find('localRealEstate')
            region = local_real_estate.find('region') if local_real_estate != None else "N/A"

            region_id = region.get('id') if region != None else "N/A"
            region_type = region.get('type') if region != None else "N/A"
            region_name = region.get('name') if region != None else "N/A"
        except Exception:
            pass

        zillow_home_data = [street, zip_code, city, state, latitude, longitude, use_code, tax_assessment_year, tax_assessment,
                            year_built, lot_size_sqft, finished_sqft, bathroom, bedrooms, last_sold_date, last_sold_price, region_id,
                            region_type, region_name]

        print(zillow_home_data)
        write_to_csv(zillow_home_data, county)
    else:
        print(address + " is invalid")
  

    
bergen_home_addresses = get_home_addresses("bergen")
essex_home_addresses = get_home_addresses("essex")
hudson_home_addresses = get_home_addresses("hudson")
morris_home_addresses = get_home_addresses("morris")
passaic_home_addresses = get_home_addresses("passaic")
union_home_addresses = get_home_addresses("union")
warren_home_addresses = get_home_addresses("warren")



# property_deep_search('Unit 4d', "Hackensack, NJ", "bergen")

# for index, row in bergen_home_addresses.iterrows():
#     property_deep_search(row['street'], row['city']+", NJ", "bergen" )
    

# for index, row in essex_home_addresses.iterrows():
#     property_deep_search(row['street'], row['city']+", NJ", "essex" )


# for index, row in hudson_home_addresses.iterrows():
#     property_deep_search(row['street'], row['city']+", NJ", "hudson" )

# for index, row in morris_home_addresses.iterrows():
#     property_deep_search(row['street'], row['city']+", NJ", "morris" )

# for index, row in passaic_home_addresses.iterrows():
#     property_deep_search(row['street'], row['city']+", NJ", "passaic" )

# for index, row in union_home_addresses.iterrows():
#     property_deep_search(row['street'], row['city']+", NJ", "union" )

# for index, row in warren_home_addresses.iterrows():
#     property_deep_search(row['street'], row['city']+", NJ", "warren" )



