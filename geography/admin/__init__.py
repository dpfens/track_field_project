from django.contrib import admin
from track_field_project.admin.site import advanced_admin
from geography import models

READONLY_FIELDS = ('created_at', 'last_modified_at')


@admin.register(models.Address, site=advanced_admin)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'county', 'state')
    readonly_fields = READONLY_FIELDS


@admin.register(models.AddressComponent, site=advanced_admin)
class AddressComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'address_component_type')
    readonly_fields = READONLY_FIELDS


@admin.register(models.AddressComponentType, site=advanced_admin)
class AddressComponentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS


@admin.register(models.Amenity, site=advanced_admin)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS


@admin.register(models.Continent, site=advanced_admin)
class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS


@admin.register(models.Country, site=advanced_admin)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso', 'continent')


@admin.register(models.CountryCodes, site=advanced_admin)
class CountryCodesAdmin(admin.ModelAdmin):
    list_display = ('country', 'iso3_code', 'ioc_code', 'fifa_code')


@admin.register(models.CountryCurrency, site=advanced_admin)
class CountryCurrencyAdmin(admin.ModelAdmin):
    list_display = ('country', 'currency')
    readonly_fields = READONLY_FIELDS


@admin.register(models.Currency, site=advanced_admin)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    readonly_fields = READONLY_FIELDS


@admin.register(models.Language, site=advanced_admin)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_639_1', 'iso_639_2')
    readonly_fields = READONLY_FIELDS


@admin.register(models.LanguageVariant, site=advanced_admin)
class LanguageVariantAdmin(admin.ModelAdmin):
    list_display = ('iso_639_1', 'language_code', 'iso_639_1')
    readonly_fields = READONLY_FIELDS


@admin.register(models.Location, site=advanced_admin)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('formatted_address', 'latitude', 'longitude', 'elevation')
    readonly_fields = READONLY_FIELDS


@admin.register(models.LocationAddress, site=advanced_admin)
class LocationAddressAdmin(admin.ModelAdmin):
    list_display = ('location', 'address_component')
    readonly_fields = READONLY_FIELDS


@admin.register(models.LocationType, site=advanced_admin)
class LocationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS


@admin.register(models.LocationTypes, site=advanced_admin)
class LocationTypesAdmin(admin.ModelAdmin):
    list_display = ('location_type', 'location')
    readonly_fields = READONLY_FIELDS


@admin.register(models.Terrain, site=advanced_admin)
class TerrainAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS


@admin.register(models.Venue, site=advanced_admin)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    readonly_fields = READONLY_FIELDS


@admin.register(models.VenueAmenities, site=advanced_admin)
class VenueAmenitiesAdmin(admin.ModelAdmin):
    list_display = ('venue', 'amenity', 'start', 'end')
    readonly_fields = READONLY_FIELDS


@admin.register(models.VenueLocations, site=advanced_admin)
class VenueLocationsAdmin(admin.ModelAdmin):
    list_display = ('venue', 'location', 'start_date', 'end_date')
    readonly_fields = READONLY_FIELDS


@admin.register(models.VenueType, site=advanced_admin)
class VenueTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS


@admin.register(models.VenueTypes, site=advanced_admin)
class VenueTypesAdmin(admin.ModelAdmin):
    list_display = ('venue', 'venue_type')
    readonly_fields = READONLY_FIELDS


@admin.register(models.Weather, site=advanced_admin)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ('location', 'date')
    readonly_fields = READONLY_FIELDS
