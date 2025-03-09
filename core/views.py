import random
import string

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import ApprovedRequest, Parking, ReservedRequest  # Import your Parking model
from django.contrib.auth.decorators import login_required
from django.utils import timezone  # Import timezone
from user.models import Car
from authentication.models import User, PlateNumber

@login_required
def reserve_parking(request, id):
    # Check if an active parking request exists for the current user
    existing_request = ReservedRequest.objects.filter(user=request.user).first()
    if existing_request:
        # Use Django messages to pass the error message
        messages.error(request, 'You already have an active parking request.')
        return redirect('user_home')  # Redirect to the user home page or another page

    # Fetch the Parking instance using the provided ID
    parking_instance = get_object_or_404(Parking, id=id)

    def generate_random_string():
    # Generate 3 random uppercase letters
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        
        # Generate 3 random digits
        numbers = ''.join(random.choices(string.digits, k=3))
        
        # Combine letters and numbers
        random_string = letters + numbers
        
        return random_string
    
    car = None

    # Check if the user is a valid user and if they have a car
    if request.user.role == User.USER_ROLE:  # Assuming is_user is a boolean field in the User model
        car = PlateNumber.objects.filter(user=request.user).first()  # Use first() to get the first car or None

    # Check if car exists
        if not car:
            messages.error(request, "Car Is Not Configured, Please Try Again After Configuring")
            return redirect('user_home')
        
    # Create a new ParkingRequest instance
        parking_request = ReservedRequest(
            user=request.user,
            parking=parking_instance,  # Assign the Parking instance
            date=timezone.now().date(),  # Set the date to the current date
            status = False,
            requset_rfe = generate_random_string(),
            plate_number = car.plate_number,
        )
        parking_request.save()

        messages.success(request, 'Your Parking Is Reserved, Wait a few miniute  to get your parking details!')
        return redirect('user_home')  # Adjust to your actual success URL

    