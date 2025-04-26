from django.db import models
from authentication.models import User
from parking.models import Parking, ParkingGroup

class ReserveParking(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
   slot = models.IntegerField()
   request_ref = models.CharField(max_length=10)
   start_time = models.DateTimeField()
   end_time = models.DateTimeField()
   status = models.BooleanField(default=True)
   payment_status = models.BooleanField(default=False)
   total_price = models.DecimalField(max_digits=10, decimal_places=2)

   def __str__(self):
        return self.user.first_name + ' ' + self.parking.name


class ApprovedRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parking = models.ForeignKey(Parking, related_name='parking',on_delete=models.CASCADE)
    reference_trx = models.CharField(max_length=20, default="none")
    slot = models.IntegerField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    payment_status = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    stop = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    def __str__(self):
        return self.user.first_name + ' ' + self.parking.name



class Payment(models.Model):
    # Unique identifier for the payment
    request_id = models.ForeignKey(ApprovedRequest, related_name='request_id',on_delete=models.CASCADE)
    tx_ref = models.CharField(max_length=50, unique=True)  # Transaction reference
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who made the payment
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount paid
    currency = models.CharField(max_length=10, default='ETB')  # Currency of the payment
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ], default='pending')  # Payment status
    date = models.DateTimeField(auto_now_add=True)  # Timestamp of when the payment was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of when the payment was last updated

    
    def __str__(self):
        return f"Payment {self.tx_ref} - Amount: {self.amount} {self.currency} - Status: {self.status}"


class Incident(models.Model):
    incident_type = [
        ('Accident','Accident'),
        ('Thife','Thife'),
        ('Vandalism','Vandalism'),
        ('Item Lost','Item Lost'),
    ]
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
    request = models.ForeignKey(ApprovedRequest, on_delete=models.CASCADE)
    incident_type  = models.CharField(max_length=100, choices = incident_type)
    date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(max_length=200)
    evidence = models.FileField(upload_to="Incident/", default="1.jpg")

    def __str__(self):
        return self.incident_type
    
    
class Request(models.Model):
  subcity_choice = [
        ('Addis Ketema','Addis Ketema'),
        ('Akaky Kaliti','Akaky Kaliti'),
        ('Arada','Arada'),
        ('Bole','Bole'),
        ('Gullele','Gullele'),
        ('Kirkos','Kirkos'),
        ('Kolfe Keranio','Kolfe Keranio'),
        ('Lideta','Lideta'),
        ('Nifas Silk-Lafto','Nifas Silk-Lafto'),
        ('Yeka','Yeka'),
                     ]
  
  parking_group = models.ForeignKey(ParkingGroup, on_delete= models.CASCADE)    
  parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)
  is_read = models.BooleanField(default=False)
  status = models.BooleanField(default=False)
  woreda = models.ForeignKey(User, on_delete=models.CASCADE)
  subcity = models.TextField(max_length=50, choices=subcity_choice)


class ReservedRequest(models.Model):
   pass

class ApprovedRequestAdmin(models.Model):
  request_ref = models.ForeignKey(Request, on_delete=models.CASCADE)
  message = models.TextField(max_length=300)
  is_read = models.BooleanField(default=False)
  date = models.DateTimeField(auto_now_add=True)


class DecliendRequestAdmin(models.Model):
  request_ref = models.ForeignKey(Request, on_delete=models.CASCADE)
  message = models.TextField(max_length=300)
  is_read = models.BooleanField(default=False)
  date = models.DateTimeField(auto_now_add=True)


class DeletedInstance(models.Model):
  instance_type = [
    ('Parking-Group','Parking-Group'),
    ('Parking','Parking'),
    ('Parking-Group-Member','Parking-Group-Member'),
  ]
  user = models.ForeignKey(User, on_delete=models.CASCADE ,null=True, blank=True)
  parking_group = models.ForeignKey(ParkingGroup, on_delete=models.CASCADE ,null=True, blank=True)
  parking = models.ForeignKey(Parking, on_delete=models.CASCADE, null=True, blank=True)
  woreda_admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Woreda_admin")
  reason = models.TextField()
  Instance_type = models.CharField(max_length=100, choices=instance_type, default='Parking')
  date = models.DateTimeField(auto_now_add=True)

