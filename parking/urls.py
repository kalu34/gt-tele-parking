from django.contrib import admin
from django.urls import path
from . import views
from .api.views import ParkingListView,ParkingIncomeReportView

urlpatterns = [
    path('parking_home', views.parking_home, name='parking_home'),
    path('parking_request', views.parking_request, name='parking_request'),
    path('parking_approved_request', views.parking_request_approved, name='parking_approved_request'),
    path('parking_new_request_detail/<int:id>/', views.parking_new_request_detail, name='parking_new_request_detail'),
    path('parking_approved_request_detail/<int:id>/', views.parking_approved_request_detail, name='parking_approved_request_detail'),
    path('parking_new_approve_request/<int:id>/', views.parking_new_approve_request, name='parking_new_approve_request'),
    path('parking_approve_request_stop/<int:id>/', views.parking_approve_request_stop, name='parking_approve_request_stop'),
    path('parking_payment', views.parking_payment, name='parking_payment'),
    path('cash_payment/<int:id>/', views.cash_payment, name='cash_payment'),
    path('parking_history', views.parking_history, name='parking_history'),
    path('parking_report', views.parking_report, name='parking_report'),
    # Parking Data Profile
    path('parking_profile', views.parking_profile, name='parking_profile'),
    path('parking_password', views.parking_password, name='parking_password'),
    path('parking_data', views.parking_data, name='parking_data'),
    path('incident_report/<int:id>/<int:id2>/', views.incident_report, name='incident_report'),
    path('parking_working_hour', views.parking_working_hour, name='parking_working_hour'),
    path('toggle_working_day/<int:id>/', views.toggle_working_day, name='toggle_working_day'),
    path('update_working_hour/<int:id>/', views.update_working_hour, name='update_working_hour'),

    # API
    path('parking-list/', ParkingListView.as_view(), name='mymodel-list'),
    path('near_parking/', views.NearestParkingView.as_view(), name="near_parking" ),
    path('api/report_income/<str:time_frame>/', ParkingIncomeReportView.as_view(), name='parking_report'),
    # Request Sent

    path('request_send', views.request_send, name='request_send'),
]