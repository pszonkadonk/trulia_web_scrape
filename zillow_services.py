import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree
import xml.dom.minidom


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

    pretty_print(response.content)


    #RESPONSE

    results= root[2][0]
    result = results[0]

    zpid = result[1]

    # ADDRESS
    address = result[2]
    street = address[0]
    zip_code = address[1]
    city = address[2]
    state = address[3]
    latitude = address[4]
    longitude = address[5]

    # HOUSE INFO

    use_code = result[4]
    tax_assessment_year = result[5]
    tax_assessment = result[6]
    year_built = result[7]
    lot_size_sqft = result[8]
    finished_sqft = result[9]
    bathroom = result[10]
    bedrooms = result[11]
    last_sold_date = result[12]
    last_sold_price = result[13]

    zestimate_amount = result[14][0]

    # LOCAL REAL ESTATE

    region = result[15][0]
    neighborhood_type = result[15][1]
    neighborhood_name = result[15][2]

    region_id = region.get('id')
    region_type = region.get('type')
    region_name = region.get('name')


    
    

    
    

    




property_deep_search("120 Lincoln Street", "Jersey City, NJ")

