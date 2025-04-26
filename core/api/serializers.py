from rest_framework import serializers
from rest_framework.serializers import ValidationError
from datetime import datetime, timedelta, timezone
from ..models import ApprovedRequest, ReservedRequest, ReserveParking
from user.models import Car
from parking.models import Parking

class ParkingSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = '__all__'


class ParkingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovedRequest
        fields = '__all__'


class SerialiserReserveParking(serializers.ModelSerializer):
    class Meta:
        model = ReserveParking
        fields = '__all__'


class ReserveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservedRequest
        fields = []


class ReserveParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReserveParking
        fields = ['start_time', 'end_time']

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        print(start_time, end_time)

        if not start_time:
            raise ValidationError({'start_time': ['Start time is required.']})
        
        if not end_time:
            raise ValidationError({'end_time': ['End time is required.']})

        if start_time and end_time:
            if start_time >= end_time:
                raise ValidationError({'end_time': ['End time must be after start time.']})

            now = datetime.now(timezone.utc)
            if start_time < now:
                raise ValidationError({'start_time': ['Start time cannot be in the past.']})

        return data

    def get_fields(self):
        fields = super().get_fields()
        fields['start_time'].style = {'input_type': 'datetime-local', 'min': datetime.now(timezone.utc).isoformat(timespec='minutes')}
        return fields



from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import datetime, timezone

class ParkingReserveSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()

    def validate(self, attrs):
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')

        modified_date = start_time + timedelta(minutes=5)

        if not modified_date:
            raise ValidationError({'start_time': ['Start time is required.']})

        if not end_time:
            raise ValidationError({'end_time': ['End time is required.']})

        if modified_date and end_time:
            if modified_date >= end_time:
                raise ValidationError({'end_time': ['End time must be after start time.']})

            now = datetime.now(timezone.utc)
            if modified_date < now:
                raise ValidationError({'start_time': ['Start time cannot be in the past.']})

        return attrs


