from rest_framework import serializers
from parking.models import Parking
from core.models import Payment, ApprovedRequest
from user.models import Car, LegalDocument
from authentication.models import User, Profile

class ViewParkingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = '__all__'

class RequestSerializerWithParking(serializers.ModelSerializer):
    # parkings = ViewParkingListSerializer(many=True, read_only=True)

    class Meta:
        model = ApprovedRequest
        fields = ['slot']

class ViewUserHistorySerializer(serializers.ModelSerializer):
    request_id = RequestSerializerWithParking(read_only = True)

    class Meta:
        model = Payment
        fields = '__all__'


# Profile Serializer

class ProfileSerialiser(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class ProfilePictureSerializer(serializers.ModelSerializer):
    user = ProfileSerialiser(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'

 
# Car Serializer
class CreateCarSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) # Make user read-only

    class Meta:
        model = Car
        fields = '__all__'  # or specify the fields you want

    def validate(self, attrs):

        user = attrs.get('user')  # Use attrs.get('user') to access user

        if Car.objects.filter(user=user).exists():
            raise serializers.ValidationError("Car With This User Already Exist")

        return attrs
    
class UpdateCarSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Car
        fields = '__all__'

# Legal Document Serialzier

class LegalDocumentSerializer(serializers.ModelSerializer):
    car = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = LegalDocument
        fields = '__all__'