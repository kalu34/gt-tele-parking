from django.urls import path
from . import views
from .ReportApi.views import *

urlpatterns = [
path('City_Dashboard', views.City_Dashboard, name="City_Dashboard"),
# Dashboard API
path('CityReportDashboard/<int:year>/', CityReportDashboard.as_view(), name="CityReportDashboard"),
path('YearlyPaymentSerializer/<int:year>/<int:month>/', CityReportDasboardDetail.as_view(), name="YearlyPaymentSerializer"),
# ---- Subcity Admins Views
path('ViewSubcityAdmins', views.ViewSubcityAdmins, name="ViewSubcityAdmins"),
path('AddSubcityAdmins/<int:id>/', views.AddSubcityAdmins, name="AddSubcityAdmins"),
path('AddSubcityAdminsRole/<int:id>/', views.AddSubcityAdminRole, name="AddSubcityAdminsRole"),
path('AdminSubcityDetail/<int:id>/', views.AdminSubcityDetail, name="AdminSubcityDetail"),
path('RemoveSubcityAdmin/<int:id>/', views.RemoveSubcityAdmin, name="RemoveSubcityAdmin"),
# ---- Report City
path('CityIncomeReportPerDay/<str:subcity>/<int:woreda>/', views.CityIncomeReportPerDay, name="CityIncomeReportPerDay"),
path('CityIncomeReportPerMonth/<str:subcity>/<int:woreda>/<str:month>/', views.CityIncomeReportPerMonth, name="CityIncomeReportPerMonth"),
path('CityIncomeReportPerYear/<str:subcity>/<int:woreda>/', views.CityIncomeReportPerYear, name="CityIncomeReportPerYear"),
path('CityCustomerReportPerDay/<str:subcity>/<int:woreda>/', views.CityCustomerReportPerDay, name="CityCustomerReportPerDay"),
path('CityCustomerReportPerMonth/<str:subcity>/<int:woreda>/<str:month>/', views.CityCustomerReportPerMonth, name="CityCustomerReportPerMonth"),
path('CityCustomerReportPerYear/<str:subcity>/<int:woreda>/', views.CityCustomerReportPerYear, name="CityCustomerReportPerYear"),
#  ---- Report Base
path('SubcityReportView', views.SubcityReportView, name="SubcityReportView"),
path('WoredaReportView/<str:subcity>/', views.WoredaReportView, name="WoredaReportView"),

#  Request Views
path('CItyViewApprovedRequest', views.ViewApprovedRequest, name="CItyViewApprovedRequest"),
path('CItyViewDeclinedRequest', views.ViewDeclinedRequest, name="CItyViewDeclinedRequest"),
path('CItyAllRequest', views.AllRequest, name="CItyAllRequest"),

# parking Group
path('CityParkingGroupView', views.CityParkingGroupView, name="CityParkingGroupView"),
path('CityParkingGroupDetailView/<int:id>/', views.CityParkingGroupDetailView, name="CityParkingGroupDetailView"),
# Parkings
path('CityParkingView', views.CityParkingView, name="CityParkingView"),
path('CityParkingViewDetail/<int:id>/', views.CityParkingViewDetail, name="CityParkingViewDetail"),
# Incident View 
path('CityIncidentView', views.CityIncidentView, name="CityIncidentView"),
# Profile Edit
path('CityProfile', views.CityProfile, name="CityProfile"),
path('CityProfileUpdate', views.CityProfile, name="CityProfile"),
]