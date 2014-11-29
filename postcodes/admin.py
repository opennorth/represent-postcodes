from django.contrib.gis import admin

from postcodes.models import Postcode, PostcodeConcordance


class PostcodeAdmin(admin.OSMGeoAdmin):
    list_display = ('code', 'city', 'province')

admin.site.register(Postcode, PostcodeAdmin)


class PostcodeConcordanceAdmin(admin.ModelAdmin):
    list_display = ('code', 'boundary', 'source')

admin.site.register(PostcodeConcordance, PostcodeConcordanceAdmin)
