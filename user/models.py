from django.db import models
from authentication.models import User
from core.models import ApprovedRequest
from typing import List


class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    name = models.CharField(max_length=300, default="toyota")
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    color = models.CharField(max_length=20)
    mileage = models.IntegerField()
    plate_number = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.plate_number})"
    

class LegalDocument(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    document = models.FileField(upload_to="legal_document/")  # Changed FieldFile to FileField
    document_type = models.CharField(max_length=50)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.document_type}"
    
class Notification(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=3000)
    sent_at = models.DateField()
    is_seen = models.BooleanField()
    action_url = models.TextField(max_length=300)

class UserLegalDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driving_licence = models.FileField(upload_to = 'userLegalDocument/driving_licence')
    national_id = models.FileField(upload_to = "userLegalDocument/national_id")

class Message(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.ForeignKey(ApprovedRequest, on_delete=models.CASCADE)
    message = models.TextField(max_length=3000)
    sent_at = models.DateField()
    is_seen = models.BooleanField()

# Wallet Model 
