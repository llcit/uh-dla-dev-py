from django.contrib import admin

from .models import Repository, Community, Collection, MetadataElement, Record

admin.site.register(Repository)
admin.site.register(Community)
admin.site.register(Collection)
admin.site.register(Record)
admin.site.register(MetadataElement)