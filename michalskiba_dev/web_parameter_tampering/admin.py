from django.contrib import admin

from web_parameter_tampering.models import PressApplication, User

admin.site.register(User)
admin.site.register(PressApplication)
