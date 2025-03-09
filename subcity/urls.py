from django.urls import path
from . import views
# from .ReportApi.views import *

urlpatterns = [
  # Subcity Url =========================
path('subcity_dashboard', views.subcity_dashboard, name="subcity_dashboard"), 
        # Reqeust
path('subcity_request', views.subcity_request, name="subcity_request"), 
path('subcity_request_detail/<int:id>/', views.subcity_request_detail, name="subcity_request_detail"), 
path('ApproveRequestSubcity/<int:id>/', views.ApproveRequestSubcity, name="ApproveRequestSubcity"), 
path('DeclineRequestSubcity/<int:id>/', views.DeclineRequestSubcity, name="DeclineRequestSubcity"), 
        # Register Woreda Member
path('ViewWoredaAdmin/', views.ViewWoredaAdmin, name="ViewWoredaAdmin"), 
path('AddWoredaAdminsRole/<int:id>/', views.AddWoredaAdminsRole, name="AddWoredaAdminsRole"),
path('AdminWoredaDetail/<int:id>/', views.AdminWoredaDetail, name="AdminWoredaDetail"),
path('RegisterWoreda/<int:id>/', views.RegisterWoreda, name="RegisterWoreda"), 
        # Profile Form
path('subcity_profile', views.subcity_profile, name="subcity_profile"), 
path('subcity_profile_update', views.subcity_profile_update, name="subcity_profile_update"), 

        #==========================Report  =====================
 path('SubcityReport', views.SubcityReport, name="SubcityReport"), 
 path('SubcityWoredaDetailReport/<int:id>/', views.SubcityWoredaDetailReport, name="SubcityWoredaDetailReport"), 
 path('SubcityIncomeReportPerMonth/<int:id>/<str:month_name>/', views.SubcityIncomeReportPerMonth, name="SubcityIncomeReportPerMonth"), 
 path('SubcityIncomReportPerYear/<int:id>', views.SubcityIncomReportPerYear, name="SubcityIncomReportPerYear"), 

 path('SubcityCustomerReportPerDay/<int:id>/', views.SubcityCustomerReportPerDay, name="SubcityCustomerReportPerDay"), 
 path('SubcityCustomerReportPerMonth/<int:id>/<str:month_name>/', views.SubcityCustomerReportPerMonth, name="SubcityCustomerReportPerMonth"), 
 path('SubcityCustomerReportPerYear/<int:id>/', views.SubcityCustomerReportPerYear, name="SubcityCustomerReportPerYear"), 
]