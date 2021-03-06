import requests
import enum
import sys
from datetime import datetime
from django.core.management.base import BaseCommand
sys.path.append("/code/pages/management/commands")
from mapping import Mapping, GeoAttributes
from pages.models import Site, CE, GEO
from geocode import create_geocode_object, geocode_address, geocode_lat_long

seen_ce_list = set()

class Program(enum.Enum):
    SFSP = 1
    SSO = 2


class Entity(enum.Enum):
    CE = 1
    Site = 2


def get_from_row(key, row):
    if key in row:
        return row[key]
    else:
        return None


def get_mapped_attr(key_dict, key, row):
    attribute = key_dict[key]
    return get_from_row(attribute, row)


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
    key_dict = get_key_dict(program, entity)
    new_object = None

    if entity == Entity.CE:
        new_object = CE()
    elif entity == Entity.Site:
        new_object = Site()

    for db_attr, portal_attr in key_dict.items():
        setattr(new_object, db_attr, str(get_from_row(portal_attr, row)))

    setattr(new_object, "last_updated", datetime.now())
    setattr(new_object, "geo_id", geo_id)

    if program==Program.SFSP:
        setattr(new_object, "sso_or_sfsp", "SFSP")
    elif program==Program.SSO:
        setattr(new_object, "sso_or_sfsp", "SSO")

    new_object.save()


# Gets the mapping of portal name : database name for an entity based
# on what type of entity (Site, CE) and the program (SSO, SFSP)
def get_key_dict(program, entity):
    if program == Program.SSO:
        if entity == Entity.CE:
            return {**Mapping.ce_mapping, **Mapping.sso_ce_mapping}
        elif entity == Entity.Site:
            return {**Mapping.site_mapping, **Mapping.sso_site_mapping}
    elif program == Program.SFSP:
        if entity == Entity.CE:
            return Mapping.ce_mapping
        elif entity == Entity.Site:
            return {**Mapping.site_mapping, **Mapping.sfsp_site_mapping}


# Checks if an old entity and new entity have the same values for all attributes
def attributes_match(key_dict, new_entity, old_entity):
    for db_attr, portal_attr in key_dict.items():
        new_attr = get_from_row(portal_attr, new_entity)
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
def update_database(json_data, program_type):
    for row in json_data:
        seen = False

        new_site_id = get_from_row('siteid', row)
        new_ce_id = get_from_row('ceid', row)
        if new_ce_id not in seen_ce_list:
            seen_ce_list.add(new_ce_id)
        else:
            seen = True
        
        for typename, entity_model, extra_filter, entity_type in [(new_site_id, Site, {'site_id': new_site_id}, Entity.Site), (new_ce_id, CE, {}, Entity.CE)]:
            if typename is not None:
                if (entity_type == Entity.Site) or (entity_type == Entity.CE and not seen):
                    existing = entity_model.objects.filter(ce_id=new_ce_id, most_current_record=True, **extra_filter)
                    key_dict = get_key_dict(program_type, entity_type)
                    if existing.count() == 1:
                        old = existing.first()
                        if not attributes_match(get_key_dict(program_type, entity_type), row, old):

                            geo_id = None
                            # Compares location details of old row and new row. 
                            if compare_location_details(old, row, key_dict):
                                geo_id = old.geo_id
                            else:
                                # TODO: Find more elegant way to call these attributes
                                geo_id = does_geocode_exist(get_mapped_attr(key_dict,'street_address1', row), get_mapped_attr(key_dict,'street_address2', row), 
                                get_mapped_attr(key_dict,'street_city', row), get_mapped_attr(key_dict,'street_state', row), get_mapped_attr(key_dict,'street_zip', row))

                            # Need to do checks based on name & address
                            old.most_current_record = False
                            old.save()
                            save_entity(program_type, entity_type, row, geo_id)
                    else:
                        # Not in database- create new object with most_current_record=True
                        geo_id = does_geocode_exist(get_mapped_attr(key_dict, 'street_address1', row), get_mapped_attr(key_dict,'street_address2', row), 
                                get_mapped_attr(key_dict,'street_city', row), get_mapped_attr(key_dict,'street_state', row), get_mapped_attr(key_dict,'street_zip', row))
                        save_entity(program_type, entity_type, row, geo_id)
                
    # After checking rows, geocode rows with null lat/long
    geocode_lat_long()      

def populate():
    app_token = 'EHZP1uaN4Sx0pg0cxnbLdRvQU'
    headers = {'X-App-Token': app_token}
    max_records = 10
    sso_portal = "3hpz-ajxk"
    sfsp_portal = "rmea-7b2m"

    for portal_id, entity_type in [(sso_portal, Program.SSO), (sfsp_portal, Program.SFSP)]:
        response = requests.get(
            'https://data.texas.gov/resource/' + portal_id + '.json',
            params={'$limit': max_records},
            headers=headers
        )
        
        data = response.json()
        update_database(data, entity_type)

    return None

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
def compare_location_details(old_object, row, key_dict):
    
    for attribute in GeoAttributes.location_attributes:
        if getattr(old_object, attribute) != get_mapped_attr(key_dict, attribute, row):
            return False

    return True

class Command(BaseCommand):
    help = "Populates the database"

    def handle(self, *args, **options):
        populate() 
