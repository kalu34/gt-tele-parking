from rest_framework import generics
from .serializer import *
from parking.models import Parking, ParkingGroup, ParkingGroupMember
from core.models import Parking, ReservedRequest, ApprovedRequest, Payment
from django.db.models.functions import ExtractDay
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# 
from datetime import datetime, timedelta
from django.db.models import Q


def get_current_user_payment_list(self):
  queryset = Payment.objects.filter(status = 'successful', request_id__parking__parking_group__subcity = self.request.user.subcity)
  return queryset


class TotalIncome(generics.ListAPIView):
    def get_queryset(self):
        payment = Payment.objects.filter(status = 'successful', request_id__parking__parking_group__subcity = self.request.user.subcity)
        status = self.kwargs.get('range')
        if status == "day": 
          queryset = payment.filter(date__date=datetime.now().date())
        elif status == "month":
           queryset = payment.filter(date__month = datetime.now().month)
        elif status == 'year':
           queryset = payment.filter(date__year = datetime.now().year)
        return queryset
    serializer_class = PaymentSerializer

class TotalIncomePerMonth(generics.ListAPIView):
    serializer_class = PaymentSerializer
    def get_queryset(self):
        payment = Payment.objects.filter(status='successful', request_id__parking__parking_group__subcity=self.request.user.subcity)
        month = self.kwargs.get('month')  # Assuming you pass the month as 'id' in the URL
        queryset = payment.filter(date__year = datetime.now().year, date__month=month)
        return queryset

class TotalUser(generics.ListAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        # Get the current user
        user_subcity = self.request.user.subcity

        # Filter payments for the user's subcity and successful status
        payment_queryset = Payment.objects.filter(
            status='successful',
            request_id__parking__parking_group__subcity=user_subcity
        )

        # Determine the range (day, month, year) from URL kwargs
        range_filter = self.kwargs.get('range')
        if range_filter == "day":
            payment_queryset = payment_queryset.filter(date__date=datetime.now().date())
        elif range_filter == "month":
            payment_queryset = payment_queryset.filter(date__month=datetime.now().month)
        elif range_filter == "year":
            payment_queryset = payment_queryset.filter(date__year=datetime.now().year)

        # Ensure only unique users are included in the result
        return payment_queryset.distinct('user')



class ApprovedParkingRequest(generics.ListAPIView):
  def get_queryset(self):
        payment = Payment.objects.filter(status = 'successful', request_id__parking__parking_group__subcity = self.request.user.subcity)
        status = self.kwargs.get('range')
        if status == "day": 
          queryset = payment.filter(date__date=datetime.now().date())
        elif status == "month":
           queryset = payment.filter(date__month = datetime.now().month)
        elif status == 'year':
           queryset = payment.filter(date__year = datetime.now().year)
        return queryset
  serializer_class = PaymentSerializer

 

from django.db.models import Sum, Func, F, IntegerField
from calendar import month_name

class ExtractMonth(Func):
    function = 'EXTRACT'
    template = "%(function)s(MONTH FROM %(expressions)s)"
    output_field = IntegerField()

class CityReportDashboard(generics.ListAPIView):
    serializer_class = MonthlyPaymentSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        year = self.kwargs.get('year')

        if not year:
            return

        queryset = (
            Payment.objects.filter(status='successful', date__year=year)
            .annotate(month=ExtractMonth(F('date')))  # Extract month as an integer
            .values('month')
            .annotate(
                total_payments=Sum('amount'),
                total_customers=Sum(1)
            )
            .order_by('month')
        )
        return queryset
    
class CityReportDasboardDetail(generics.ListAPIView):
    serializer_class = YearlyPaymentSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        year = self.kwargs.get('year')  # Use get() to safely retrieve kwargs
        month = self.kwargs.get('month')

        if not year or not month:
            return []  # Return an empty list instead of None

        queryset = (
            Payment.objects.filter(status='successful', date__year=year, date__month=month)
            .annotate(day=ExtractDay('date'))
            .extra(select={'month': month})
            .values('day', 'month')  # Use values() to get a dictionary of values
            .annotate(
                total_payments=Sum('amount'),
                total_customers=Sum(1),
            )
            .order_by('day')
        )
        return queryset

   