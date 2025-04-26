# ================= Token Based User Registration Done =========================================
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserRegistrationAPIViewSerializer
from rest_framework.authentication import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from authentication.models import User, UserRoles


class UserRegistrationAPIView(generics.GenericAPIView):
    serializer_class = UserRegistrationAPIViewSerializer

    def post(self, request):
        user_data = request.data

        serializer = self.serializer_class(data=user_data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        ('user-login')

        return Response({'message':'user created successfuly','data':serializer.data}, status=status.HTTP_201_CREATED)


class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserRegistrationAPIViewSerializer

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        password = request.data.get('password')

        user = User.objects.filter(phone_number=phone).first()

        if user is None:
            raise AuthenticationFailed({'message':'User Not Found, Invalid credential'})

        if not user.is_active:
            raise AuthenticationFailed({'meesage':'User Is Not Active'})

        if not user.check_password(password):
            raise AuthenticationFailed({'message':'Invalid Password'})

        token = str(user.token)

        login(request, user)        

        return Response({'phone': user.phone_number, 'role': user.role, 'token': token, 'message':'Login Successful'}, status=status.HTTP_200_OK)
    
    
class AdminLoginAPIView(generics.GenericAPIView):
    serializer_class = UserRegistrationAPIViewSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed('User Not Found, Invalid credientail')
        
        if not user.is_active:
            raise AuthenticationFailed('User Is Not Active')
        
        if user.is_verified:
            raise AuthenticationFailed('User Email is not verified')
        
        response = Response({'username':user.username, 'role':user.role})

        response.set_cookie('access_token', value=user.token, 
                httponly=False, 
                secure=True,    
                samesite='Lax', 
                path='/',)
        login(request, user)
    
        return response

    
class UserLogout(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            response = Response(status=status.HTTP_204_NO_CONTENT) # 204 No Content is appropriate here
            response.delete_cookie('access_token') # Clear refresh token cookie
            user = request.user # Get user before logout
            logout(request)
            return response
        
        except Exception as e:
            print(e) # Log the exception for debugging
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckPhoneNumber(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')

        if User.objects.filter(phone_number = phone).exists():
            return Response({'message':'Phone Number Already Exist'}, status=status.HTTP_400_BAD_REQUEST)

        
        return Response({'message':'New phone number'}, status=status.HTTP_202_ACCEPTED)



def loginView(request):
    return render(request, 'UserLogin.html')

def landingPageView(request):
    return render(request, 'index.html')

def userRegisterView(request):
    return render(request, 'registerUser.html')

def adminLoginView(request):
    return render(request, 'AdminLogin.html')

def removeRole(request, id):
    current_user = request.user
    user = User.objects.filter(id=id).first()
    role = UserRoles.objects.filter(user=user).first()

    if role: 
        role.delete()
        messages.success(request,'Role Removed')

        if current_user.role == 5:
            return redirect('ViewSubcityAdmins')
        else:
            return redirect('ViewWoredaAdmins')


# ================= Session Based User Login Done ======================================

def changePassword(request):
    if request.method == 'POST':
        currentPassword = request.POST['currentPassword']
        newPassword = request.POST['newPassword']
        confirmPassword = request.POST['confirmPassword']

        user = request.user

        if newPassword != confirmPassword:
            messages.error( request, 'password do not match ')
            return
        if not user.check_password(currentPassword):
            messages.error(request, 'Current Password Incorrect')
            return
        user.set_password(newPassword)
        user.save()
        logout(request)
        messages.success(request,'password changed successfuly')

        if user.role == 1:
            return redirect('/user-login')
        
        return redirect('/admin')

        

