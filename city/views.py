from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from authentication.forms import UserForm, ProfileForm, RoleForm
from authentication.models import User, Profile, UserRoles, Woreda
from core.models import Request, ApprovedRequestAdmin, DecliendRequestAdmin, DeletedInstance, ApprovedRequest

# Woreda Import 
from parking.models import ParkingGroup, ParkingGroupMember, Parking
from authentication.forms import UserForm
from authentication.models import User, UserRoles, Subcity, Woreda
from core.models import Payment, Incident
from datetime import datetime
from user.models import Car

# Rest Framework 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# Exception
from django.core.exceptions import ObjectDoesNotExist

# Paginator and Pagination Applied Here
from django.core.paginator import Paginator
# Decorator
from authentication.RoleDecorator.decorators import role_auth_decorator

# Create your views here.
# ====================================== CITY VIEWS  ============ \
@role_auth_decorator(role=5)
@permission_classes([IsAuthenticated])
def City_Dashboard(request):
    # 12 Month Report 
    total_user = User.objects.filter(role = 1).count()
    total_income = Payment.objects.filter(status="successful").order_by('date')
    total_parking = Parking.objects.all().count()
    total_parking_group = ParkingGroup.objects.all().count()

    IncomePaginatorObject = Paginator(total_income.filter(date__date=datetime.now().date()), 5)
    page = request.GET.get('page')
    total_incomes = IncomePaginatorObject.get_page(page)


    context = {
        'total_user':total_user,
        'total_income_count': sum(item.amount for item in total_income),
        'IncomeReport': total_incomes,
        'total_parking':total_parking,
        'total_parking_group':total_parking_group
    }

    return render(request, 'City/CityDashboard.html', context)

@role_auth_decorator(role=5)
def ViewSubcityAdmins(request):
    subcityAdmins = User.objects.filter(role = 4)
    subcityAdminPaginatorObject = Paginator(subcityAdmins, 5)
    page = request.GET.get('page')
    subcityAdminPaginator = subcityAdminPaginatorObject.get_page(page)

    user_with_role = []

    for user in subcityAdminPaginator:
        role = UserRoles.objects.filter(user=user).first()
        user_with_role.append({'user':user, 'role':role})

    context = {
        'user_with_role':user_with_role,
        'subcityAdmins':subcityAdminPaginator
    }
    return render(request, 'City/Admins/ViewSubcityAdmins.html', context)

@role_auth_decorator(role=5)
def AddSubcityAdmins(request, id):
    user = User.objects.filter(id=id).first() 
    role = UserRoles.objects.filter(user=user).first()

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.set_password('123')
            form_instance.role = 4  
            form_instance.save()
            messages.success(request, 'operatin successful')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.warning(request, f"{error}")

    else:
        form = UserForm(instance=user) 

    context = {
        'form': form,
        'user_id': id,
        'role':role,
    }

    return render(request, 'City/Admins/AddSubcityAdmins.html', context)

@role_auth_decorator(role=5)
def AddSubcityAdminRole(request, id):
    user = get_object_or_404(User, id=id)
    role = UserRoles.objects.filter(user=user).first()

    try:
        woreda = Woreda.objects.first()

        if request.method == "POST":
            form = RoleForm(request.POST, instance=role)
            if form.is_valid():
                role_instance = form.save(commit=False)
                role_instance.user = user  # Associate the user
                role_instance.woreda = woreda
                role_instance.role = 4 # set role to 4
                role_instance.save()
                messages.success(request, 'Operation successful')
                return redirect('ViewSubcityAdmins')
            else:
                for fields, errors in form.errors.items():
                    for error in errors:
                        messages.warning(request, f"{error}")
        else:
            form = RoleForm(instance=role)
    except:
        messages.error(request, 'No Defalut Woreda is assigned, Please Contact the System Admin')
        return redirect('ViewSubcityAdmins') 

    context = {'form': form}
    return render(request, 'City/Admins/AddSubcityAdminsRole.html', context)


@role_auth_decorator(role=5)
def AdminSubcityDetail(request, id):
    user = get_object_or_404(User, id=id)
    role = UserRoles.objects.filter(user=user).first()

    context = {
        'user':user,
        'role':role
    }

    return render(request, 'City/Admins/AdminSubcityDetail.html', context)

#  CIty Request Views
@role_auth_decorator(role=5)
def ViewApprovedRequest(request):
    approvedRequset = ApprovedRequestAdmin.objects.all()
    paginationObject = Paginator(approvedRequset, 10)
    page = request.GET.get('page')
    approvedRequestPaginator = paginationObject.get_page(page)

    context = {
        'ApprovedRequest':approvedRequestPaginator
    }
    return render(request, 'City/Request/ApprovedRequest.html',context)

