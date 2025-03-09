from django.urls import path
from . import views
from .ReportApi.views import *
urlpatterns = [
#   Woreda Url 
path('woreda_dashboard', views.woreda_dashboard, name="woreda_dashboard"),
path('woreda_parking_register', views.woreda_parking_register, name="woreda_parking_register"),
path('RegisterParkingGroupDetail/<int:id>/', views.RegisterParkingGroupDetail, name="RegisterParkingGroupDetail"),
path('ViewParkingMember/<int:id>/', views.ViewParkingMember, name="ViewParkingMember"),
path('RegisterParkingGroupMember/<int:id>/<int:id2>/', views.RegisterParkingGroupMember, name="RegisterParkingGroupMember"),
path('RegisterParking/<int:id>/<slug:status>/', views.RegisterParking, name="RegisterParking"),

            #  Woreda Requst Url

path('RequestList', views.requestList, name ="RequestList"),
path('requestListDetail/<int:id>/', views.requestListDetail, name = "requestListDetail"),
path('sendRequestWoreda/<int:id>/<int:id_2>/', views.sendRequestWoreda, name = "sendRequestWoreda"),

        #  Deleted Instance and Review Page
path('InstanceDelete/<int:id>/<int:id_2>/<int:id_3>/', views.InstanceDelete, name="InstanceDelete"),
path('ViewDeletedInstance', views.ViewDeletedInstance, name="ViewDeletedInstance"),
path('ViewDeletedInstanceParking', views.ViewDeletedInstanceParking, name="ViewDeletedInstanceParking"),
path('ViewDeletedInstanceParkingMember', views.ViewDeletedInstanceParkingMember, name="ViewDeletedInstanceParkingMember"),

        # Report API View
 path('TotalIncome/<str:range>/', TotalIncome.as_view(), name='total-Income-per-day'),
 path('TotalIncomePerMonth/<int:month>/', TotalIncomePerMonth.as_view(), name='total-Income-per-day'),
 path('TotalUser/<str:range>/', TotalUser.as_view(), name='total-customer-per-day'),
 path('ApprovedParkingRequest/<str:range>/', ApprovedParkingRequest.as_view(), name='total-customer-per-day'),

        # Report View 
path('IncomeReportWoredaPerDay', views.IncomeReportWoredaPerDay, name="IncomeReportWoredaPerDay"),
path('IncomeReportWoredaPerMonth/<int:id>/', views.IncomeReportWoredaPerMonth, name="IncomeReportWoredaPerMonth"),
path('IncomeReportWoredaPerYear', views.IncomeReportWoredaPerYear, name="IncomeReportWoredaPerYear"),
                # Report On Customer 
path('CustomerReportWoredaPerDay', views.CustomerReportWoredaPerDay, name="CustomerReportWoredaPerDay"),
path('CustomerReportWoredaPerMonth/<int:id>/', views.CustomerReportWoredaPerMonth, name="CustomerReportWoredaPerMonth"),
path('CustomerReportWoredaPerYear', views.CustomerReportWoredaPerYear, name="CustomerReportWoredaPerYear"),
                # Report On Incident
path('IncidentReportWoredaPerDay', views.IncidentReportWoredaPerDay, name="IncidentReportWoredaPerDay"),
path('IncidentReportWoredaPerMonth/<int:id>/', views.IncidentReportWoredaPerMonth, name="IncidentReportWoredaPerMonth"),
path('IncidentReportWoredaPerYear', views.IncidentReportWoredaPerYear, name="IncidentReportWoredaPerYear"),

                # Report On Parking
path('ParkingReportWoredaPerDay', views.ParkingReportWoredaPerDay, name="ParkingReportWoredaPerDay"),
                #Profile Page
path('WoredaProfile', views.WoredaProfile, name="WoredaProfile"), 
                #Notification Notification 
path('WoredaNotificationIncident', views.WoredaNotificationIncident, name="WoredaNotificationIncident"), 
path('WoredaNotificationIncidentDetail/<int:id>/', views.WoredaNotificationIncidentDetail, name="WoredaNotificationIncidentDetail"), 
path('WoredaNotificationChangePrice', views.WoredaNotificationChangePrice, name="WoredaNotificationChangePrice"), 
path('WoredaNotificationRequest', views.WoredaNotificationRequest, name="WoredaNotificationRequest"), 


]