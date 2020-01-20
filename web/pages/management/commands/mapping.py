class Mapping:
    site_mapping = {
        "program_year": "programyear",
        "site_id": "siteid",
        "ce_id": "ceid",
        "name": "sitename",
        "county": "sitecounty",
        "street_address1": "sitestreetaddressline1",
        "street_address2": "sitestreetaddressline2",
        "start_date": "sitestartdate",
        "end_date": "siteenddate",
        "breakfast_time": "breakfasttime",
        "breakfast_days_served": "breakfastdaysserved",
        "amsnack_time": "amsnacktime",
        "amsnack_days_served": "amsnackdaysserved",
        "lunch_time": "lunchtime",
        "lunch_days_served": "lunchdaysserved",
        "pmsnack_time": "pmsnacktime",
        "pmsnack_days_served": "pmsnackdaysserved",
        "supper_time": "suppertime",
        "supper_days_served": "supperdaysserved",
    }

    sso_site_mapping = {
        "type_of_snp_org": "typeofsnporg",
        "sso_site_type": "sitetype",
        "street_city": "sitestreetcity",
        "street_state": "sitestreetstate",
        "street_zip": "sitestreetzipcode",
        "program_contact_salutation": "seamlesssummercontactsal",
        "program_contact_first_name": "seamlesssummercontactfirstname",
        "program_contact_last_name": "seamlesssummercontactlastname",
        "program_contact_title_position": "seamlesssummercontacttit",
        "program_contact_email": "seamlesssummercontactemail",
        "program_contact_phone": "seamlesssummercontactphone",
        "days_of_operation": "days_of_operation",
        "meal_types_served": "meal_types_served"
    }

    sfsp_site_mapping = {
        "type_of_sfsp_org": "typeofsfsporg",
        "rural_or_urban_code": "ruralorurbancode",
        "sfsp_site_type": "sitetype",
        "street_city": "sitestreetaddresscity",
        "street_state": "sitestreetaddressstate",
        "street_zip": "sitestreetaddresszipcode",
        "program_contact_salutation": "sfspcontactsalutation",
        "program_contact_first_name": "sfspcontactfirstname",
        "program_contact_last_name": "sfspcontactlastname",
        "program_contact_title_position": "sfspcontacttitleposition",
        "program_contact_email": "sfspcontactemail",
        "program_contact_phone": "sfspcontactphone",
        "site_supervisor_salutation": "sitesupervisorsalutatio",
        "site_supervisor_first_name": "sitesupervisorfirstname",
        "site_supervisor_last_name": "sitesupervisorlastname",
        "site_supervisor_title_position": "sitesupervisortitleposition",
        "site_supervisor_email": "sitesupervisoremail",
        "site_supervisor_phone": "sitesupervisorphone",
        "days_of_operation": "daysofoperation",
        "meal_types_served": "mealtypesserved",
        "primary_auth_rep_salutation": "primaryauthorizedreprese",
        "primary_auth_rep_first_name": "primaryauthorizedreprese_1",
        "primary_auth_rep_last_name": "primaryauthorizedreprese_2",
        "primary_auth_rep_title_position": "primaryauthorizedreprese_3",
        "primary_auth_rep_email": "primaryauthorizedreprese_4",
        "primary_auth_rep_phone": "primaryauthorizedreprese_5"
    }

    ce_mapping = {
        "program_year": "programyear",
        "ce_id": "ceid",
        "name": "cename",
        "county": "cecounty",
        "type_of_agency": "typeofagency",
        "county_district_code": "countydistrictcode",
        "esc": "esc",
        "tda_region": "tdaregion",
        "street_address1": "cestreetaddressline1",
        "street_address2": "cestreetaddressline2",
        "street_city": "cestreetaddresscity",
        "street_state": "cestreetaddressstate",
        "street_zip": "cestreetaddresszipcode",
        "ce_status": "cestatus"
    }

    sso_ce_mapping = {
        "superintendent_salutation": "superintendentsalutation",
        "superintendent_first_name": "superintendentfirstname",
        "superintendent_last_name": "superintendentlastname",
        "superintendent_title_position": "superintendenttitleposition",
        "superintendent_email": "superintendentemail",
        "superintendent_phone": "superintendentphone",
        "childnutdir_salutation": "childnutdirsalutation",
        "childnutdir_first_name": "childnutdirfirstname",
        "childnutdir_last_name": "childnutdirlastname",
        "childnutdir_title_position": "childnutdirtitleposition",
        "childnutdir_email": "childnutdiremail",
        "childnutdir_phone": "childnutdirphone"
    }

class GeoAttributes:
    geo_attributes = [
        'street_address1', 
        'street_address2',
        'street_city',
        'street_state',
        'street_zip',
        'latitude',
        'longitude'
    ]

    location_attributes = [
        'street_address1', 
        'street_address2',
        'street_city',
        'street_state',
        'street_zip'
    ]
