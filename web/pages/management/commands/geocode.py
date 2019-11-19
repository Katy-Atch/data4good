import requests

# Control flow of the script

# This script will be run in the fetchdata.py script. Two ways it can go are:
# 1.) fetchdata retrieves records one by one, and if it finds a record that is
#     not geocoded, it will not put it in the database but instead will add all 
#     of its information to a dictionary and will add its address to the .csv
#     file. This script will be run at the end of fetchdata, and the records will
#     be read from the file one by one as the records are read from the dictionary
#     concurrently, and only after the geocoding will these records be put in the
#     database. Problems- have to ensure the dictionary and the records in the csv
#     line up. Probably not best solution
# 2.) fetchdata retrieves records one by one, and when it finds a sponsor or site
#     that has no coordinates, it still creates the entity but also adds the address
#     of the entity to the file. After fetchdata has retrieved and stored every record,
#     this script is run, and then fetchdata will go on to update all of the records
#     by matching up the addresses
# 3.) Instead of batch geocoding, as fetchdata retrieves records, if it finds one that
#     has no geolocation, it immediately makes a call to the endpoint to geocode it
#     and then stores the record after geocoding the address

def geocode_address(street_address1, street_address2, street_city, street_state, street_zip):
    #Construct query then parse returned json. Next, enter into the database

def add_to_geocode_db(latitude, longitude):
    