@role_auth_decorator(role=5)
def ViewDeclinedRequest(request):
    declinedRequset = DecliendRequestAdmin.objects.all()
    paginationObject = Paginator(declinedRequset, 10)
    page = request.GET.get('page')
    declineRequestPaginator = paginationObject.get_page(page)

    context = {
        'DecliendRequest':declineRequestPaginator
    }

    return render(request, 'City/Request/DecliedRrequest.html', context)

@role_auth_decorator(role=5)
def AllRequest(request):
    allRequest = Request.objects.all()
    paginationObject = Paginator(allRequest, 10)
    page = request.GET.get('page')
    allRequestPaginator = paginationObject.get_page(page)

    context = {
        'AllRequest':allRequestPaginator
    }

    return render(request, 'City/Request/AllRequest.html', context)
# Parking Group View 

@role_auth_decorator(role=5)
def CityParkingGroupView(request):
    parkingGroup = ParkingGroup.objects.filter(is_active = True)
    
    paginatorObject = Paginator(parkingGroup, 10)
    page = request.GET.get('page')
    parkingGroupList = paginatorObject.get_page(page)
    parkingGroupWithParking = []

    for item in parkingGroupList:
        parkingGroupWithParking.append({'parkingGroup':item, 'parking':Parking.objects.filter(parking_group = item).count()})

    context = {
        'parkingGroupList': parkingGroupWithParking,
        'ParkingPaginator': parkingGroupList,
    }
    return render(request, 'City/ParkingGroup/CityParkingGroupView.html', context)

@role_auth_decorator(role=5)
def CityParkingGroupDetailView(request, id):
    try:
        parking_group = ParkingGroup.objects.get(id=id)
        parkings_data = [] #list to hold parking data

        for parking in Parking.objects.filter(parking_group=parking_group):
            successful_payments = Payment.objects.filter(status='successful', request_id__parking=parking)
            approved_requests = ApprovedRequest.objects.filter(payment_status=True, parking=parking)
            incidents = Incident.objects.filter(parking=parking)

            parking_data = {
                'parking': parking,
                'income': sum(payment.amount for payment in successful_payments),
                'user': successful_payments.count(),
                'requests': approved_requests.count(),
                'incident': incidents.count(),
            }
            parkings_data.append(parking_data)

        total_income = sum(item['income'] for item in parkings_data)
        total_users = sum(item['user'] for item in parkings_data)
        total_requests = sum(item['requests'] for item in parkings_data)
        total_incidents = sum(item['incident'] for item in parkings_data)

        context = {
            'parking_group': parking_group,
            'parkings_data': parkings_data,
            'income': total_income,
            'user': total_users,
            'requests': total_requests,
            'incident': total_incidents,
        }
        return render(request, 'City/ParkingGroup/CityParkingGroupDetailView.html', context)

    except ObjectDoesNotExist:
        messages.error(request, 'Oops, this parking group does not exist.')
        return redirect('CityParkingView')

#  Parking Detail 
@role_auth_decorator(role=5)
def CityParkingView(request):
    parkingAll = Parking.objects.filter(is_active = True)
    paginationObject = Paginator(parkingAll, 10)
    page = request.GET.get('page')
    parkings = paginationObject.get_page(page)

    context = {
        'parkings':parkings
    }
    return render(request, 'City/Parking/CityParkingView.html', context)

@role_auth_decorator(role=5)
def CityParkingViewDetail(request, id):
    parking = Parking.objects.get(id=id)
    parkingMembers = ParkingGroupMember.objects.filter(is_active = True, parking__id = id)
    parkingMemberAdmin = parkingMembers.filter(is_admin=True).first()
    if parkingMemberAdmin is not None:
        parkingMemberAdminProfile = Profile.objects.filter(user=parkingMemberAdmin.user).first()
    payments = Payment.objects.filter(status='successful', request_id__parking = parking)
    requests = ApprovedRequest.objects.filter(payment_status=True, parking = parking)
    incident = Incident.objects.filter(parking = parking)

    context = {
        'parkingMembers':parkingMembers,
        'parkingMemberAdmin':parkingMemberAdmin,
        # 'parkingMemberAdminProfile': parkingMemberAdminProfile,
        'income':sum(item.amount for item in payments),
        'user':sum(1 for item in payments),
        'requests':sum(1 for item in requests),
        'incident':sum(1 for item in incident),
        'parking':parking,
    }
    return render(request, 'City/Parking/CityParkingViewDetail.html', context)

# Incident City View

@role_auth_decorator(role=5)
def CityIncidentView(request):
    incident = Incident.objects.all()
    paginatorObject = Paginator(incident, 10)
    page = request.GET.get('page')
    incidentPaginator = paginatorObject.get_page(page)

    context = {
        'incidentList':incidentPaginator
    }
    return render(request, 'City/Incident/CityIncidentView.html', context)
