import random
import string

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from chapa import Chapa

from authentication.models import User, Wallet, Transaction
from parking.models import Parking
from core.models import Payment
from core.context_processors import global_settings
from user.models import LegalDocument

from .serializers import *


def generate_random_string():
    # Generate 3 random uppercase letters
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        # Generate 3 random digits
        numbers = ''.join(random.choices(string.digits, k=3))
        # Combine letters and numbers
        random_string = letters + numbers
        return random_string
     

key = 'CHASECK_TEST-doJ2DjZLsviBfWL6sK0U0JkDqpGOZZ3s'
chapa = Chapa(key)

class chapaPayView(generics.ListAPIView):
  permission_classes = [IsAuthenticated]

  
  
  def post(self, request, *args, **kwargs):
    context = global_settings(request)  # Manually call the processor
    api_url = context.get('API_URL')  # Extract the API_URL
    amount = request.data.get('amount')
    tx_refs = generate_random_string()
    response = chapa.initialize(
    email=request.user.email,
    amount=amount,
    first_name=request.user.first_name,
    last_name=request.user.last_name,
    tx_ref=tx_refs,
    callback_url=f"{api_url}/chapa_verify_payment", 
    return_url=f"{api_url}/user_wallet" 
    )
    wallet = Wallet.objects.get(user=request.user)
    if wallet: # Check if wallet exists
        wallet.create_transaction(amount, tx_refs)
    return Response({"message":"You have paid", 'response':response})
  
from urllib.parse import urlparse, parse_qs  # Import for better URL parsing

from rest_framework import generics
from rest_framework.permissions import AllowAny  # Or IsAuthenticated if needed
from rest_framework.response import Response
from urllib.parse import urlparse, parse_qs
from django.contrib import messages


class VerifyChapaPayment(generics.GenericAPIView):
    permission_classes = [AllowAny]  # Or IsAuthenticated

    def get(self, request, *args, **kwargs):
        try:
            full_url = request.build_absolute_uri()
            parsed_url = urlparse(full_url)
            query_params = parse_qs(parsed_url.query)

            tx_ref = query_params.get('trx_ref', [None])[0]
            status = query_params.get('status', [None])[0]

            if status == "success":
                transaction = Transaction.objects.filter(transaction_ref = tx_ref).first()
                wallet = transaction.wallet
                wallet.credit(transaction.amount)
                transaction.status = True
                transaction.save()
                print('payment done')
            return Response({"message": "Wallet Credit Successful"}, status=200)

        except Exception as e:
            print(f"Error processing callback: {e}")
            return Response({"message": "Error processing callback"}, status=500)

#======================= 
# User Page Activities 
# 5. All Parking List - Done
# History  - Done
#  Payment List - Done
# 6. Wallet Configuration 
# 7. Profile - Done
# Car Information -- Done
# And Legal Informaiotn  --Done 

class ViewParkingLIst(generics.ListAPIView):
    serializer_class = ViewParkingListSerializer
    queryset = Parking.objects.all()
    permission_classes = [IsAuthenticated]


class ViewUserHistory(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewUserHistorySerializer

    def get_queryset(self):
        queryset = Payment.objects.filter(user=self.request.user, status="successful")
        return queryset
    
class ViewUserPayment(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewUserHistorySerializer

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
# Profile View

class ViewProfile(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerialiser

    def get_object(self):
        return self.request.user 

class ViewProfilePicture(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfilePictureSerializer

    def get_object(self): 
        return get_object_or_404(Profile, user=self.request.user)
    
class UpdateProfile(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerialiser

    def get_object(self):
        user_id = self.kwargs['user_id']
        return get_object_or_404(User, id=user_id)
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# Car View
class ViewUserCar(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateCarSerializer

    def get_queryset(self):
        return Car.objects.filter(user=self.request.user)
    
class CreateCar(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCarSerializer

    def perform_create(self, serializer): 
        serializer.save(user=self.request.user) 

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)  # Call perform_create
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except ValidationError as e:  # Catch validation errors
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e: # Catch other exceptions
            return Response({"detail": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateCar(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateCarSerializer
    lookup_url_kwarg = 'car_id'

    def get_object(self):
        car_id = self.kwargs['car_id']
        return get_object_or_404(Car, id=car_id, user=self.request.user)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Car updated successfully'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewLegalDocument(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = LegalDocumentSerializer
    def get_object(self):
        return get_object_or_404(Car, user=self.request.user)
    
    def get_queryset(self):
        return LegalDocument.objects.filter(car=self.get_object())

class CreateLegalDocument(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LegalDocumentSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def perform_create(self, serializer):
        try:
            car = get_object_or_404(Car, user=self.request.user)
            serializer.save(car=car)
        except ObjectDoesNotExist:
            raise ValidationError("Car not found for this user.")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(): 
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class UpdateLegalDocument(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LegalDocumentSerializer

    def patch(self, request, *args, **kwargs):
        try: 
            instance = get_object_or_404(LegalDocument, id = self.kwargs['document_id'])
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'FIle updated successfully'}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            raise ValidationError('Document Dont Exist At This Id')
        

