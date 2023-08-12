from django.contrib import admin
from .models import CalendarEntry, CalendarUser
from import_export.admin import ExportActionMixin



class CalendarEntryAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("user", "paymentMode", "singleCount","multiCount","isPaid","isApproved","isProcessing","isPrinted","isDelivered","isRejected","isDeleted","isCompleted")
    search_fields = ["user__user__first_name","user__user__last_name", "singleCount", "multiCount"]
    list_editable = ("isPaid","isApproved","isProcessing","isPrinted","isDelivered","isRejected","isDeleted","isCompleted")
    
admin.site.register(CalendarEntry,CalendarEntryAdmin)
admin.site.register(CalendarUser)