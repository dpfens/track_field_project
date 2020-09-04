from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


# Create your models here.
class Address(models.Model):
    raw = models.CharField(max_length=1000)
    name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150)
    street = models.CharField(max_length=150)
    area_district = models.CharField(max_length=150)
    city = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_addresses')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_addresses')

    class Meta:
        db_table = 'address'


class AddressComponent(models.Model):
    address_component_type = models.ForeignKey('AddressComponentType', models.DO_NOTHING)
    name = models.CharField(max_length=150)
    long_name = models.CharField(max_length=150)
    short_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_address_components')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_address_components')

    class Meta:
        db_table = 'address_component'


class AddressComponentType(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_address_component_types')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_address_component_types')

    class Meta:
        db_table = 'address_component_type'


class Amenity(models.Model):
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_amenities')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_amenities')

    class Meta:
        db_table = 'amenity'


class Continent(models.Model):
    code = models.CharField(unique=True, max_length=2)
    name = models.CharField(unique=True, max_length=13)
    geonames_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_continents')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_continents')

    class Meta:
        db_table = 'continent'


class Country(models.Model):
    continent = models.ForeignKey(Continent, models.DO_NOTHING)
    iso = models.CharField(unique=True, max_length=2, blank=True, null=True)
    iso3 = models.CharField(max_length=3, blank=True, null=True)
    iso_numeric = models.IntegerField(blank=True, null=True)
    fips = models.CharField(max_length=2, blank=True, null=True)
    name = models.CharField(unique=True, max_length=44, blank=True, null=True)
    full_name = models.CharField(max_length=500)
    creation = models.DateField(blank=True, null=True)
    disintegration = models.DateField(blank=True, null=True)
    capital = models.CharField(max_length=19, blank=True, null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)
    tld = models.CharField(max_length=3, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    postal_code_format = models.CharField(max_length=55, blank=True, null=True)
    postal_code_regex = models.CharField(max_length=400, blank=True, null=True)
    languages = models.CharField(max_length=200, blank=True, null=True)
    geonames_id = models.IntegerField(blank=True, null=True)
    neighbours = models.CharField(max_length=41, blank=True, null=True)
    equivalent_fips_code = models.CharField(max_length=2, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        db_table = 'country'


class CountryCodes(models.Model):
    country = models.OneToOneField(Country, on_delete=models.DO_NOTHING)
    ioc_code = models.CharField(max_length=3, blank=True, null=True)
    fifa_code = models.CharField(max_length=3, blank=True, null=True)
    undp_code = models.CharField(max_length=3)
    iso3_code = models.CharField(max_length=4, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'country_codes'


class CountryCurrency(models.Model):
    country = models.ForeignKey(Country, models.DO_NOTHING)
    currency = models.ForeignKey('Currency', models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_country_currencies')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_country_currencies')

    class Meta:
        db_table = 'country_currency'
        unique_together = (('country', 'currency'),)


class Currency(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_currencies')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_currencies')

    class Meta:
        db_table = 'currency'


class Language(models.Model):
    iso_639_3 = models.CharField(max_length=3, blank=True, null=True)
    iso_639_2 = models.CharField(max_length=11, blank=True, null=True)
    iso_639_1 = models.CharField(max_length=2, blank=True, null=True)
    name = models.CharField(max_length=58, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_languages')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_languages')

    class Meta:
        db_table = 'language'


class LanguageVariant(models.Model):
    language = models.ForeignKey(Language, models.DO_NOTHING)
    iso_639_1 = models.CharField(max_length=14, blank=True, null=True)
    language_code = models.CharField(max_length=4, blank=True, null=True)
    territory = models.CharField(max_length=3, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_language_variants')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_language_variants')

    class Meta:
        db_table = 'language_variant'


class Location(models.Model):
    id = models.BigAutoField(primary_key=True)
    place_id = models.CharField(max_length=300)
    geonames_id = models.PositiveIntegerField(blank=True, null=True)
    formatted_address = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=12, decimal_places=3)
    longitude = models.DecimalField(max_digits=12, decimal_places=3)
    elevation = models.DecimalField(max_digits=12, decimal_places=5, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_locations')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_locations')

    class Meta:
        db_table = 'location'


class LocationAddress(models.Model):
    location = models.ForeignKey(Location, models.DO_NOTHING)
    address_component = models.ForeignKey(AddressComponent, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_location_addresses')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_location_addresses')

    class Meta:
        db_table = 'location_address'
        unique_together = (('address_component', 'location'),)


class LocationType(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_location_type')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_location_type')

    class Meta:
        db_table = 'location_type'


class LocationTypes(models.Model):
    location_type = models.ForeignKey(LocationType, models.DO_NOTHING)
    location = models.ForeignKey(Location, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_location_types')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_location_types')

    class Meta:
        db_table = 'location_types'
        unique_together = (('location_type', 'location'),)


class Terrain(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=20)

    class Meta:
        db_table = 'terrain'


class Venue(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.CharField(unique=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('geography.views.venue_details', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Venue, self).save(*args, **kwargs)

    class Meta:
        db_table = 'venue'


class VenueAmenities(models.Model):
    venue = models.OneToOneField(Venue, on_delete=models.DO_NOTHING)
    amenity = models.ForeignKey(Amenity, models.DO_NOTHING)
    start = models.DateField()
    end = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by')

    class Meta:
        db_table = 'venue_amenities'
        unique_together = (('venue', 'amenity'),)


class VenueLocations(models.Model):
    venue = models.ForeignKey(Venue, models.DO_NOTHING)
    location = models.ForeignKey(Location, models.DO_NOTHING)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'venue_locations'
        unique_together = (('venue', 'location'),)


class VenueType(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'venue_type'


class VenueTypes(models.Model):
    venue = models.ForeignKey(Venue, models.DO_NOTHING)
    venue_type = models.ForeignKey(VenueType, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'venue_types'
        unique_together = (('venue_type', 'venue'),)


class Weather(models.Model):
    location = models.ForeignKey(Location, models.DO_NOTHING)
    date = models.DateTimeField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    precipitation = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    source = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'weather'
        unique_together = (('location', 'date', 'source'),)
