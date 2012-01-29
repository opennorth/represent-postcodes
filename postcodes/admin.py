from django.contrib.gis import admin

from postcodes.models import *

class PostcodeAdmin(admin.OSMGeoAdmin):
    list_display = ('code', 'city', 'province')

class PostcodeConcordanceAdmin(admin.ModelAdmin):
    list_display = ('code', 'boundary', 'source')

admin.site.register(Postcode, PostcodeAdmin)
admin.site.register(PostcodeConcordance, PostcodeConcordanceAdmin)