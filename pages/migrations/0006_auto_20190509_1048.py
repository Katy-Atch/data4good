# Generated by Django 2.2.1 on 2019-05-09 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20190509_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='ce_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]