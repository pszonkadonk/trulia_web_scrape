import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree
import xml.dom.minidom
import pandas as pd
import numpy as np
import csv
import os

class ZillowServices:
    def __init__(self):
        self.zillow_home_data = []
    def get_home_addresses_trulia(self, county):
        filename="trulia-street-addresses-" + county + ".csv"
        path = os.getcwd() + '/more_trulia_housing_data'
        fullpath = os.path.join(path, filename)
        home_data = pd.read_csv(fullpath)
        home_addresses = pd.DataFrame()
        home_addresses['street'] = home_data['street']
        home_addresses['city'] = home_data.city

        return home_addresses

    def get_zillow_sales_data(self, county_file):
        filename = county_file +  ".csv"
        path = os.getcwd() + '/zillow_sales'
        fullpath = os.path.join(path, filename)
        sales_data = pd.read_csv(fullpath)

        return sales_data



    def write_to_csv(self, data, county): 
        filename = "sales-"+county+".csv"
        path = os.getcwd() + '/more_zillow_sales_data'
        fullpath = os.path.join(path, filename)

        print("writing data to file...")
        print(data)
        with open(fullpath, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)   

    def pretty_print(self, xml_content):
        content = xml.dom.minidom.parseString(xml_content)
        pretty_xml = content.toprettyxml()

        print(pretty_xml)

    def property_deep_search(self, address, city_state_zip, county):


        endpoint = "http://www.zillow.com/webservice/GetDeepSearchResults.htm?"
        
        #citystatezip format: "city, state zip"
        params = {
            "zws-id": "X1-ZWz199a3t11kwb_2doog",
            "address": address,
            "citystatezip": city_state_zip
        }

        response = requests.get(endpoint, params=params)
        root = ElementTree.fromstring(response.content)

        # self.pretty_print(response.content)
        status_code = root[1][1]

        if(status_code.text == '0'):  # request succeeded
            # RESPONSE
            try:
                results= root[2][0]
                result = results[0]

                zpid = result[1]

                # ADDRESS
                address = result.find('address')
                street = address.find('street').text if address.find('street') != None else "NA"
                zip_code = address.find('zipcode').text if address.find('zipcode') != None else "NA"
                city = address.find('city').text if address.find('city') != None else "NA"
                state = address.find('state').text if address.find('state') != None else "NA"
                latitude = address.find('latitude').text if address.find('latitude') != None else "NA"
                longitude = address.find('longitude').text if address.find('longitude') != None else "NA"
            except Exception:
                pass
                # HOUSE INFO
            try:    
                use_code = result.find('useCode').text if result.find('useCode') != None else "NA"
                tax_assessment_year = result.find('taxAssessmentYear').text if result.find('taxAssessmentYear') != None else "NA"
                tax_assessment = result.find('taxAssessment').text if result.find('taxAssessment') != None else "NA"
                year_built = result.find('yearBuilt').text if result.find('yearBuilt') != None else "NA"
                lot_size_sqft = result.find('lotSizeSqFt').text if result.find('lotSizeSqFt') != None else "NA"
                finished_sqft = result.find('finishedSqFt').text if result.find('finishedSqFt') != None else "NA"
                bathroom = result.find('bathrooms').text if result.find('bathrooms') != None else "NA"
                bedrooms = result.find('bedrooms').text if result.find('bedrooms') != None else "NA"
                last_sold_date = result.find('lastSoldDate').text if result.find('lastSoldDate') != None else "NA"
                last_sold_price = result.find('lastSoldPrice').text if result.find('lastSoldPrice') != None else "NA"

                zestimate_amount = result.find('zestimate')

                # LOCAL REAL ESTATE

                local_real_estate = result.find('localRealEstate')
                region = local_real_estate.find('region') if local_real_estate != None else "NA"

                region_id = region.get('id') if region != None else "NA"
                region_type = region.get('type') if region != None else "NA"
                region_name = region.get('name') if region != None else "NA"
            except Exception:
                pass

            self.zillow_home_data = [street, zip_code, city, state, latitude, longitude, use_code, tax_assessment_year, tax_assessment,
                                    year_built, lot_size_sqft, finished_sqft, bathroom, bedrooms, last_sold_date, last_sold_price, region_id,
                                    region_type, region_name]

            print(self.zillow_home_data)
            self.write_to_csv(self.zillow_home_data, county)
        else:
            print(address + " is invalid")