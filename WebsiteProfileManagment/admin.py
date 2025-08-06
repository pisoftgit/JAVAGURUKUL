from django.contrib import admin
from .models import *
# Register your models here.

class Website_Manage_Admin(admin.ModelAdmin):
    list_display = ('phone_number','email','address_line_1','address_line_2','powered_by')
admin.site.register(Website_Manage, Website_Manage_Admin)

class Social_Links_Admin(admin.ModelAdmin):
    list_display = ('facebook_link','linkedin_link','twitter_link','instagram_link','skype_link')
admin.site.register(Social_Links, Social_Links_Admin)