# City Report View 
@role_auth_decorator(role=5)
def SubcityReportView(request):
    subcityAdmins = User.objects.filter(role = 4)
    subcityAdminPaginatorObject = Paginator(subcityAdmins, 10)
    page = request.GET.get('page')
    subcityAdminPaginator = subcityAdminPaginatorObject.get_page(page)
    admin_with_role = []

    for user in subcityAdminPaginator:
        role = UserRoles.objects.filter(user=user).first()
        admin_with_role.append({'role':role, 'user':user})

    context = {
        'admin_with_role': admin_with_role,
        'subcityAdmins':subcityAdminPaginator
    }
    return render(request, 'City/Report/SubcityReportView.html', context)

@role_auth_decorator(role=5)
def WoredaReportView(request, subcity):
    subcity = Subcity.objects.filter(subcity=subcity).first()
    woredaAdmins = UserRoles.objects.filter(subcity = subcity ,role = 3)
    WoredaAdminPaginatorObject = Paginator(woredaAdmins, 10)
    page = request.GET.get('page')
    woredaAdminPaginator = WoredaAdminPaginatorObject.get_page(page)

    context = {
        'woredaAdmins':woredaAdminPaginator,
        'subcity':subcity
    }
    return render(request, 'City/Report/WoredaReportView.html', context)

    # Detail Function For City Start Here

@role_auth_decorator(role=5)
def CityIncomeReportPerDay(request, subcity, woreda):
    # Filter payments based on status, subcity, and woreda
    payment = Payment.objects.filter(
        status='successful',
        request_id__parking__subcity=subcity,
        request_id__parking__woreda=woreda,
    )
    
    # Further filter payments for the current date
    queryset = payment.filter(date__date=datetime.now().date())
    
    # Ensure the queryset is ordered (e.g., by date or another field) before pagination
    queryset = queryset.order_by('-date')  # Order by date descending, modify as needed
    
    # Apply pagination
    PaginatorObject = Paginator(queryset, 10)
    page = request.GET.get('page')
    IncomeReport = PaginatorObject.get_page(page)
    
    # Prepare context
    context = {
        'IncomeReport': IncomeReport,
        'sum': sum(item.amount for item in IncomeReport),
        'woreda': woreda,
        'subcity': subcity,
    }
    
    # Render the template with the context
    return render(request, 'City/Report/CityIncomeReport/CityIncomeReportPerDay.html', context)

@role_auth_decorator(role=5)
def CityIncomeReportPerMonth(request, subcity, woreda, month):
    month_mapping = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }

    # Get the numeric month value
    month = month_mapping.get(month, None)
    

    # Filter the payments based on the month number and other conditions
    payment = Payment.objects.filter(
        status='successful',
        request_id__parking__subcity=subcity,
        request_id__parking__woreda=woreda
    )
    querysets = payment.filter(date__year=datetime.now().year, date__month=month)
    
    # Ensure the queryset is ordered (e.g., by date or another field) before pagination
    queryset = querysets.order_by('-date')  # Order by date descending, modify as needed
    
    # Apply pagination
    PaginatorObject = Paginator(queryset, 10)
    page = request.GET.get('page')
    IncomeReport = PaginatorObject.get_page(page)
    
    # Prepare context
    context = {
        'IncomeReport': IncomeReport,
        'sum': sum(item.amount for item in IncomeReport),
        'woreda': woreda,
        'subcity': subcity,
    }
    
    # Render the template with the context
    return render(request, 'City/Report/CityIncomeReport/CityIncomeReportPerMonth.html', context)

@role_auth_decorator(role=5)
def CityIncomeReportPerYear(request, subcity, woreda):
    # Filter payments based on status, subcity, and woreda
    payment = Payment.objects.filter(
        status='successful',
        request_id__parking__subcity=subcity,
        request_id__parking__woreda=woreda,
    )
    
    # Further filter payments for the current date
    queryset = payment.filter(date__year = datetime.now().year)
    
    # Ensure the queryset is ordered (e.g., by date or another field) before pagination
    queryset = queryset.order_by('-date')  # Order by date descending, modify as needed
    
    # Apply pagination
    PaginatorObject = Paginator(queryset, 10)
    page = request.GET.get('page')
    IncomeReport = PaginatorObject.get_page(page)
    
    # Prepare context
    context = {
        'IncomeReport': IncomeReport,
        'sum': sum(item.amount for item in IncomeReport),
        'woreda': woreda,
        'subcity': subcity,
    }
    
    # Render the template with the context
    return render(request, 'City/Report/CityIncomeReport/CityIncomeReportPerDay.html', context)

    # Removed Instance 

