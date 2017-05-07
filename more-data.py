from ZillowServices import ZillowServices

zillow = ZillowServices()

bergen_home_addresses = zillow.get_home_addresses_trulia("bergen")
essex_home_addresses = zillow.get_home_addresses_trulia("essex")
hudson_home_addresses = zillow.get_home_addresses_trulia("hudson")
morris_home_addresses = zillow.get_home_addresses_trulia("morris")
passaic_home_addresses = zillow.get_home_addresses_trulia("passaic")
union_home_addresses = zillow.get_home_addresses_trulia("union")
warren_home_addresses = zillow.get_home_addresses_trulia("warren")

# for index, row in bergen_home_addresses.iterrows():
#     zillow.property_deep_search(row['street'], row['city']+", NJ", "bergen" )
    

# for index, row in essex_home_addresses.iterrows():
#     zillow.property_deep_search(row['street'], row['city']+", NJ", "essex" )


# for index, row in hudson_home_addresses.iterrows():
#     zillow.property_deep_search(row['street'], row['city']+", NJ", "hudson" )

# for index, row in morris_home_addresses.iterrows():
#     zillow.property_deep_search(row['street'], row['city']+", NJ", "morris" )

# for index, row in passaic_home_addresses.iterrows():
#     zillow.property_deep_search(row['street'], row['city']+", NJ", "passaic" )

# for index, row in union_home_addresses.iterrows():
#     zillow.property_deep_search(row['street'], row['city']+", NJ", "union" )

# for index, row in warren_home_addresses.iterrows():
#     zillow.property_deep_search(row['street'], row['city']+", NJ", "warren" )
