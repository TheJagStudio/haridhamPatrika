from django.contrib import admin
from .models import (
    City,
    Taluka,
    District,
    State,
    Pradesh,
    BhagatDetail,
    Karyakarta,
    Zone,
)
from import_export.admin import ExportActionMixin


class DistrictAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("districtName", "districtCode", "state")
    search_fields = ["districtName", "districtCode", "state__stateName"]
    list_editable = ("districtCode",)


class PradeshAdmin(ExportActionMixin, admin.ModelAdmin):
    search_fields = ["pradeshName"]


class StateAdmin(ExportActionMixin, admin.ModelAdmin):
    search_fields = ["stateName"]


class TalukaAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("talukaName", "district", "state")
    search_fields = ["talukaName", "district__districtName", "state__stateName"]


class CityAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("cityName", "pradesh", "taluka", "district", "state", "pincode")
    search_fields = [
        "cityName",
        "pradesh__pradeshName",
        "taluka__talukaName",
        "district__districtName",
        "state__stateName",
        "pincode",
    ]


class ZoneAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("zoneName", "city")
    search_fields = ["zoneName", "city"]


class BhagatDetailAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "districtCode",
        "receiptNo",
        "entryDate",
        "endDate",
        "subYear",
        "addressOne",
        "addressTwo",
        "addressThree",
        "city",
        "taluka",
        "district",
        "state",
        "pradesh",
        "phoneNum",
        "pincode",
        "dataid",
        "is_active",
    )
    search_fields = [
        "name",
        "districtCode",
        "receiptNo",
        "entryDate",
        "endDate",
        "subYear",
        "addressOne",
        "addressTwo",
        "addressThree",
        "city__cityName",
        "taluka__talukaName",
        "district__districtName",
        "state__stateName",
        "pradesh__pradeshName",
        "phoneNum",
        "dataid",
        "is_active",
    ]
    # list_editable = ("districtCode", "receiptNo","entryDate","endDate","subYear","addressOne","addressTwo","addressThree","city","taluka","district","state","pincode")


class KaryakartaAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("name", "email", "phoneNum", "city", "taluka", "district", "state")
    search_fields = [
        "name",
        "email",
        "phoneNum",
        "city__cityName",
        "taluka__talukaName",
        "district__districtName",
        "state__stateName",
    ]
    list_editable = ("email", "phoneNum", "city", "taluka", "district", "state")


admin.site.register(District, DistrictAdmin)
admin.site.register(Pradesh, PradeshAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Taluka, TalukaAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(BhagatDetail, BhagatDetailAdmin)
admin.site.register(Karyakarta, KaryakartaAdmin)
