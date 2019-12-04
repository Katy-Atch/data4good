# Generated by Django 2.2.5 on 2019-12-04 12:50

from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CE',
            fields=[
                ('most_current_record', models.BooleanField(default=True)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('ce_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('county', models.CharField(max_length=500)),
                ('program_year', models.CharField(blank=True, max_length=500, null=True)),
                ('geo_id', models.IntegerField(blank=True, null=True)),
                ('type_of_agency', models.CharField(choices=[('EDUCATIONAL', 'Educational Institution'), ('GOV_AGENCY', 'Government Agency'), ('INDIAN_TRIBE', 'Indian Tribe'), ('MILITARY', 'Military Installation'), ('PRIVATE_NON_PROFIT', 'Private Non-Profit Organization'), ('OTHER', 'Other')], default='OTHER', max_length=100)),
                ('county_district_code', models.CharField(blank=True, max_length=500, null=True)),
                ('esc', models.IntegerField()),
                ('tda_region', models.IntegerField()),
                ('street_address1', models.CharField(max_length=500)),
                ('street_address2', models.CharField(blank=True, max_length=500, null=True)),
                ('street_city', models.CharField(max_length=500)),
                ('street_state', models.CharField(max_length=500)),
                ('street_zip', models.CharField(max_length=500)),
                ('superintendent_salutation', models.CharField(blank=True, max_length=500, null=True)),
                ('superintendent_first_name', models.CharField(blank=True, max_length=500, null=True)),
                ('superintendent_last_name', models.CharField(blank=True, max_length=500, null=True)),
                ('superintendent_title_position', models.CharField(blank=True, max_length=150000, null=True)),
                ('superintendent_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('superintendent_phone', phone_field.models.PhoneField(blank=True, max_length=31, null=True)),
                ('childnutdir_salutation', models.CharField(blank=True, max_length=500, null=True)),
                ('childnutdir_first_name', models.CharField(blank=True, max_length=500, null=True)),
                ('childnutdir_last_name', models.CharField(blank=True, max_length=500, null=True)),
                ('childnutdir_title_position', models.CharField(blank=True, max_length=500, null=True)),
                ('childnutdir_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('childnutdir_phone', phone_field.models.PhoneField(blank=True, max_length=31, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GEO',
            fields=[
                ('geo_id', models.AutoField(primary_key=True, serialize=False)),
                ('street_address1', models.CharField(max_length=500)),
                ('street_address2', models.CharField(blank=True, max_length=500, null=True)),
                ('street_city', models.CharField(max_length=500)),
                ('street_state', models.CharField(max_length=500)),
                ('street_zip', models.CharField(max_length=500)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('most_current_record', models.BooleanField(default=True)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('sso_or_sfsp', models.CharField(choices=[('SSO', 'Seamless Summer Option'), ('SFSP', 'Summer Food Service Program'), ('OTHER', 'Other')], default='OTHER', max_length=20)),
                ('program_year', models.CharField(blank=True, max_length=500, null=True)),
                ('site_id', models.IntegerField()),
                ('ce_id', models.IntegerField(blank=True, null=True)),
                ('geo_id', models.IntegerField(blank=True, null=True)),
                ('type_of_snp_org', models.CharField(blank=True, choices=[('CHARTER', 'Charter'), ('PRIVATE', 'Private'), ('PUBLIC', 'Public'), ('RCCI', 'Residential Child Care Institution'), ('OTHER', 'Other')], default='OTHER', max_length=100, null=True)),
                ('type_of_sfsp_org', models.CharField(blank=True, choices=[('NSC', 'Nonresidential Summer Camp'), ('PNP', 'Private Non Profit'), ('RC', 'Residential Camp'), ('SFA', 'School Food Authority'), ('UG', 'Unit of Government'), ('OTHER', 'Other')], default='OTHER', max_length=100, null=True)),
                ('name', models.CharField(max_length=500)),
                ('county', models.CharField(max_length=500)),
                ('rural_or_urban_code', models.CharField(blank=True, choices=[('RURAL', 'Rural'), ('URBAN', 'Urban')], max_length=20, null=True)),
                ('sso_site_type', models.CharField(blank=True, choices=[('CAMP', 'Camp'), ('CLOSED', 'Closed'), ('OPEN', 'Open'), ('ROPEN', 'Open Restricted'), ('OTHER', 'Other')], default='OTHER', max_length=20, null=True)),
                ('sfsp_site_type', models.CharField(blank=True, choices=[('CAMP_NON_RES', 'Camp-Non-Residential'), ('CAMP_RES', 'Camp-Residential'), ('CLOSED_ENROLLED_NEEDY', 'Closed-Enrolled in Needy Area'), ('CLOSED_ENROLLED_NON_NEEDY', 'Closed-Enrolled in Non-Needy Area'), ('HOMELESS', 'Homeless'), ('OPEN', 'Open'), ('ROPEN', 'Restricted Open'), ('OTHER', 'Other')], default='OTHER', max_length=100, null=True)),
                ('street_address1', models.CharField(max_length=500)),
                ('street_address2', models.CharField(blank=True, max_length=500, null=True)),
                ('street_city', models.CharField(max_length=500)),
                ('street_state', models.CharField(max_length=500)),
                ('street_zip', models.CharField(max_length=500)),
                ('program_contact_salutation', models.CharField(blank=True, max_length=500, null=True)),
                ('program_contact_first_name', models.CharField(max_length=500)),
                ('program_contact_last_name', models.CharField(max_length=500)),
                ('program_contact_title_position', models.CharField(max_length=500)),
                ('program_contact_email', models.EmailField(max_length=254)),
                ('program_contact_phone', phone_field.models.PhoneField(blank=True, max_length=31)),
                ('site_supervisor_salutation', models.CharField(blank=True, max_length=500, null=True)),
                ('site_supervisor_first_name', models.CharField(blank=True, max_length=500, null=True)),
                ('site_supervisor_last_name', models.CharField(blank=True, max_length=500, null=True)),
                ('site_supervisor_title_position', models.CharField(blank=True, max_length=500, null=True)),
                ('site_supervisor_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('site_supervisor_phone', phone_field.models.PhoneField(blank=True, max_length=31, null=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('days_of_operation', models.CharField(max_length=500)),
                ('meal_types_served', models.CharField(max_length=500)),
                ('primary_auth_rep_salutation', models.CharField(blank=True, max_length=500, null=True)),
                ('primary_auth_rep_first_name', models.CharField(blank=True, max_length=500, null=True)),
                ('primary_auth_rep_last_name', models.CharField(blank=True, max_length=500, null=True)),
                ('primary_auth_rep_title_position', models.CharField(blank=True, max_length=500, null=True)),
                ('primary_auth_rep_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('primary_auth_rep_phone', phone_field.models.PhoneField(blank=True, max_length=31, null=True)),
            ],
        ),
    ]
