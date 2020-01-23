from django.contrib import admin
from pages.models import Site, CE, GEO, SiteAdmin, CEAdmin, GEOAdmin

# Register your models here.
admin.site.register(Site,SiteAdmin)
admin.site.register(CE,CEAdmin)
admin.site.register(GEO,GEOAdmin)
