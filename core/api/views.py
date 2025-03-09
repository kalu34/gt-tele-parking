import random
import string

from decimal import Decimal

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError, NotFound, APIException

from authentication.models import Wallet, PlateNumber, Transaction
from core.models import Payment

from django.contrib import messages
from .serializers import ParkingRequestSerializer,ReserveRequestSerializer, ReserveParkingSerializer, ParkingSerialzier
from ..models import ApprovedRequest, ReservedRequest, ReserveParking
from authentication.models import User
from parking.models import Parking, ParkingGroupMember
from user.models import Car
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from ..signals import  parking_request_updated


def generate_random_string():
    # Generate 3 random uppercase letters
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        
        # Generate 3 random digits
        numbers = ''.join(random.choices(string.digits, k=3))
        
        # Combine letters and numbers
        random_string = letters + numbers
        
        return random_string

class ParkingRequestView(APIView):
    def get(self, request):
        parking_admin = ParkingGroupMember.objects.get(user=request.user)
        parking = Parking.objects.get(id=parking_admin.parking.id)
        approved_parking = ApprovedRequest.objects.filter(parking=parking)
        reserve_parking = ReservedRequest.objects.filter(parking=parking)

        reserve_serializer = ReserveRequestSerializer(reserve_parking, many=True)
        approved_serializer = ParkingRequestSerializer(approved_parking, many=True)

        reserve_data = reserve_serializer.data
        approved_data = approved_serializer.data

        for item in reserve_data:
            user_id = item['user']
            user = User.objects.get(id=user_id)
            item['user_name'] = user.username

            try:
                car = Car.objects.get(user=user_id)
                item['car'] = car.plate_number
            except Car.DoesNotExist:
                item['car'] = None  # or some other default value

        for item in approved_data:
            user_id = item['user']
            user = User.objects.get(id=user_id)
            item['user_name'] = user.username

            try:
                car = Car.objects.get(user=user_id)
                item['car'] = car.plate_number
            except Car.DoesNotExist:
                item['car'] = None  # or some other default value

        data = {
            'reserve_parking': reserve_data,
            'approved_parking': approved_data
        }

        return Response(data)



