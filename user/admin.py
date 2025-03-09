from django.contrib import admin
from .models import Car, LegalDocument, Notification, Message,UserLegalDocument

# Register your models here.
admin.site.register(Car)
admin.site.register(LegalDocument)
admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(UserLegalDocument)