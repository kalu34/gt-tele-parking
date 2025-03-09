from authentication.models import User, PlateNumber
from rest_framework import serializers
from django.core.validators import validate_email
import re

class UserRegistrationAPIViewSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=2, read_only=True)
    plate_number = serializers.CharField(max_length=6, write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'phone_number', 'plate_number', 'role']
        extra_kwargs = {'password': {'write_only': True}} # Important: hide password on responses

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        phone_number = attrs.get('phone_number')
        plate_number = attrs.get('plate_number') #Get plate number
        errors = {}

        # Name Validation (First and Last)
        if not first_name:
            errors['first_name'] = "First name is required."
        elif not re.match(r'^[a-zA-Z\s]+$', first_name):  # Allows only letters and spaces
            errors['first_name'] = "First name can only contain letters and spaces."

        if not last_name:
            errors['last_name'] = "Last name is required."
        elif not re.match(r'^[a-zA-Z\s]+$', last_name):  # Allows only letters and spaces
            errors['last_name'] = "Last name can only contain letters and spaces."

        # Phone Number Validation
        if not phone_number:
            errors['phone_number'] = "Phone number is required."
        elif not re.match(r'^\+?[0-9]+$', phone_number):  # Allows + and numbers. You might want stricter pattern
            errors['phone_number'] = "Invalid phone number format. Only digits and optionally a leading '+' are allowed."
        elif len(phone_number) < 7:  # Example minimum length
            errors['phone_number'] = "Phone number is too short."
        elif len(phone_number) > 11:  # Example maximum length
            errors['phone_number'] = "Phone number is too long."
        #Plate number validation
        if not plate_number:
            errors['plate_number'] = "Plate number is required."
        elif len(plate_number) > 6:
            errors['plate_number'] = "Plate number is too long."
        elif len(plate_number) < 1:
            errors['plate_number'] = "Plate number is too short"

        if errors:  # If there are any errors
            raise serializers.ValidationError(errors)  # Raise a validation error to be handled by DRF

        return attrs  # Return the validated attributes if no errors

    def create(self, validated_data):
        plate_number = validated_data.pop('plate_number', None) 

        if plate_number: 
            if PlateNumber.objects.filter(plate_number=plate_number).exists():
                raise serializers.ValidationError('Plate Number Alreday Exisist')
            
            user = User.objects.create_user(**validated_data)
            PlateNumber.objects.create(user=user, plate_number=plate_number) 


        return user