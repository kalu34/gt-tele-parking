from rest_framework import serializers
from ..models import Parking
from core.models import ApprovedRequest

class AbsoluteImageField(serializers.ImageField):
    def to_representation(self, value):
        request = self.context.get('request')
        return request.build_absolute_uri(value.url)

class ParkingListSerializer(serializers.ModelSerializer):
    image1 = AbsoluteImageField()
    image2 = AbsoluteImageField()

    class Meta:
        model = Parking
        fields = '__all__'




class ParkingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovedRequest
        fields = '__all__'  # Or specify the fields you need