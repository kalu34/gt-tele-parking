from django.contrib.gis.db import models
from authentication.models import User
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django.dispatch import receiver
from django.db.models.signals import post_save


class ParkingGroup(models.Model):
    subcity_choice = [
        ('Addis Ketema', 'Addis Ketema'),
        ('Akaky Kaliti', 'Akaky Kaliti'),
        ('Arada', 'Arada'),
        ('Bole', 'Bole'),
        ('Gullele', 'Gullele'),
        ('Kirkos', 'Kirkos'),
        ('Kolfe Keranio', 'Kolfe Keranio'),
        ('Lideta', 'Lideta'),
        ('Nifas Silk-Lafto', 'Nifas Silk-Lafto'),
        ('Yeka', 'Yeka'),
    ]

    subcity = models.CharField(max_length= 20, choices=subcity_choice)
    woreda = models.CharField(max_length=20)
    kebele = models.CharField(max_length= 20)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now_add=True)

class Parking(models.Model):
    subcity_choice = [
        ('Addis Ketema', 'Addis Ketema'),
        ('Akaky Kaliti', 'Akaky Kaliti'),
        ('Arada', 'Arada'),
        ('Bole', 'Bole'),
        ('Gullele', 'Gullele'),
        ('Kirkos', 'Kirkos'),
        ('Kolfe Keranio', 'Kolfe Keranio'),
        ('Lideta', 'Lideta'),
        ('Nifas Silk-Lafto', 'Nifas Silk-Lafto'),
        ('Yeka', 'Yeka'),
    ]
    parking_group = models.ForeignKey(ParkingGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    location = models.PointField(blank=True, null=True, srid=4326)

    has_ev_charging = models.BooleanField(default=False)
    has_disabled_parking = models.BooleanField(default=False)
    is_covered = models.BooleanField(default=False)
    has_security_cameras = models.BooleanField(default=False)
    has_security_guard = models.BooleanField(default=False)
    payment_method = ArrayField(models.CharField(max_length=100), blank=True)
    amenities = ArrayField(models.CharField(max_length=300), blank=True)

    price_per_hour = models.DecimalField(max_digits=5, decimal_places=2)
    price_per_day = models.DecimalField(max_digits=15, decimal_places=2)
    slot_capacity = models.IntegerField()
    available_slots = models.IntegerField()

    subcity = models.CharField(max_length=60, choices=subcity_choice)
    woreda = models.IntegerField()
    keble = models.IntegerField()

    is_approved = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)

    image1 = models.ImageField(upload_to='parking_images', blank=True, null=True)
    image2 = models.ImageField(upload_to='parking_images', blank=True, null=True)


    def save(self, *args, **kwargs):
        super(Parking, self).save(**kwargs)
        workingDay = WorkingHours.objects.filter(parking=self).first()
        if workingDay is  None: 
            days = ['Sunday', 'Saturday', 'Friday', 'Thursday', 'Wednesday', 'Tuesday', 'Monday']
            for day in days:
                    working_hours = WorkingHours(
                        parking=self,
                        day=day,
                        start_time='14:30',
                        end_time='14:30',
                    )
                    working_hours.save()

    def __str__(self):
        return f"{self.name} {self.parking_group.name}"



class ParkingGroupMember(models.Model):
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default = False)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField()
    


class ParkingLegalDoc(models.Model):
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
    insurance_file = models.FileField(upload_to = "ParkingLegalDoc/insurance_file")
    legal_document = models.FileField(upload_to="ParkingLegalDoc/legal_file")

class Category(models.Model):
    parking_choices = [
        ('private', 'private'),
        ('public', 'public')
    ]
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
    category =  models.TextField(choices=parking_choices, max_length=30)


class WorkingHours(models.Model):
    weeks = [
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday')
    ]
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
    day = models.CharField(max_length=20, choices=weeks)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.parking.name} {self.day}"
    

@receiver(post_save, sender=ParkingGroup)
def post_save_parking_group_handler(sender, instance, created, **kwargs):
    # Skip processing if the ParkingGroup is newly created
    if created:
        print("ParkingGroup created. No changes made to related objects.")
        return

    # If the ParkingGroup is inactive, update related objects
    if not instance.is_active:
        # Fetch related Parking objects
        parkings = Parking.objects.filter(parking_group=instance)

        # Update is_active status of related Parking objects
        for parking in parkings:
            parking.is_active = False
            parking.save()

        # Fetch related ParkingGroupMember objects
        parking_members = ParkingGroupMember.objects.filter(parking__in=parkings)

        # Update is_active status of related ParkingGroupMember objects
        for member in parking_members:
            member.is_active = False
            member.save()

        print("All related Parking and ParkingGroupMember objects have been set to inactive.")
    else:
        # Do nothing if the ParkingGroup is active
        print("ParkingGroup is active. No changes made to related objects.")

