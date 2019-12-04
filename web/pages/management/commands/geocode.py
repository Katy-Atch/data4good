import requests
from pages.models import Site, GEO
from random import randint
from django.core.management.base import BaseCommand
import sys
sys.path.append("/code/pages/management/commands")
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

def geocode_address(geo_id, street_address1, street_address2, street_city, street_state, street_zip):

    BingMapsAPIKey = 'Ao5wMyg0cjJUxELJFM2NpmRaX9zWtatIPpDW01SprBbnJofurOjUL3dSV1p3o82c'
    URL = 'http://dev.virtualearth.net/REST/v1/Locations?q={0}%20{1}%20{2}%20{3}%20{4}&key={5}'.format(street_address1, 
    street_address2, street_city, street_state, street_zip, BingMapsAPIKey)
    r = requests.get(URL)
    data = r.json()

    coordinates = data['resourceSets'][0]['resources'][0]['point']['coordinates']
    latitude = coordinates[LATITUDE]
    longitude = coordinates[LONGITUDE]

    geo_object = GEO.objects.filter(geo_id=geo_id).first()
    geo_object.latitude = latitude
    geo_object.longitude = longitude
    

def create_geocode_object(geo_id, street_address1, street_address2, street_city, street_state, 
                          street_zip,latitude, longitude):
    new_geo_object = GEO()
    assign_geo_values(new_geo_object, geo_id, street_address1, 
    street_address2, street_city, street_state, 
                          street_zip,latitude, longitude)

    new_geo_object.save()

def create_geo_id():
    # Replace with geo_id algorithm
    return 0

def assign_geo_values(new_geo_object, geo_id, street_address1, 
    street_address2, street_city, street_state, 
                          street_zip,latitude, longitude):
    new_geo_object.geo_id = geo_id
    new_geo_object.street_address1 = street_address1
    new_geo_object.street_address2 = street_address2
    new_geo_object.street_city = street_city
    new_geo_object.street_state
    new_geo_object.street_zip = street_zip 
    new_geo_object.latitude = latitude
    new_geo_object.longitude = longitude

class Command(BaseCommand):
    help = "Geocodes addresses"

    def handle(self, *args, **options):
        geocode_address('2733 Rosedale Ave', '', 'Dallas', 'TX', 75205)
