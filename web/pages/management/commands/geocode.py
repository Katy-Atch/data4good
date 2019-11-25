import requests
from pages.models import Site, GEO
from random import randint
from pages.management.commands.mapping import geo_attributes

LATITUDE = 0
LONGITUDE = 1

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

    BingMapsAPIKey = 'Ao5wMyg0cjJUxELJFM2NpmRaX9zWtatIPpDW01SprBbnJofurOjUL3dSV1p3o82c'
    URL = "http://dev.virtualearth.net/REST/v1/Locations?q={street_address1}%20{street_address2}%20{street_city}%20{street_state}%20{street_zip}&key={BingMapsAPIKey}"
    r = requests.get(URL)
    data = r.json()

    coordinates = data['resourceSets']['resources']['point']['coordinates']
    latitude = coordinates[LATITUDE]
    longitude = coordinates[LONGITUDE]
    # TODO: create elegant method of creating geo_id
    geo_id = randint(0,10)

    create_geocode_object(geo_id, street_address1, street_address2, street_city, street_state, street_zip,
                          latitude, longitude)
    
    return geo_id


def create_geocode_object(geo_id, street_address1, street_address2, street_city, street_state, 
                          street_zip,latitude, longitude):
    new_object = GEO()
    variables = locals()
    for key, value in variables:
        if key in geo_attributes:
            new_object.key = value

    new_object.save()
