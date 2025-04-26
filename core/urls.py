from django.urls import path
from .api.views import *
from . import views

urlpatterns = [
    path('parking-requests/', ParkingRequestView.as_view()),
    path('parking-requests/<pk>/', ParkingRequestStartUpdateView.as_view()),
    path('parking-requests-stop/<int:id>/', ParkingRequestStopUpdateView.as_view()),

    path('reserve_parkng/<int:id>', views.reserve_parking, name="reserve_parkng"),

    path('api/parking/<int:id>', ParkingView.as_view()),
    path('api/reserve-parking-appointment/<int:parking_id>/', ReserveParkingView.as_view()),
    path('api/cancel-reserved-parking/<int:reserved_id>/', CancelReservedParking.as_view()),
    path('api/reserve-parking/<int:parking_id>/', ReserveParkingRequest.as_view()),
    path('api/remove-parking-reservasion/<int:reserved_id>/', RemoveReservedParking.as_view(), name="remove-parking-reservasion"),
    path('api/remove-parking-request/<int:request_id>/', RemoveReservedParkingRequest.as_view()),
    path('api/stop-active-parking-request/<int:request_id>/', StopActiveParkingRequest.as_view()),
    path('api/pay-active-parking-request/<int:request_id>/', PayActiveParkingRequest.as_view()),
    #  Mobile App Api

    path('api/mobile/reserve-parking', ReserveParkingAPI.as_view(), name="api/mobile/reserve-parking"),
    path('api/mobile/check-reserve', CheckReserve.as_view(), name="Check-Reserve"),
    path('api/mobile/filter-reservasion', FilterReservasion.as_view(), name='filter-reservasion')

]