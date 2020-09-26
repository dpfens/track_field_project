from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from utility.models import base as base_models


# Create your models here.
class Address(base_models.BaseAuditModel):
    """
    Information about a given postal address
    """
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


class AddressComponent(base_models.BaseModel):
    """
    A specific address component instance

    Example: Des Moines, Sacramento County, Colorado Avenue
    """
    address_component_type = models.ForeignKey('AddressComponentType', models.DO_NOTHING)
    name = models.CharField(max_length=150)
    long_name = models.CharField(max_length=150)
    short_name = models.CharField(max_length=100)


class AddressComponentType(base_models.BaseModel):
    """
    Type of address component

    Examples: Locality, political, neighborhood, establishment, etc.
    """
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)


class Amenity(base_models.BaseAuditModel):
    """
    Features of a given Venue

    Example: Weight room, Pool, etc.
    """
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=255)


class Continent(base_models.BaseModel):
    code = models.CharField(unique=True, max_length=2)
    name = models.CharField(unique=True, max_length=13)
    geonames_id = models.IntegerField()


class Country(base_models.BaseModel):
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


class CountryCodes(base_models.BaseModel):
    """
    Country ID codes
    """
    country = models.OneToOneField(Country, on_delete=models.DO_NOTHING)
    ioc_code = models.CharField(max_length=3, blank=True, null=True)
    fifa_code = models.CharField(max_length=3, blank=True, null=True)
    undp_code = models.CharField(max_length=3)
    iso3_code = models.CharField(max_length=4, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)


class CountryCurrency(base_models.BaseModel):
    country = models.ForeignKey(Country, models.DO_NOTHING)
    currency = models.ForeignKey('Currency', models.DO_NOTHING)

    class Meta:
        unique_together = (('country', 'currency'),)


class Currency(base_models.BaseModel):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)


class Language(base_models.BaseModel):
    """
    Identifiers of languages
    """
    iso_639_3 = models.CharField(max_length=3, blank=True, null=True)
    iso_639_2 = models.CharField(max_length=11, blank=True, null=True)
    iso_639_1 = models.CharField(max_length=2, blank=True, null=True)
    name = models.CharField(max_length=58, blank=True, null=True)


class LanguageVariant(base_models.BaseModel):
    """
    Language variants
    """
    language = models.ForeignKey(Language, models.DO_NOTHING)
    iso_639_1 = models.CharField(max_length=14, blank=True, null=True)
    language_code = models.CharField(max_length=4, blank=True, null=True)
    territory = models.CharField(max_length=3, blank=True, null=True)


class Location(base_models.BaseModel):
    """
    A location based on geographic coordinates and elevation
    """
    id = models.BigAutoField(primary_key=True)
    place_id = models.CharField(max_length=300)
    geonames_id = models.PositiveIntegerField(blank=True, null=True)
    formatted_address = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=12, decimal_places=3)
    longitude = models.DecimalField(max_digits=12, decimal_places=3)
    elevation = models.DecimalField(max_digits=12, decimal_places=5, blank=True, null=True)


class LocationAddress(base_models.BaseModel):
    """
    Linking a location to an address
    """
    location = models.ForeignKey(Location, models.DO_NOTHING)
    address_component = models.ForeignKey(AddressComponent, models.DO_NOTHING)

    class Meta:
        unique_together = (('address_component', 'location'),)


class LocationType(base_models.BaseModel):
    """
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)


class LocationTypes(base_models.BaseModel):
    location_type = models.ForeignKey(LocationType, models.DO_NOTHING)
    location = models.ForeignKey(Location, models.DO_NOTHING)

    class Meta:
        unique_together = (('location_type', 'location'),)


class Terrain(base_models.BaseModel):
    """
    Types of Terrain

    Example: Hills, Mountains, Plains, etc.
    """
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)


class Venue(base_models.BaseModel):
    """
    """
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.CharField(unique=True, max_length=50)
    address = models.ForeignKey(Address, models.DO_NOTHING)

    def get_absolute_url(self):
        return reverse('geography.views.venue_details', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Venue, self).save(*args, **kwargs)


class VenueAmenities(base_models.BaseModel):
    """
    Records when amenities were added/removes from a venue
    """
    venue = models.OneToOneField(Venue, on_delete=models.DO_NOTHING)
    amenity = models.ForeignKey(Amenity, models.DO_NOTHING)
    start = models.DateField()
    end = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = (('venue', 'amenity'),)


class VenueLocations(base_models.BaseModel):
    """
    Identifies the location of a venue
    """
    venue = models.ForeignKey(Venue, models.DO_NOTHING)
    location = models.ForeignKey(Location, models.DO_NOTHING)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = (('venue', 'location'),)


class VenueType(base_models.BaseModel):
    """
    Type of venue

    Example: embassy, clothing store, museum, etc.
    """
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)


class VenueTypes(base_models.BaseModel):
    """
    Assocates a Venue Type to a Venue
    """
    venue = models.ForeignKey(Venue, models.DO_NOTHING)
    venue_type = models.ForeignKey(VenueType, models.DO_NOTHING)

    class Meta:
        unique_together = (('venue_type', 'venue'),)


class Weather(base_models.BaseAuditModel):
    """
    Weather at a given location at a given time
    """
    location = models.ForeignKey(Location, models.DO_NOTHING)
    date = models.DateTimeField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    precipitation = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = (('location', 'date', ),)
