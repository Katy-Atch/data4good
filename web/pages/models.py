from django.db import models
from phone_field import PhoneField

# test blah

# Create your models here.
class Site(models.Model):
    # Still need unique identifier for sites

    # Defined by myself
    most_current_record = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    # SSO or SFSP site
    SSO = 'SSO'
    SFSP = 'SFSP'
    OTHER = 'OTHER' 

    program_choices = (
        (SSO, 'Seamless Summer Option'),
        (SFSP, 'Summer Food Service Program'),
        (OTHER, 'Other'),
    )
    sso_or_sfsp = models.CharField(
        max_length=20,
        choices=program_choices,
        default=OTHER,
    )
    # End defined by myself

    # Fetch from data portal
    program_year = models.CharField(max_length=500, null=True, blank=True)
    site_id = models.IntegerField()
    ce_id = models.IntegerField(null=True, blank=True)
    geo_id = models.IntegerField()
    # ce_id = models.ForeignKey(
    #     'CE',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    # )

    # Type of SNP org- for SSO only
    CHARTER = 'CHARTER'
    PRIVATE = 'PRIVATE'
    PUBLIC = 'PUBLIC'
    RCCI = 'RCCI'
    OTHER = 'OTHER'
    snp_org_choices = (
        (CHARTER, 'Charter'),
        (PRIVATE, 'Private'),
        (PUBLIC, 'Public'),
        (RCCI, 'Residential Child Care Institution'),
        (OTHER, 'Other'),
    )
    type_of_snp_org = models.CharField(
        max_length=100,
        choices=snp_org_choices,
        default=OTHER,
        null=True,
        blank=True,
    )

    # Type of SFSP org- for SFSP only
    NSC = 'NSC'
    PNP = 'PNP'
    RC = 'RC'
    SFA = 'SFA'
    UG = 'UG'
    OTHER = 'OTHER'
    sfsp_org_choices = (
        (NSC, 'Nonresidential Summer Camp'),
        (PNP, 'Private Non Profit'),
        (RC, 'Residential Camp'),
        (SFA, 'School Food Authority'),
        (UG, 'Unit of Government'),
        (OTHER, 'Other'),
    )
    type_of_sfsp_org = models.CharField(
        max_length=100,
        choices=sfsp_org_choices,
        default=OTHER,
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=500)
    county = models.CharField(max_length=500)

    # Rural or Urban
    RURAL = 'RURAL'
    URBAN = 'URBAN'
    rural_urban_choices = (
        (RURAL, 'Rural'),
        (URBAN, 'Urban'),
    )
    rural_or_urban_code = models.CharField(
        max_length=20,
        choices=rural_urban_choices,
        null=True,
        blank=True,
    )

    # Site Type- different for SSO and SFSP
    CAMP = 'CAMP'
    CLOSED = 'CLOSED'
    OPEN = 'OPEN'
    ROPEN = 'ROPEN'
    OTHER = 'OTHER'
    sso_site_type_choices = (
        (CAMP, 'Camp'),
        (CLOSED, 'Closed'),
        (OPEN, 'Open'),
        (ROPEN, 'Open Restricted'),
        (OTHER, 'Other'),
    )
    sso_site_type = models.CharField(
        max_length=20,
        choices=sso_site_type_choices,
        default=OTHER,
        null=True,
        blank=True,
    )

    CAMP_NON_RES = 'CAMP_NON_RES'
    CAMP_RES = 'CAMP_RES'
    CLOSED_ENROLLED_NEEDY = 'CLOSED_ENROLLED_NEEDY'
    CLOSED_ENROLLED_NON_NEEDY = 'CLOSED_ENROLLED_NON_NEEDY'
    HOMELESS = 'HOMELESS'
    OPEN = 'OPEN'
    ROPEN = 'ROPEN'
    OTHER = 'OTHER'
    sfsp_site_type_choices = (
        (CAMP_NON_RES, 'Camp-Non-Residential'),
        (CAMP_RES, 'Camp-Residential'),
        (CLOSED_ENROLLED_NEEDY, 'Closed-Enrolled in Needy Area'),
        (CLOSED_ENROLLED_NON_NEEDY, 'Closed-Enrolled in Non-Needy Area'),
        (HOMELESS, 'Homeless'),
        (OPEN, 'Open'),
        (ROPEN, 'Restricted Open'),
        (OTHER, 'Other'),
    )
    sfsp_site_type = models.CharField(
        max_length=100,
        choices=sfsp_site_type_choices,
        default=OTHER,
        null=True,
        blank=True,
    )

    street_address1 = models.CharField(max_length=500)
    street_address2 = models.CharField(max_length=500, null=True, blank=True)
    street_city = models.CharField(max_length=500)
    street_state = models.CharField(max_length=500)
    street_zip = models.CharField(max_length=500)

    program_contact_salutation = models.CharField(max_length=500, null=True, blank=True)
    program_contact_first_name = models.CharField(max_length=500)
    program_contact_last_name = models.CharField(max_length=500)
    program_contact_title_position = models.CharField(max_length=500)
    program_contact_email = models.EmailField()
    program_contact_phone = PhoneField(null=False, blank=True)

    site_supervisor_salutation = models.CharField(max_length=500, null=True, blank=True)
    site_supervisor_first_name = models.CharField(max_length=500, null=True, blank=True)
    site_supervisor_last_name = models.CharField(max_length=500, null=True, blank=True)
    site_supervisor_title_position = models.CharField(max_length=500, null=True, blank=True)
    site_supervisor_email = models.EmailField(null=True, blank=True)
    site_supervisor_phone = PhoneField(null=True, blank=True)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    days_of_operation = models.CharField(max_length=500)
    meal_types_served = models.CharField(max_length=500)

    primary_auth_rep_salutation = models.CharField(max_length=500, null=True, blank=True)
    primary_auth_rep_first_name = models.CharField(max_length=500, null=True, blank=True)
    primary_auth_rep_last_name = models.CharField(max_length=500, null=True, blank=True)
    primary_auth_rep_title_position = models.CharField(max_length=500, null=True, blank=True)
    primary_auth_rep_email = models.EmailField(null=True, blank=True)
    primary_auth_rep_phone = PhoneField(null=True, blank=True)

    def __str__(self):
        return self.name


