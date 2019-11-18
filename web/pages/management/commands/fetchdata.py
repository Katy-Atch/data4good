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


def create_entity(program, entity, row):
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
def check_attributes(attribute_list, new_entity, old_entity):
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
def parse_json(json_data, program):
    for x in range(len(json_data)):
        new_ce_id = get_if_available('ceid', json_data[x])
        if new_ce_id is not None:
            existing_ce = CE.objects.filter(ce_id=new_ce_id, most_current_record=True)
            if existing_ce.count() == 1:
                old_ce = existing_ce.first()
                # Check that all attributes match
                if not check_attributes(get_attribute_list(program, Entity.CE), json_data[x], old_ce):
                    # Set most_current_record=False on old object
                    old_ce.most_current_record = False
                    old_ce.save()
                    create_entity(program, Entity.CE, json_data[x])
            else:
                # Not in database- create new object with most_current_record=True
                create_entity(program, Entity.CE, json_data[x])

        new_site_id = get_if_available('siteid', json_data[x])
        if new_site_id is not None:
            existing_site = Site.objects.filter(ce_id=new_ce_id, site_id=new_site_id, most_current_record=True)
            if len(existing_site) == 1:
                # Need better function for comparing names and addresses so that the strings are stripped of whitespace
                # and punctuation
                old_site = existing_site.first()
                if not check_attributes(get_attribute_list(program, Entity.Site), json_data[x], old_site):
                    if not (old_site.name == get_if_available('name', json_data[x]) or
                            old_site.street_address1 == get_if_available('sitestreetaddressline1', json_data[x])):
                        # Different site- create new object, set most_current_object of old object to False
                        old_site.most_current_record = False
                        old_site.save()
                        create_entity(program, Entity.Site, json_data[x])
            else:
                create_entity(program, Entity.Site, json_data[x])
                # Check for address with different side id but same name and address


def populate():
    app_token = 'EHZP1uaN4Sx0pg0cxnbLdRvQU'
    headers = {'X-App-Token': app_token}
    max_records = 50000
    sso_portal = "93u6-myq9k"
    sfsp_portal = "myag-hymh"

    # GET SSO DATA
    response = requests.get('https://data.texas.gov/resource/' + sso_portal + '.json?$limit=' + str(max_records),
                            headers=headers)
    sso_data = response.json()
    parse_json(sso_data, Program.SSO)

    # GET SFSP DATA
    response = requests.get('https://data.texas.gov/resource/' + sfsp_portal + '.json?$limit=' + str(max_records),
                            headers=headers)
    sfsp_data = response.json()
    parse_json(sfsp_data, Program.SFSP)

    return None


class Command(BaseCommand):
    help = "Populates the database"

    def handle(self, *args, **options):
        populate() 
