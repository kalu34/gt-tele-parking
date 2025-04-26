from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import Parking
from .serializers import ParkingListSerializer , LocationSerializer
from geopy.distance import geodesic



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
    


class NearParkingListView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        location_data = request.query_params
        location_serialiser = LocationSerializer(data=location_data)
        

        if location_serialiser.is_valid():
            
            try: 
                userLocation = (location_serialiser.validated_data['latitude'], location_serialiser.validated_data['longitude'])
                nearParkingList = []
                allParking = Parking.objects.all()

                for parking in allParking:

                    if parking.location.srid != 4326:
                        transformed_location = parking.location.transform(4326, clone=True)
                        parkingLocation = (transformed_location.y, transformed_location.x)
                    else:
                        parkingLocation = (parking.location.y, parking.location.x)

                    distance = geodesic(userLocation, parkingLocation).kilometers

                    if distance <= 1: 
                        parking_serialiser = ParkingListSerializer(parking, context={'request': request})
                        nearParkingList.append(parking_serialiser.data)

                return Response({'mesage':'Data Fetched', 'data': nearParkingList}, status=status.HTTP_200_OK)


            except: 
                print('internal server error')
                return Response({'message':'Internal Server Error'})
        else:
            print('error location datat is not valid')
            return Response({'message': 'Location Data is Not Valid'})
        





        
        