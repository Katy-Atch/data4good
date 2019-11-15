import requests
import enum
import sys
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

    for portal_attr, db_attr in attribute_list.items():
        setattr(new_object, db_attr, get_if_available(portal_attr, row))

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
    for attribute in attribute_list:
        if get_if_available(attribute, new_entity) != get_if_available(attribute, old_entity):
            return False
    return True


# Need to add another condition for if there are more than one entities- error
# Need to only check a CE in the portal one time
def parse_json(json_data, program):
    for x in range(len(json_data)):
        new_ce_id = get_if_available('ceid', json_data[x])
        if new_ce_id is not None:
            existing_ce = CE.objects.filter(ce_id=new_ce_id, most_current_record=True)
            if len(existing_ce) == 1:
                # Check that all attributes match
                if not check_attributes(get_attribute_list(program, Entity.CE), json_data[x], existing_ce):
                    # Set most_current_record=False on old object
                    existing_ce.most_current_record = False
                    existing_ce.save()
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
                if not check_attributes(get_attribute_list(program, Entity.Site), json_data[x], existing_site):
                    if not (existing_site.name == get_if_available('name', json_data[x]) or
                            existing_site.street_address1 == get_if_available('sitestreetaddressline1', json_data[x])):
                        # Different site- create new object, set most_current_object of old object to False
                        existing_site.most_current_record = False
                        existing_site.save()
                        create_entity(program, Entity.Site, json_data[x])
            else:
                create_entity(program, Entity.Site, json_data[x])


def populate():
    app_token = 'EHZP1uaN4Sx0pg0cxnbLdRvQU'
    headers = {'X-App-Token': app_token}
    max_records = 50000
    sso_portal = "3hpz-ajxk"
    sfsp_portal = "rmea-7b2m"

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
