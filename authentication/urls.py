from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView,UserLogout,AdminLoginAPIView,CheckPhoneNumber, loginView, landingPageView,userRegisterView,adminLoginView, changePassword, logout, removeRole



urlpatterns = [
    # Defalut Route
    path('', landingPageView, name="landing-page"),
    path('admin/', adminLoginView, name="admin"),
    path('user-login', loginView, name="user-login"),

    path('user-register', userRegisterView, name="user-register"),
    path('user-regiseter-api', UserRegistrationAPIView.as_view(), name="customer-register"),
    path('user-login-api', UserLoginAPIView.as_view(), name="user-login-api"),
    path('admin-login-api', AdminLoginAPIView.as_view(), name="admin-login-api"),
    path('user-logout', UserLogout.as_view(), name="user-logout"),

    path('check_phone_number', CheckPhoneNumber.as_view(), name='check_phone_number'),

    path('logout', logout, name="logout"),

    path('change_password', changePassword, name="change_password"),

    path('remove-role/<int:id>/', removeRole, name="remove-role")
]