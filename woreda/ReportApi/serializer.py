from rest_framework import serializers
from parking.models import ParkingGroup, Parking, ParkingGroupMember
from core.models import ApprovedRequest, Payment
from decimal import Decimal

class ParkingGroupSerializer(serializers.ModelSerializer):
  class Meta:
    model = ParkingGroup
    fields = ('__all__')

class ParkingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Parking
    fields = ('__all__')

class ParkingGroupMemberSerializer(serializers.ModelSerializer):
  class Meta:
    model = ParkingGroupMember
    fields = ('__all__')

class ApprovedRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = ApprovedRequest
    fields = ('__all__')


class PaymentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Payment
    fields = ('__all__')


class MonthlyPaymentSerializer(serializers.Serializer):
    total_payments = serializers.FloatField()
    total_customers = serializers.IntegerField()
    month = serializers.IntegerField()


class YearlyPaymentSerializer(serializers.Serializer):
    total_payments = serializers.FloatField()
    total_customers = serializers.IntegerField()
    day = serializers.IntegerField()
    month = serializers.IntegerField()
