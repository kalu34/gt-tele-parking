from rest_framework import serializers
from rest_framework.serializers import ValidationError
from datetime import datetime, timezone
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


class ReserveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservedRequest
        fields = []


class ReserveParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReserveParking
        fields = ['slot', 'start_time', 'end_time']

    def validate(self, data):
        slot = data.get('slot')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        print(slot, start_time, end_time)

        if not slot:
            raise ValidationError({'slot': ['Slot is required.']})

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

