from django.contrib import admin

from feature.models import Flag


class FlagAdmin(admin.ModelAdmin[Flag]):
    list_display = ["name", "enabled"]


admin.site.register(Flag, FlagAdmin)