class ParkingRequestStartUpdateView(APIView):
    def patch(self, request, pk):
        parking_request = ApprovedRequest.objects.get(pk=pk)
        parking = parking_request.parking
        serializer = ParkingRequestSerializer(parking_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            parking.available_slots -= 1
            parking.save()
            print('Parking request started successfully')
            return Response({'message': 'Parking request started successfully'})
        return Response(serializer.errors, status=400)


class ParkingRequestStopUpdateView(APIView):
    def patch(self, request, pk):
        parking_request = ApprovedRequest.objects.get(pk=pk)
        
        # Get the start time of the parking request
        start_time = parking_request.start_time
        
        # Get the current time, adjusted for 3-hour difference
        current_time = datetime.now() - timedelta(hours=3)
        
        parking_request.end_time = current_time.strftime("%H:%M")
        
        # Make sure start_time is a datetime object
        if not isinstance(start_time, datetime):
            start_time = datetime.combine(parking_request.date, start_time)
        
        # Calculate the duration in hours
        duration_hours = (current_time - start_time).total_seconds() / 3600
        
        # Get the price per hour from the parking data
        price_per_hour = parking_request.payment_per_hour
        
        # Calculate the total cost
        total_cost = float(duration_hours) * float(price_per_hour)
        
        # Update the total_price field of the parking_request object
        parking_request.total_price = total_cost
        parking_request.stop = False
        parking_request.is_active = False  # Set stop to True
        parking_request.save()

        parking = parking_request.parking
        parking.available_slots += 1
        parking.save()
        
        parking_request_updated.send(sender=ApprovedRequest, instance=parking_request)
        
        return Response({'message': 'Parking request stopped successfully'})
    
    def get(self, request, pk):
        parking_request = ApprovedRequest.objects.get(pk=pk)
        serializer = ParkingRequestSerializer(parking_request)
        return Response(serializer.data)
    

# 0 - Reserving Parking 
# 1. Reserve A parking  -- Done
# 2. Remove If Request Is Not Approved -- Done
# 2.1 Remove Reserved Request
# 3. Stop Request -- Done
# 4. pay  -- Done


class ParkingView(generics.GenericAPIView):  # Change to GenericAPIView for custom response
    serializer_class = ParkingSerialzier

    def get(self, request, id=None): # change to get and add id.
        if id is not None:
            try:
                query = Parking.objects.get(id=id) # Use get() instead of filter().first()
                serializer = self.get_serializer(query) # Use serializer
                return Response({'data': serializer.data}, status=status.HTTP_200_OK)
            except Parking.DoesNotExist:
                return Response({'message': 'No Parking Found In this id'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'please Enter Id'})

class ReserveParkingView(generics.GenericAPIView):
    serializer_class = ReserveParkingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, parking_id):
        try:
           parking = Parking.objects.get(pk=parking_id)
        except Parking.DoesNotExist:
           return Response({"parking_id":"Parking does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = request.user
        validated_data['user'] = user
        validated_data['parking'] = parking
        validated_data['request_ref'] = generate_random_string()

        try:
            plate_number = PlateNumber.objects.get(user=user).plate_number
            validated_data['plate_number'] = plate_number
        except PlateNumber.DoesNotExist:
            return Response({"plate_number":"Plate number not registered for this user."}, status=status.HTTP_400_BAD_REQUEST)

        time_difference = validated_data['end_time'] - validated_data['start_time']
        hours = time_difference.total_seconds() / 3600
        validated_data['total_price'] = Decimal(str(hours)) * parking.price_per_hour

        if ReserveParking.objects.filter(user=user, status=True).exists():
            return Response({'message':"Parking Already Reseved, please reload the page"})
        ReserveParking.objects.create(**validated_data)
        messages.success(request, 'Parking Reserved Successfuly')

        return Response({'message': 'Parking Reserved', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    
class CancelReservedParking(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, reserved_id):
        try:
            parking_reserved = ReserveParking.objects.get(id=reserved_id)
        except ReserveParking.DoesNotExist:
            raise NotFound('No Request Found At This ID')

        if not parking_reserved.payment_status or not parking_reserved.status:
            return Response({'message': 'Parking Request is not active or not paid'}, status=status.HTTP_400_BAD_REQUEST)

        user = parking_reserved.user
        refund_amount = parking_reserved.total_price / Decimal('3.0') 

        try:
            wallet = Wallet.objects.get(user=user)
            wallet.credit(refund_amount)
            wallet.save()

            Transaction.objects.create(
                wallet=wallet,
                amount=refund_amount,
                transaction_ref=parking_reserved.request_ref,
                transaction_type='credit',
                status=True
            )

            parking_reserved.delete()
            messages.success(request, 'Refund Applied Successfuly')
            return Response({'message': 'Reservation Removed and Refund Processed Successfully'}, status=status.HTTP_200_OK)

        except Wallet.DoesNotExist:
            return Response({'message': 'User wallet not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise APIException('Error while refunding, please try again later')


class ReserveParkingRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, parking_id):
        user = request.user
        parking = Parking.objects.get(id=parking_id)



        if user is None:
            raise ValidationError('User is not found')
        
        if parking_id is None or parking is None:
            raise ValidationError('Parking ID is Missing or no parking found in this id')
        
        car = Car.objects.filter(user=user).first()
        if car is None:
            raise ValidationError('Please Configure Car Before Making Any Request')

        active_parking_request = ApprovedRequest.objects.filter(user=request.user, is_active = True)

        if active_parking_request: 
            raise ValidationError('There Is Active Parking For This User')
        
        payment_pending_request = ApprovedRequest.objects.filter(user=user, payment_status = False)
        
        if payment_pending_request:
            raise ValidationError('There Is Payment Pending Request, Please Pay That First')
        
        active_reserved_request = ReservedRequest.objects.filter(user=request.user)

        if active_reserved_request:
            raise ValidationError('There Is Active Reserved Request, Please Remove That and make request again')
        
        try:
            reservedRequest = ReservedRequest(
                user=user,
                parking=parking,
                plate_number= car.plate_number
            )
            reservedRequest.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Parking Request Reserved Successfuly'}, status=status.HTTP_201_CREATED)

class RemoveReservedParkingRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        parking_request = ReservedRequest.objects.filter(id=request_id).first()
    
        if parking_request is None:
            raise ValidationError('No Request Found At This ID')
        
        if parking_request.status:
            raise ValidationError('Request Already Started, You Can Only Stop')
        
        parking_request.delete()

        return Response({'message':'Parking Request Deleted Successfuly'})


class RemoveReservedParking(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, reserved_id):
        parking_reserved = ReserveParking.objects.filter(id=reserved_id).first()
    
        if parking_reserved is None:
            raise ValidationError('No Request Found At This ID')
        
        parking_reserved.delete()
        messages.success(request, 'Reservasion Removed Successfuly')

        return Response({'message':'Parking Request Deleted Successfuly'})


class StopActiveParkingRequest(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):

        parking_request = ApprovedRequest.objects.filter(id=self.kwargs['request_id']).first()
        
        if parking_request is None:
            raise ValidationError('No Approved Request Found In Using This Id')
        
        if parking_request.stop:
            raise ValidationError('Parking request already stopped.')
        
        parking_request.stop = True
        parking_request.save()

        return Response({'message':"parking Request Stop Successfuly"}, status=status.HTTP_202_ACCEPTED)

class PayActiveParkingRequest(APIView):
    permission_classes =[IsAuthenticated]

    def post(self, request, *args, **kwargs):

        parking_request = ApprovedRequest.objects.filter(id=self.kwargs['request_id']).first()

        if parking_request is None:
            raise ValidationError('No Parking Found Using This ID')
        
        if parking_request.payment_status: 
            raise ValidationError('Payment Already Done')
        
        if not parking_request.is_active:
            raise ValidationError('No Active Parking Found')
        
        
        wallet = Wallet.objects.filter(user=request.user).first()

        if wallet is None:
            raise ValidationError('No User Wallet Found')
        
        wallet_pay = wallet.debit(parking_request.total_price, parking_request.reference_trx)

        if (wallet_pay):
            payment = Payment(
            request_id = parking_request,
            tx_ref = parking_request.reference_trx,
            user = request.user,
            amount = parking_request.total_price,
            status = "successful")
            payment.save()

            parking_request.payment_status = True
            parking_request.is_active = False
            parking_request.save()

            return Response({'message':'Payment Done Successfuly'}, status=status.HTTP_202_ACCEPTED)
        
        
        return Response({'message':'Payment can not be done, insuffcient Balance'})
    

