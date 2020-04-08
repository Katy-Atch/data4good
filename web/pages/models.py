from django.db import models
from django.contrib import admin
from phone_field import PhoneField

class Site(models.Model):

    # Defined by myself
    most_current_record = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    # SSO or SFSP entity
    SSO = 'SSO'
    SFSP = 'SFSP'
    OTHER = 'OTHER'
    program_choices = (
        (SSO, 'Seamless Summer Option'),
        (SFSP, 'Summer Food Service Program'),
        (OTHER, 'Other')
    )

    sso_or_sfsp = models.CharField(
        max_length=255,
        choices=program_choices,
        default=OTHER,
    )
    # End defined by myself

    # Fetch from data portal
    program_year = models.CharField(max_length=255)
    site_id = models.IntegerField()
    ce_id = models.IntegerField()
    geo_id = models.IntegerField(null=True, blank=True)

    name = models.CharField(max_length=255)
    county = models.CharField(max_length=255)

    street_address1 = models.CharField(max_length=255)
    street_address2 = models.CharField(max_length=255, null=True, blank=True)
    street_city = models.CharField(max_length=255)
    street_state = models.CharField(max_length=255)
    street_zip = models.CharField(max_length=255)

    program_contact_salutation = models.CharField(max_length=255, null=True, blank=True)
    program_contact_first_name = models.CharField(max_length=255)
    program_contact_last_name = models.CharField(max_length=255)
    program_contact_title_position = models.CharField(max_length=255)
    program_contact_email = models.EmailField(null=True, blank=True)
    program_contact_phone = PhoneField(null=False, blank=True)

    site_supervisor_salutation = models.CharField(max_length=255, null=True, blank=True)
    site_supervisor_first_name = models.CharField(max_length=255, null=True, blank=True)
    site_supervisor_last_name = models.CharField(max_length=255, null=True, blank=True)
    site_supervisor_title_position = models.CharField(max_length=255, null=True, blank=True)
    site_supervisor_email = models.EmailField(null=True, blank=True)
    site_supervisor_phone = PhoneField(null=True, blank=True)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    days_of_operation = models.CharField(max_length=255)
    meal_types_served = models.CharField(max_length=255)

    primary_auth_rep_salutation = models.CharField(max_length=255, null=True, blank=True)
    primary_auth_rep_first_name = models.CharField(max_length=255, null=True, blank=True)
    primary_auth_rep_last_name = models.CharField(max_length=255, null=True, blank=True)
    primary_auth_rep_title_position = models.CharField(max_length=255, null=True, blank=True)
    primary_auth_rep_email = models.EmailField(null=True, blank=True)
    primary_auth_rep_phone = PhoneField(null=True, blank=True)

    breakfast_time = models.CharField(max_length=255, null=True, blank=True)
    amsnack_time = models.CharField(max_length=255, null=True, blank=True)
    lunch_time = models.CharField(max_length=255, null=True, blank=True)
    pmsnack_time = models.CharField(max_length=255, null=True, blank=True)
    supper_time = models.CharField(max_length=255, null=True, blank=True)
    breakfast_days_served = models.CharField(max_length=255, null=True, blank=True)
    amsnack_days_served = models.CharField(max_length=255, null=True, blank=True)
    lunch_days_served = models.CharField(max_length=255, null=True, blank=True)
    pmsnack_days_served = models.CharField(max_length=255, null=True, blank=True)
    supper_days_served = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class CE(models.Model):

    # Defined by myself
    most_current_record = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    # SSO or SFSP entity
    SSO = 'SSO'
    SFSP = 'SFSP'
    OTHER = 'OTHER'
    program_choices = (
        (SSO, 'Seamless Summer Option'),
        (SFSP, 'Summer Food Service Program'),
        (OTHER, 'Other')
    )

    sso_or_sfsp = models.CharField(
        max_length=255,
        choices=program_choices,
        default=OTHER,
    )
    # End defined by myself

    # Unique identifier
    ce_id = models.IntegerField()
    name = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    program_year = models.CharField(max_length=255)
    ce_status = models.CharField(max_length=255, null=True, blank=True)

    geo_id = models.IntegerField(null=True, blank=True)

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
        max_length=255,
        choices=agency_type_choices,
        default=OTHER,
    )

    street_address1 = models.CharField(max_length=255)
    street_address2 = models.CharField(max_length=255, null=True, blank=True)
    street_city = models.CharField(max_length=255)
    street_state = models.CharField(max_length=255)
    street_zip = models.CharField(max_length=255)

    superintendent_salutation = models.CharField(max_length=255, null=True, blank=True)
    superintendent_first_name = models.CharField(max_length=255, null=True, blank=True)
    superintendent_last_name = models.CharField(max_length=255, null=True, blank=True)
    superintendent_title_position = models.CharField(max_length=255, null=True, blank=True)
    superintendent_email = models.EmailField(null=True, blank=True)
    superintendent_phone = PhoneField(blank=True, null=True)

    childnutdir_salutation = models.CharField(max_length=255, null=True, blank=True)
    childnutdir_first_name = models.CharField(max_length=255, null=True, blank=True)
    childnutdir_last_name = models.CharField(max_length=255, null=True, blank=True)
    childnutdir_title_position = models.CharField(max_length=255, null=True, blank=True)
    childnutdir_email = models.EmailField(null=True, blank=True)
    childnutdir_phone = PhoneField(null=True, blank=True)

    def __str__(self):
        return self.name

class GEO(models.Model):

    geo_id = models.AutoField(primary_key=True)

    street_address1 = models.CharField(max_length=255)
    street_address2 = models.CharField(max_length=255, null=True, blank=True)
    street_city = models.CharField(max_length=255)
    street_state = models.CharField(max_length=255)
    street_zip = models.CharField(max_length=255)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    valid_coordinates = models.BooleanField(default=True)

class SiteAdmin(admin.ModelAdmin):
    readonly_fields = ('last_updated',)
    list_display = ('name', 'last_updated')

class CEAdmin(admin.ModelAdmin):
    readonly_fields = ('last_updated',)
    list_display = ('name', 'last_updated')

class GEOAdmin(admin.ModelAdmin):
    list_display = ('street_address1', 'geo_id')