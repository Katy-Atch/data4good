import requests
from pages.models import Site, GEO
from random import randint
from django.core.management.base import BaseCommand
import sys
sys.path.append("/code/pages/management/commands")
from mapping import Mapping, GeoAttributes

LATITUDE = 0
LONGITUDE = 1
BingMapsAPIKey = 'Ao5wMyg0cjJUxELJFM2NpmRaX9zWtatIPpDW01SprBbnJofurOjUL3dSV1p3o82c'

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

    r = requests.get(
        'http://dev.virtualearth.net/REST/v1/Locations',
        params={'q': street_address1 + ' ' + str(street_address2) + ' ' + street_city + ' ' + street_state + ' ' + str(street_zip),
                'key': BingMapsAPIKey})
    data = r.json()

    latitude = 0
    longitude = 0
    # Will be changed to false if an error occurs during geocoding
    valid_coordinates = True


    try:
        # Checking if there exists a lat/long for the given location
        if data['resourceSets'][0]['estimatedTotal'] > 0:
            # Extract point representing coordinates
            coordinates = data['resourceSets'][0]['resources'][0]['point']['coordinates']
            latitude = coordinates[LATITUDE]
            longitude = coordinates[LONGITUDE]
    except:
        # If an error occurred during geocoding, change  valid_coordinates 
        # field of geo object to False
        valid_coordinates = False


    geo_object = GEO.objects.filter(geo_id=geo_id).first()
    geo_object.latitude = latitude
    geo_object.longitude = longitude
    geo_object.valid_coordinates = valid_coordinates
    geo_object.save()


def create_geocode_object(street_address1, street_address2, street_city, street_state, 
                          street_zip,latitude, longitude):
    new_geo_object = GEO()
    assign_geo_values(new_geo_object, street_address1, 
    street_address2, street_city, street_state, 
                          street_zip,latitude, longitude)

    new_geo_object.save()
    return new_geo_object.geo_id




def assign_geo_values(new_geo_object, street_address1, 
    street_address2, street_city, street_state, 
                          street_zip,latitude, longitude):
    # TODO: Find more elegant way to do this
    new_geo_object.street_address1 = street_address1
    new_geo_object.street_address2 = street_address2
    new_geo_object.street_city = street_city
    new_geo_object.street_state = street_state
    new_geo_object.street_zip = street_zip 
    new_geo_object.latitude = latitude
    new_geo_object.longitude = longitude

class Command(BaseCommand):
    help = "Geocodes addresses"
    
    def handle(self, *args, **options):
        # geo_objects = [{'geo_id': 0,
        # 'street_address1': '2733 Rosedale ave', 
        # 'street_address2': '',
        # 'street_city': 'Dallas',
        # 'street_state': 'TX',
        # 'street_zip': 75205,
        # 'latitude': 0,
        # 'longitude': 0}]
        # batch_geocode(geo_objects)
        geocode_address(0, '2733 Rosedale Ave', '', 'Dallas', 'TX', 75205)


# def batch_geocode(geo_objects):
#     data = create_geocode_input_data(geo_objects)
#     create_job = requests.post(url='http://spatial.virtualearth.net/REST/v1/Dataflows/Geocode',
#                     data=data, params={'input': 'pipe', 'output': 'json','key': BingMapsAPIKey})
#     job_response = create_job.json()
#     print('hey')

# def create_geocode_input_data(geo_objects):
#     data = 'Bing Spatial Data Services, 2.0\n'
#     data += 'Id| GeocodeRequest/Address/AddressLine| GeocodeRequest/Address/Locality| GeocodeRequest/Address/AdminDistrict| GeocodeRequest/Address/PostalCode| GeocodeResponse/Point/Latitude| GeocodeResponse/Point/Longitude\n'
#     for geo_object in geo_objects:
#         data += str(geo_object['geo_id']) + '| '
#         for location_attribute in GeoAttributes.location_attributes:
#             # data += getattr(geo_object, location_attribute)
#             data += str(geo_object[location_attribute])
#             if location_attribute == 'street_address1':
#                 data += ' '
#             else:
#                 data += '| '
#         data += '0|0'
#     return data