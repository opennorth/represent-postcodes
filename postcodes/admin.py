from django.contrib.gis import admin

from postcodes.models import Postcode, PostcodeConcordance


@admin.register(PostcodeConcordance)
class PostcodeConcordanceAdmin(admin.ModelAdmin):
    list_display = ('code', 'boundary', 'source')


@admin.register(Postcode)
class PostcodeAdmin(admin.OSMGeoAdmin):
    list_display = ('code', 'city', 'province')
