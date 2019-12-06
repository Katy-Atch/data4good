import requests
import enum
import sys
from datetime import datetime
from django.core.management.base import BaseCommand
sys.path.append("/code/pages/management/commands")
from mapping import *
from pages.models import Site, CE, GEO
from geocode import create_geocode_object, geocode_address


class Program(enum.Enum):
    SFSP = 1
    SSO = 2


class Entity(enum.Enum):
    CE = 1
    Site = 2


def get_if_available(key, row):
    if key in row:
        return row[key]
    else:
        return None


def get_lat(key, row):
    if key in row:
        return row[key]['coordinates'][1]
    else:
        return None


def get_long(key, row):
    if key in row:
        return row[key]['coordinates'][0]
    else:
        return None


def save_entity(program, entity, row, geo_id):
    attribute_list = get_attribute_list(program, entity)
    new_object = None

    if entity == Entity.CE:
        new_object = CE()
    elif entity == Entity.Site:
        new_object = Site()

    for db_attr, portal_attr in attribute_list.items():
        setattr(new_object, db_attr, str(get_if_available(portal_attr, row)))

    setattr(new_object, "last_updated", datetime.now())
    setattr(new_object, "geo_id", geo_id)

    new_object.save()


# Gets the mapping of portal name : database name for an entity based
# on what type of entity (Site, CE) and the program (SSO, SFSP)
def get_attribute_list(program, entity):
    if program == Program.SSO:
        if entity == Entity.CE:
            return {**ce_mapping, **sso_ce_mapping}
        elif entity == Entity.Site:
            return {**site_mapping, **sso_site_mapping}
    elif program == Program.SFSP:
        if entity == Entity.CE:
            return ce_mapping
        elif entity == Entity.Site:
            return {**site_mapping, **sfsp_site_mapping}


# Checks if an old entity and new entity have the same values for all attributes
def attributes_match(attribute_list, new_entity, old_entity):
    for db_attr, portal_attr in attribute_list.items():
        new_attr = get_if_available(portal_attr, new_entity)
        old_attr = getattr(old_entity, db_attr)
        if isinstance(old_attr, int):
            new_attr = int(new_attr)

        if new_attr is None:
            new_attr = "None"

        if new_attr != old_attr:
            return False
    return True


# Need to add another condition for if there are more than one entities- error
# Need to only check a CE in the portal one time
def update_database(json_data, program):
    for row in json_data:
        new_ce_id = get_if_available('ceid', row)
        new_site_id = get_if_available('siteid', row)
        for typename, entity_model, extra_filter, entity_type in [(new_site_id, Site, {'site_id': new_site_id}, Entity.Site), (new_ce_id, CE, {}, Entity.CE)]:
            if typename is not None:
                existing = entity_model.objects.filter(ce_id=new_ce_id, most_current_record=True, **extra_filter)
                if existing.count() == 1:
                    old = existing.first()
                    if not attributes_match(get_attribute_list(program, entity_type), row, old):

                        geo_id = None
                        # Compares location details of old row and new row. 
                        if compare_location_details(old, row):
                            geo_id = old.geo_id
                        else:
                            geo_id = does_geocode_exist(row.street_address1, row.street_address2, 
                            row.street_city, row.street_state, row.street_zip)

                        # Need to do checks based on name & address
                        old.most_current_record = False
                        old.save()
                        save_entity(program, entity_type, row, geo_id)
                else:
                    # Not in database- create new object with most_current_record=True
                    geo_id = does_geocode_exist(row.street_address1, row.street_address2, 
                            row.street_city, row.street_state, row.street_zip)
                    save_entity(program, entity_type, row, geo_id)
                
    geocode_lat_long()      

def populate():
    app_token = 'EHZP1uaN4Sx0pg0cxnbLdRvQU'
    headers = {'X-App-Token': app_token}
    max_records = 50000
    sso_portal = "3hpz-ajxk"
    sfsp_portal = "rmea-7b2m"

    for portal_id, entity_type in [(sso_portal, Program.SSO), (sfsp_portal, Program.SFSP)]:
        response = requests.get(
            'https://data.texas.gov/resource/' + portal_id + '.json?',
            params={'$limit': max_records},
            headers=headers
        )
        
        data = response.json()
        update_database(data, entity_type)

    return None

# Loops through each item in the GEO table which needs geocoding and geocodes/saves the object
def geocode_lat_long():
    for item in GEO.objects.filter(latitude=None, longitude=None):
        geocode_address(item.geo_id, item.street_address1, item.street_address2, 
        item.street_city, item.street_state, item.street_zip)

# Checks if geocode with given location details exists. If so, return the associated geo_id. If not,
# Create new GEO object with given location details, and return its geo_id
def does_geocode_exist(street_address1, street_address2, street_city, street_state, street_zip):
    existing = GEO.objects.filter(street_address1=street_address1, street_address2=street_address2,
                                  street_city=street_city, street_state=street_state, street_zip=street_zip)
    
    if existing.count() == 1:
        return existing.first().geo_id
    else:
        return create_geocode_object(street_address1, street_address2, 
                            street_city, street_state, street_zip, None, None)
    

# Checks if the location details of the old and new objects are the same. Returns true if they are
# and false if they are different            
def compare_location_details(old_object, new_object):
    return (old_object.street_address1 == new_object.street_address1 and
            old_object.street_address2 == new_object.street_address2 and
            old_object.street_city == new_object.street_city and
            old_object.street_zip == new_object.street_zip and
            old_object.street_state == new_object.street_state)

class Command(BaseCommand):
    help = "Populates the database"

    def handle(self, *args, **options):
        populate() 
