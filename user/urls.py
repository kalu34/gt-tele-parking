from django.urls import path
from . import views
from .api.views import *

urlpatterns = [
    path('user_home/', views.user_home, name='user_home'), 
    path('user_listing/', views.user_listing, name='user_listing'), 
    path('remove_request/<int:request_id>', views.remove_request, name='remove_request'), 
    path('stop_request/<int:request_id>', views.stop_request, name='stop_request'), 
    path('user_history', views.user_history, name='user_history'), 
    path('user_payment', views.user_payment, name='user_payment'), 
    path('create_payment', views.create_payment, name='create_payment'), 

    # Pay
    path('chapa_deposit', chapaPayView.as_view()),
    path('chapa_verify_payment', VerifyChapaPayment.as_view()),
    path('pay_now/<int:id>', views.pay_now, name="pay_now" ),
    path('pay_reserve_now/<int:id>', views.pay_reserve_now, name="pay_reserve_now"),
    # Profile Edit User

    path('user_wallet', views.user_wallet, name="user_wallet"),

    # Profile Urls
    path('user_profile', views.user_profile, name='user_profile'), 
    path('create_or_update_car/<int:user_id>', views.create_or_update_car, name='create_or_update_car'), 
    path('create_or_update_user_profile/<int:user_id>', views.create_or_update_user_profile, name='create_or_update_user_profile'), 
    path('create_or_update_user_profile_image/<int:user_id>', views.create_or_update_user_profile_image, name='create_or_update_user_profile_image'), 
    path('create_or_update_document/<int:user_id>', views.create_or_update_document, name='create_or_update_document'), 

    # API URl --------
    path('api/list-parking', ViewParkingLIst.as_view()),
    path('api/view-user-history', ViewUserHistory.as_view()),
    path('api/view-user-payment', ViewUserPayment.as_view()),

    path('api/user-profile', ViewProfile.as_view()),
    path('api/user-profile-picture', ViewProfilePicture.as_view()),
    path('api/user-profile-update/<int:user_id>/', UpdateProfile.as_view()),

    path('api/list-car', ViewUserCar.as_view()),
    path('api/create-car', CreateCar.as_view()),
    path('api/update-car/<int:car_id>/', UpdateCar.as_view()),

    path('api/user-legal-document', ViewLegalDocument.as_view()),
    path('api/user-create-legal-document', CreateLegalDocument.as_view()),
    path('api/user-update-legal-document/<int:document_id>/', UpdateLegalDocument.as_view()),

]