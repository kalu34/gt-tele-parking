from django.contrib import admin
from .models import User,Profile, Wallet, Transaction, UserRoles, Woreda, Subcity, PlateNumber

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(UserRoles)
admin.site.register(PlateNumber)
admin.site.register(Subcity)
admin.site.register(Woreda)