class CE(models.Model):

    # Defined by myself
    most_current_record = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    # End defined by myself

    # Unique identifier
    ce_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500)
    county = models.CharField(max_length=500)
    program_year = models.CharField(max_length=500, null=True, blank=True)

    geo_id = models.IntegerField()

    EDUCATIONAL = 'EDUCATIONAL'
    GOV_AGENCY = 'GOV_AGENCY'
    INDIAN_TRIBE = 'INDIAN_TRIBE'
    MILITARY = 'MILITARY'
    PRIVATE_NON_PROFIT = 'PRIVATE_NON_PROFIT'
    OTHER = 'OTHER'
    agency_type_choices = (
        (EDUCATIONAL, 'Educational Institution'),
        (GOV_AGENCY, 'Government Agency'),
        (INDIAN_TRIBE, 'Indian Tribe'),
        (MILITARY, 'Military Installation'),
        (PRIVATE_NON_PROFIT, 'Private Non-Profit Organization'),
        (OTHER, 'Other'),
    )

    type_of_agency = models.CharField(
        max_length=100,
        choices=agency_type_choices,
        default=OTHER,
    )

    county_district_code = models.CharField(max_length=500, null=True, blank=True)
    esc = models.IntegerField()
    tda_region = models.IntegerField()
    street_address1 = models.CharField(max_length=500)
    street_address2 = models.CharField(max_length=500, null=True, blank=True)
    street_city = models.CharField(max_length=500)
    street_state = models.CharField(max_length=500)
    street_zip = models.CharField(max_length=500)

    superintendent_salutation = models.CharField(max_length=500, null=True, blank=True)
    superintendent_first_name = models.CharField(max_length=500, null=True, blank=True)
    superintendent_last_name = models.CharField(max_length=500, null=True, blank=True)
    superintendent_title_position = models.CharField(max_length=150000, null=True, blank=True)
    superintendent_email = models.EmailField(null=True, blank=True)
    superintendent_phone = PhoneField(blank=True, null=True)

    childnutdir_salutation = models.CharField(max_length=500, null=True, blank=True)
    childnutdir_first_name = models.CharField(max_length=500, null=True, blank=True)
    childnutdir_last_name = models.CharField(max_length=500, null=True, blank=True)
    childnutdir_title_position = models.CharField(max_length=500, null=True, blank=True)
    childnutdir_email = models.EmailField(null=True, blank=True)
    childnutdir_phone = PhoneField(null=True, blank=True)

    def __str__(self):
        return self.name

class GEO(models.Model):

    geo_id = models.IntegerField()

    street_address1 = models.CharField(max_length=500)
    street_address2 = models.CharField(max_length=500, null=True, blank=True)
    street_city = models.CharField(max_length=500)
    street_state = models.CharField(max_length=500)
    street_zip = models.CharField(max_length=500)
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