@role_auth_decorator(role=5)
def CityCustomerReportPerDay(request, subcity, woreda):
    # Filter payments based on status, subcity, and woreda
    payments = Payment.objects.filter(status='successful', request_id__parking__parking_group__subcity=subcity, request_id__parking__woreda = woreda, date__date=datetime.now().date())
    unique_emails = payments.filter(date__date=datetime.now().date()).values('user__email').distinct()
    queryset = []
    for email in unique_emails:
        payment = payments.filter(user__email=email['user__email']).first()
        car = Car.objects.filter(user=payment.user).first()
        queryset.append({'payment': payment, 'car': car})
    
    
    # Apply pagination
    PaginatorObject = Paginator(queryset, 10)
    page = request.GET.get('page')
    IncomeReport = PaginatorObject.get_page(page)
    
    # Prepare context
    context = {
        'IncomeReport': IncomeReport,
        'sum': sum(1 for item in IncomeReport),
        'woreda': woreda,
        'subcity': subcity,
    }
    
    # Render the template with the context
    return render(request, 'City/Report/CityCustomerReport/CityCustomerReportPerDay.html', context)

@role_auth_decorator(role=5)
def CityCustomerReportPerMonth(request, subcity, woreda, month):
    month_mapping = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }

    # Get the numeric month value
    month = month_mapping.get(month, None)

    payments = Payment.objects.filter(status='successful', request_id__parking__parking_group__subcity=subcity, request_id__parking__woreda = woreda)
    unique_emails = payments.filter(date__year = datetime.now().year, date__month=month).values('user__email').distinct()
    queryset = []
    for email in unique_emails:
        payment = payments.filter(user__email=email['user__email']).first()
        car = Car.objects.filter(user=payment.user).first()
        queryset.append({'payment': payment, 'car': car})
    
    # Apply pagination
    PaginatorObject = Paginator(queryset, 10)
    page = request.GET.get('page')
    IncomeReport = PaginatorObject.get_page(page)
    
    # Prepare context
    context = {
        'IncomeReport': IncomeReport,
        'sum': sum(1 for item in IncomeReport),
        'woreda': woreda,
        'subcity': subcity,
    }
    
    # Render the template with the context
    return render(request, 'City/Report/CityCustomerReport/CityCustomerReportPerMonth.html', context)

@role_auth_decorator(role=5)
def CityCustomerReportPerYear(request, subcity, woreda):
    # Filter payments based on status, subcity, and woreda
    payments = Payment.objects.filter(status='successful', request_id__parking__parking_group__subcity=subcity, request_id__parking__woreda = woreda)
    unique_emails = payments.filter(date__year = datetime.now().year).values('user__email').distinct()
    queryset = []
    for email in unique_emails:
        payment = payments.filter(user__email=email['user__email']).first()
        car = Car.objects.filter(user=payment.user).first()
        queryset.append({'payment': payment, 'car': car})
    
    # Apply pagination
    PaginatorObject = Paginator(queryset, 10)
    page = request.GET.get('page')
    IncomeReport = PaginatorObject.get_page(page)
    
    # Prepare context
    context = {
        'IncomeReport': IncomeReport,
        'sum': sum(1 for item in IncomeReport),
        'woreda': woreda,
        'subcity': subcity,
    }
    
    # Render the template with the context
    return render(request, 'City/Report/CityCustomerReport/CityCustomerReportPerYear.html', context)

    # Removed Instance 

@role_auth_decorator(role=5)
def CityProfile(request):
    return render(request, '')

@role_auth_decorator(role=5)
def CityProfile(request):
  userForm = UserForm(request.POST, instance=request.user)
  profilePicture = Profile.objects.filter(user=request.user).first()
  profileForm = ProfileForm(request.POST, request.FILES,  instance=profilePicture)
  if request.method == 'POST':
    if userForm.is_valid():
      userForm.save()
      messages.success(request, 'Profile Have Been Updated')
      return redirect('CityProfile')
    else:
      messages.error(request, 'The Form Is Not Valid')
      return redirect('CityProfile')
  else:
    userForm = UserForm(instance=request.user)
    profileForm = ProfileForm(instance=profilePicture)

  return render(request, 'City/Profile/CityProfile.html', {'userForm': userForm, 'profileForm':profileForm,})

@role_auth_decorator(role=5)
def CityProfileUpdate(request):
  profilePicture = Profile.objects.filter(user=request.user).first()
  form = ProfileForm(request.POST, request.FILES, instance=profilePicture)
  if request.method == "POST":
    if form.is_valid():
      form_instance = form.save(commit=False)
      form_instance.user = request.user
      form_instance.save()
      messages.success(request, 'Profile Picture Have Been Updated')
      return redirect('CityProfile')

@role_auth_decorator(role=5)
def RemoveSubcityAdmin(request, id):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()
    messages.success(request, 'User Deleted Succssfuly')
    return redirect('ViewSubcityAdmins')