import json

from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from django_countries import countries

from .utils import get_requests_count
from .models import Tracker


class TrackerAdmin(admin.ModelAdmin):
    list_display = ("user","ip_address","ip_country","ip_region","ip_city","referrer","device_type","device","browser","browser_version","system","system_version")
    
    

admin.site.register(Tracker, TrackerAdmin)
