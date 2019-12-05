import requests
import enum
import sys
from datetime import datetime
from django.core.management.base import BaseCommand
sys.path.append("/code/pages/management/commands")
from mapping import *
from pages.models import Site, CE


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


def save_entity(program, entity, row):
    attribute_list = get_attribute_list(program, entity)
    new_object = None

    if entity == Entity.CE:
        new_object = CE()
    elif entity == Entity.Site:
        new_object = Site()

    for db_attr, portal_attr in attribute_list.items():
        setattr(new_object, db_attr, str(get_if_available(portal_attr, row)))

    setattr(new_object, "last_updated", datetime.now())

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
                        # TODO: Add check for if location info is the same. If not,
                        # create_geocode_object() with lat/long NULL
                        #  
                        # Need to do checks based on name & address
                        old.most_current_record = False
                        old.save()
                        save_entity(program, entity_type, row)
                else:
                    # Not in database- create new object with most_current_record=True
                    save_entity(program, entity_type, row)
                    # TODO: create_geocode_object() with lat/long NULL
                
    geocode_lat_long()      

def populate():
    app_token = 'EHZP1uaN4Sx0pg0cxnbLdRvQU'
    headers = {'X-App-Token': app_token}
    max_records = 50000
    sso_portal = "3hpz-ajxk"
    sfsp_portal = "rmea-7b2m"

    for portal_id, entity_type in [(sso_portal, Program.SSO), (sfsp_portal, Program.SFSP)]:
        response = requests.get(
            'https://data.texas.gov/resource/' + portal_id + '.json',
            params={'limit': str(max_records)},
            headers=headers
        )
        data = response.json()
        update_database(data, entity_type)

    return None

def geocode_lat_long():
    # For object in GEO
    # Check if lat/long is NULL
    # If so, geocode_address with object's location info
    return 0


class Command(BaseCommand):
    help = "Populates the database"

    def handle(self, *args, **options):
        populate() 
