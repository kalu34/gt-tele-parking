from django.contrib import admin
from .models import Parking, WorkingHours, ParkingLegalDoc, Category, ParkingGroup, ParkingGroupMember
from .forms import ParkingForm


# Register your models here.
class  ParkingAdmin(admin.ModelAdmin):
  form = ParkingForm

admin.site.register(Parking, ParkingAdmin)

admin.site.register(WorkingHours)
admin.site.register(ParkingLegalDoc)
admin.site.register(Category)

admin.site.register(ParkingGroup)
admin.site.register(ParkingGroupMember)