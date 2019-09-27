import requests
from django.core.management.base import BaseCommand
from pages.models import Site, CE
from django.db import connection
from django.core.management import call_command

def db_table_exists(table_name):
    return table_name in connection.introspection.table_names()

def get_if_available(key, dict):
    if key in dict:
        return dict[key]
    else:
        return None

def get_lat(key, dict):
    if key in dict:
        return dict[key]['coordinates'][1]
    else:
        return None

def get_long(key, dict):
    if key in dict:
        return dict[key]['coordinates'][0]
    else:
        return None

def Populate():
    APP_TOKEN = 'EHZP1uaN4Sx0pg0cxnbLdRvQU'

    headers = {'X-App-Token': APP_TOKEN}

    # LOOP
    # read data from API
    # parse json data into model instance
    # save model instance
    # END LOOP

    MAX_RECORDS = 50000

    # 2019 -> 2018 -> 2017 -> 2016
    # sso_portals = ["3hpz-ajxk", "93u6-myq9", "sjdu-n9ry", "y3zg-2gdi"]
    # sfsp_portals = ["rmea-7b2m", "myag-hymh", "wui5-2b5", "cbxb-6zrb"]
    sso_portals = ["3hpz-ajxk"]
    sfsp_portals = ["rmea-7b2m"]

    # Clear out anything in the database
    if db_table_exists('pages_ce') :
        CE.objects.all().delete()
    else :
        call_command('migrate')
    if db_table_exists('pages_site') :
        Site.objects.all().delete()
    else :
        call_command('migrate')

    for identifier in sso_portals:
        response = requests.get('https://data.texas.gov/resource/' + identifier + '.json?$limit=' + str(MAX_RECORDS),
            headers=headers)

        data = response.json()

        for x in range(len(data)):
            sponsor = CE(
                # TODO: Need to go through all other records and set most_current_record to false
                # Default is most_current_record = True
                # last_updated is set to now by default
                program_year = get_if_available('programyear', data[x]),
                ce_id = get_if_available('ceid', data[x]),
                name = get_if_available('cename', data[x]),
                county = get_if_available('cecounty', data[x]),
                type_of_agency = get_if_available('typeofagency', data[x]),
                county_district_code = get_if_available('countydistrictcode', data[x]),
                esc = get_if_available('esc', data[x]),
                tda_region = get_if_available('tdaregion', data[x]),
                street_address1 = get_if_available('cestreetaddressline1', data[x]),
                street_address2 = get_if_available('cestreetaddressline2', data[x]),
                street_city = get_if_available('cestreetaddresscity', data[x]),
                street_state = get_if_available('cestreetaddressstate', data[x]),
                street_zip = get_if_available('cestreetaddresszipcode', data[x]),

                mailing_address1 = get_if_available('cemailingaddressline1', data[x]),
                mailing_address2 = get_if_available('cemailingaddressline2', data[x]),
                mailing_city = get_if_available('cemailingaddresscity', data[x]),
                mailing_state = get_if_available('cemailingaddressstate', data[x]),
                mailing_zip = get_if_available('cemailingaddresszipcode', data[x]),

                superintendent_salutation = get_if_available('superintendentsalutation', data[x]),
                superintendent_first_name = get_if_available('superintendentfirstname', data[x]),
                superintendent_last_name = get_if_available('superintendentlastname', data[x]),
                superintendent_title_position = get_if_available('superintendenttitleposition', data[x]),
                superintendent_email = get_if_available('superintendentemail', data[x]),
                superintendent_phone = get_if_available('superintendentphone', data[x]),

                childnutdir_salutation = get_if_available('childnutdirsalutation', data[x]),
                childnutdir_first_name = get_if_available('childnutdirfirstname', data[x]),
                childnutdir_last_name = get_if_available('childnutdirlastname', data[x]),
                childnutdir_title_position = get_if_available('childnutdirtitleposition', data[x]),
                childnutdir_email = get_if_available('childnutdiremail', data[x]),
                childnutdir_phone = get_if_available('childnutdirphone', data[x]),

                # Can't get this from API
                # latitude = data[x][''],
                # longitude = data[x][''],
            )
            sponsor.save()

            site = Site(
                # TODO: Need to go through all other records and set most_current_record to false
                # Default is most_current_record = True
                # last_updated is set to now by default
                program_year = get_if_available('programyear', data[x]),
                sso_or_sfsp = Site.SSO,
                site_id = get_if_available('siteid', data[x]),
                ce_id = get_if_available('ceid', data[x]),
                type_of_snp_org = get_if_available('typeofsnporg', data[x]),
                name = get_if_available('sitename', data[x]),
                county = get_if_available('sitecounty', data[x]),
                sso_site_type = get_if_available('sitetype', data[x]),
                street_address1 = get_if_available('sitestreetaddressline1', data[x]),
                street_address2 = get_if_available('sitestreetaddressline2', data[x]),
                street_city = get_if_available('sitestreetcity', data[x]),
                street_state = get_if_available('sitestreetstate', data[x]),
                street_zip = get_if_available('sitestreetzipcode', data[x]),

                program_contact_salutation = get_if_available('seamlesssummercontactsal', data[x]),
                program_contact_first_name = get_if_available('seamlesssummercontactfirstname', data[x]),
                program_contact_last_name = get_if_available('seamlesssummercontactlastname', data[x]),
                program_contact_title_position = get_if_available('seamlesssummercontacttit', data[x]),
                program_contact_email = get_if_available('seamlesssummercontactemail', data[x]),
                program_contact_phone = get_if_available('seamlesssummercontactphone', data[x]),

                start_date = get_if_available('sitestartdate', data[x]),
                end_date = get_if_available('siteenddate', data[x]),
                days_of_operation = get_if_available('days_of_operation', data[x]),
                meal_types_served = get_if_available('meal_types_served', data[x]),

                latitude = get_lat('geocoded_column', data[x]),
                longitude = get_long('geocoded_column', data[x]),

            )
            site.save()



    for identifier in sfsp_portals:
        response = requests.get('https://data.texas.gov/resource/' + identifier + '.json?$limit=' + str(MAX_RECORDS),
            headers=headers)

        data = response.json()

        for x in range(len(data)):
            sponsor = CE(
                # TODO: Need to go through all other records and set most_current_record to false
                # Default is most_current_record = True
                # last_updated is set to now by default
                program_year = get_if_available('programyear', data[x]),
                ce_id = get_if_available('ceid', data[x]),
                name = get_if_available('cename', data[x]),
                county = get_if_available('cecounty', data[x]),
                type_of_agency = get_if_available('typeofagency', data[x]),
                county_district_code = get_if_available('countydistrictcode', data[x]),
                esc = get_if_available('esc', data[x]),
                tda_region = get_if_available('tdaregion', data[x]),
                street_address1 = get_if_available('cestreetaddressline1', data[x]),
                street_address2 = get_if_available('cestreetaddressline2', data[x]),
                street_city = get_if_available('cestreetaddresscity', data[x]),
                street_state = get_if_available('cestreetaddressstate', data[x]),
                street_zip = get_if_available('cestreetaddresszipcode', data[x]),

                mailing_address1 = get_if_available('cemailingaddressline1', data[x]),
                mailing_address2 = get_if_available('cemailingaddressline2', data[x]),
                mailing_city = get_if_available('cemailingaddresscity', data[x]),
                mailing_state = get_if_available('cemailingaddressstate', data[x]),
                mailing_zip = get_if_available('cemailingaddresszipcode', data[x]),
                # Can't get this from API
                # latitude = data[x][''],
                # longitude = data[x][''],
            )
            sponsor.save()

            site = Site(
                # TODO: Need to go through all other records and set most_current_record to false
                # Default is most_current_record = True
                # last_updated is set to now by default
                program_year = get_if_available('programyear', data[x]),
                sso_or_sfsp = Site.SFSP,
                site_id = get_if_available('siteid', data[x]), #
                ce_id = get_if_available('ceid', data[x]),
                type_of_sfsp_org = get_if_available('typeofsfsporg', data[x]),
                name = get_if_available('sitename', data[x]),
                county = get_if_available('sitecounty', data[x]),
                rural_or_urban_code = get_if_available('ruralorurbancode', data[x]), 
                sfsp_site_type = get_if_available('sitetype', data[x]),
                street_address1 = get_if_available('sitestreetaddressline1', data[x]),
                street_address2 = get_if_available('sitestreetaddressline2', data[x]),
                street_city = get_if_available('sitestreetaddresscity', data[x]),
                street_state = get_if_available('sitestreetaddressstate', data[x]),
                street_zip = get_if_available('sitestreetaddresszipcode', data[x]),

                mailing_address1 =  get_if_available('sitemailingaddressline1', data[x]),
                mailing_address2 =  get_if_available('sitemailingaddressline2', data[x]),
                mailing_city =  get_if_available('sitemailingaddresscity', data[x]),
                mailing_state =  get_if_available('sitemailingaddressstate', data[x]),
                mailing_zip =  get_if_available('sitemailingaddresszipcode', data[x]),

                program_contact_salutation = get_if_available('sfspcontactsalutation', data[x]),
                program_contact_first_name = get_if_available('sfspcontactfirstname', data[x]),
                program_contact_last_name = get_if_available('sfspcontactlastname', data[x]),
                program_contact_title_position = get_if_available('sfspcontacttitleposition', data[x]),
                program_contact_email = get_if_available('sfspcontactemail', data[x]),
                program_contact_phone = get_if_available('sfspcontactphone', data[x]),

                site_supervisor_salutation =  get_if_available('sitesupervisorsalutation', data[x]),
                site_supervisor_first_name =  get_if_available('sitesupervisorfirstname', data[x]),
                site_supervisor_last_name =  get_if_available('sitesupervisorlastname', data[x]),
                site_supervisor_title_position =  get_if_available('sitesupervisortitleposition', data[x]),
                site_supervisor_email =  get_if_available('sitesupervisoremail', data[x]),
                site_supervisor_phone =  get_if_available('sitesupervisorphone', data[x]),

                start_date = get_if_available('sitestartdate', data[x]),
                end_date = get_if_available('siteenddate', data[x]),
                days_of_operation = get_if_available('daysofoperation', data[x]),
                meal_types_served = get_if_available('mealtypesserved', data[x]),
                
                latitude = get_lat('geocoded_column', data[x]),
                longitude = get_long('geocoded_column', data[x]),

                primary_auth_rep_salutation = get_if_available('primaryauthorizedreprese', data[x]),
                primary_auth_rep_first_name = get_if_available('primaryauthorizedreprese_1', data[x]),
                primary_auth_rep_last_name = get_if_available('primaryauthorizedreprese_2', data[x]),
                primary_auth_rep_title_position = get_if_available('primaryauthorizedreprese_3', data[x]),
                primary_auth_rep_email = get_if_available('primaryauthorizedreprese_4', data[x]),
                primary_auth_rep_phone = get_if_available('primaryauthorizedreprese_5', data[x]),
            )
            if site.latitude == null or site.longitude == null:
                BingMapsApiKey = "Ao5wMyg0cjJUxELJFM2NpmRaX9zWtatIPpDW01SprBbnJofurOjUL3dSV1p3o82c"
                locationQuery = site.street_address1 + site.streetAddress2
                geoResponse = requests.get('http://dev.virtualearth.net/REST/v1/Locations?query=' + locationQuery + '&key=' + BingMapsApiKey)
                geoData = geoResponse.json()
                
            site.save()

    return None

class Command(BaseCommand):
    help = "Populates the database"

    def handle(self, *args, **options):
        Populate()




