from django.contrib import admin
from alias_app.webapp.models import Settings
from alias_app.webapp.models import HostingService


class SettingsAdmin(admin.ModelAdmin):
    pass


class HostingServiceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Settings, SettingsAdmin)
admin.site.register(HostingService, HostingServiceAdmin)
