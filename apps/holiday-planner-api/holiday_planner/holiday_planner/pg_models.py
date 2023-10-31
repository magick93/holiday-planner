# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=80)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    elevation = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    feature_code = models.CharField(max_length=10, blank=True, null=True)
    place_code = models.CharField(max_length=2, blank=True, null=True)
    admin1_id = models.IntegerField(blank=True, null=True)
    admin2_id = models.IntegerField(blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)
    place_id = models.IntegerField(blank=True, null=True)
    admin1 = models.CharField(max_length=80, blank=True, null=True)
    admin2 = models.CharField(max_length=80, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    geom = models.TextField(unique=True, blank=True, null=True)  # This field type is a guess.
    country = models.ForeignKey('Country', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'place'


class Country(models.Model):
    iso = models.CharField(unique=True, max_length=2)
    name = models.CharField(max_length=80)
    nicename = models.CharField(max_length=80)
    iso3 = models.CharField(max_length=3, blank=True, null=True)
    numcode = models.SmallIntegerField(blank=True, null=True)
    phonecode = models.IntegerField()
    is_public = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'country'
