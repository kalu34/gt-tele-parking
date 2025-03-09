from rest_framework import generics
from ..models import Parking
from .serializers import ParkingListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from core.models import ApprovedRequest
from .serializers import ParkingRequestSerializer


class ParkingListView(generics.ListAPIView):
    queryset = Parking.objects.all()
    serializer_class = ParkingListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request  # Pass the request to the context
        return context

from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ParkingRequestSerializer
from collections import defaultdict
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth

class ParkingIncomeReportView(APIView):
    def get(self, request, time_frame):
        # Get the current date and time
        now = timezone.now()
        today = now.date()  # Get today's date

        # Initialize a dictionary to store data
        report_data = {}

        if time_frame == 'day':
            # Fetch the parking requests for today
            parking_requests = ApprovedRequest.objects.filter(date=today)
            total_value = sum(item.total_price for item in parking_requests if request.total_price is not None)
            unique_customers_count = parking_requests.values('user__email').distinct().count()

            # Store the data in the report_data dictionary
            report_data[str(today)] = {
                'total_value': total_value,
                'total_customers': unique_customers_count,
                'requests': ParkingRequestSerializer(parking_requests, many=True).data,
            }

        elif time_frame == 'week':
            start_date = now - timedelta(weeks=1)

            # Loop through each day in the past week
            for i in range(7):
                date = (start_date + timedelta(days=i)).date()
                # Fetch the parking requests for that specific day using __date lookup
                parking_requests = ApprovedRequest.objects.filter(date=date)
                total_value = sum(request.total_price for request in parking_requests if request.total_price is not None)
                unique_customers_count = parking_requests.values('user__email').distinct().count()

                # Store the data in the report_data dictionary
                report_data[str(date)] = {
                    'total_value': total_value,
                    'total_customers': unique_customers_count,
                    'requests': ParkingRequestSerializer(parking_requests, many=True).data,
                }

        elif time_frame == 'month':
            # Fetch all parking requests and group by month
            monthly_data = ApprovedRequest.objects.annotate(month=TruncMonth('date')).values('month').annotate(
                total_value=Sum('total_price'),
                total_customers=Count('user__email', distinct=True)
            ).order_by('month')

            # Prepare the report data
            for entry in monthly_data:
                month_key = entry['month'].strftime('%Y-%m')
                report_data[month_key] = {
                    'total_value': entry['total_value'] or 0,  # Default to 0 if None
                    'total_customers': entry['total_customers'],
                }

        else:
            return Response({"error": "Invalid time frame"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(report_data, status=status.HTTP_200_OK)