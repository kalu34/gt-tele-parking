from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ApprovedRequest)
admin.site.register(ReservedRequest)
admin.site.register(Incident)

admin.site.register(ReserveParking)
admin.site.register(Request)
admin.site.register(ApprovedRequestAdmin)
admin.site.register(DecliendRequestAdmin)
admin.site.register(DeletedInstance)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['request_id', 'tx_ref', 'user', 'amount', 'currency', 'status']
    list_filter = ['status', 'currency']
    search_fields = ['tx_ref', 'user__username']  # Add more fields if needed
    readonly_fields = ['date', 'updated_at']

