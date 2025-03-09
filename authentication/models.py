from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number,password=None, *args, **kwargs):
        if not phone_number:
            raise ValueError('Users must have a username')
        
        email = kwargs.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValueError('Email already exists')

        user = self.model(
            phone_number=phone_number,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,phone_number, email, password=None):
        user = self.create_user(
            username = username,
            phone_number=phone_number,
            email=email,
            password=password,
            role=User.SYSTEM_ADMIN_ROLE
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    
    def remove(self, id):
        try:
            user = self.get(id=id) # get the user by id.
            user.is_active = False
            user.save(using=self._db)
            return user
        except self.model.DoesNotExist:
            return None #Or raise an exception as needed.

class User(AbstractBaseUser, PermissionsMixin):

    USER_ROLE = 1
    PARKING_ROLE = 2
    TELE_ROLE = 3
    TELE_ADMIN_ROLE = 4
    TELES_ALL_ADMIN_ROLE = 5
    SYSTEM_ADMIN_ROLE = 6
    DEFAULT_ROLE = 7

    ROLES = [
        (USER_ROLE, 'User'),
        (PARKING_ROLE, 'Parking'),
        (TELE_ROLE, 'Tele Branch'),
        (TELE_ADMIN_ROLE, 'Tele Admin'),
        (TELES_ALL_ADMIN_ROLE, 'All Tele Admins'),
        (SYSTEM_ADMIN_ROLE, 'System Admin Addis Ababa'),
        (DEFAULT_ROLE, 'Role Not Assigned'),
    ]
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    role = models.IntegerField(choices=ROLES, default=USER_ROLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username','email']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.phone_number} -/ {self.first_name}"
    
    @property
    def token(self):
        token = RefreshToken.for_user(self)
        return token.access_token


class PlateNumber(models.Model):
    plate_number = models.CharField(max_length=7, unique=True, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.plate_number} - {self.user.first_name}"


class Subcity(models.Model):
    Subcity_choice = [
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
    subcity = models.CharField(max_length=40, choices=Subcity_choice)

    def __str__(self):
        return self.subcity
    
class Woreda(models.Model):
    name = models.IntegerField()
    subcity = models.ForeignKey(Subcity, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} -> {self.subcity}"


class UserRoles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.IntegerField()
    subcity = models.ForeignKey(Subcity, on_delete=models.CASCADE)
    woreda = models.ForeignKey(Woreda, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user} -> {self.user.role} -> {self.subcity}"
    
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    image = models.ImageField(upload_to="profile", default="profile/image.png")

    def __str__(self):
        return f"{self.user.first_name} - {self.image}"


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def create_transaction(self, amount, tx_ref):
        Transaction.objects.create(wallet = self, amount=amount, transaction_type='credit', transaction_ref=tx_ref)
        return True
    
    def credit(self, amount):
        self.balance += amount
        self.save()

    
    def debit(self, amount,tx_ref):
        if self.balance > amount:
            self.balance-= amount
            self.save()
            Transaction.objects.create(wallet=self, amount=amount, transaction_type='debit', transaction_ref=tx_ref)
            return True
        else: 
            return False
    
    def __str__(self):
        return self.user.first_name


class Transaction(models.Model):
    transaction_type = [
        ('credit', 'credit'),
        ('debit', 'debit'),
    ]
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_ref = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(choices=transaction_type)
    status = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        if instance.role == 1:
            Wallet.objects.create(user=instance)