from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from authentication.forms import UserForm, ProfileForm
from authentication.models import User, Profile, UserRoles, Woreda
from core.models import Request, ApprovedRequestAdmin, DecliendRequestAdmin, Payment, ApprovedRequest, DeletedInstance
# Woreda Import 
from parking.models import  Parking, ParkingLegalDoc

from woreda.forms import  ApprovedRequestAdminForm, DecliendRequestAdminForm
from datetime import datetime
from user.models import Car
from .forms import WoredaRegisterForm, WoredaAdminRoleForm
# Paginator and Pagination Applied Here
from django.core.paginator import Paginator
# Decorator
from authentication.RoleDecorator.decorators import role_auth_decorator

# Create your views here.
@role_auth_decorator(role=4)
def subcity_dashboard(request):

    try:
        # if request.user.check_password('123'):
        #     messages.warning(request, 'Please Update Your Password')
        #     return redirect('subcity_profile')
        role = UserRoles.objects.filter(user = request.user).first()
        parking = Parking.objects.filter(is_active = True, subcity = role.subcity)  
        approved_count = sum(1 for item in parking if item.is_approved)
            
        # Get all ParkingRequest related to the parking
        parking_requests = ApprovedRequest.objects.filter(parking__in=parking)
            
            # Extract unique emails
        unique_email = set(request.user.email for request in parking_requests)

        # Count the number of unique users
        unique_user_count = len(unique_email)
        woreda_admins = UserRoles.objects.filter(subcity=role.subcity, role=3)

    except:
        messages.error(request, 'Error Fetching User Data')
        return redirect('admin')

    context = {
          
            'parking_count': parking.count(),
            'approved_request': approved_count,
            'active_user': unique_user_count,
            'parking_request': parking_requests,
            'parking_request_count': parking_requests.count(),
            'parkings':parking,
            'woreda_admins':woreda_admins.count()

        }
    return render(request, 'Subcity/SubcityDashboard.html', context)

@role_auth_decorator(role=4)
def subcity_request(request):
    role = UserRoles.objects.filter(user = request.user).first()
    request_list = Request.objects.filter(parking__subcity = role.subcity)

    context = {
      'request_lists': request_list
    }
    return  render(request, 'Subcity/request/SubcityRequest.html', context)

@role_auth_decorator(role=4)
def subcity_request_detail(request, id):
  request_list = get_object_or_404(Request, id=id)
  request_list.is_read = True
  request_list.save()
  context = {
     'request_list': request_list
     }
  return render(request, 'Subcity/request/SubcityRequestDetail.html',context)

@role_auth_decorator(role=4)
def  ApproveRequestSubcity(request, id):
    CurrentRequest = Request.objects.get(id=id)
    parking = Parking.objects.get(id=CurrentRequest.parking.id)
    declined_request_instance = DecliendRequestAdmin.objects.filter(request_ref = CurrentRequest).first()
    if declined_request_instance:
        declined_request_instance.delete()
    request_instance = ApprovedRequestAdmin.objects.filter(request_ref = CurrentRequest).first()
    legal_document = ParkingLegalDoc.objects.filter(parking = parking)
    if request.method == 'POST':
        form = ApprovedRequestAdminForm(request.POST, instance=request_instance)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.request_ref = CurrentRequest
            form_instance.save()
            CurrentRequest.status = True
            CurrentRequest.save()
            parking.is_approved = True
            parking.save()
            messages.success(request, 'Approved Successfuly')
            return redirect('subcity_request')
    else: 
        form = ApprovedRequestAdminForm(instance = request_instance)
    context = {
        'CurrentRequest':CurrentRequest,
        'parking':parking,
        'form':form,
        'legalDocument':legal_document,
    }
    return render(request, 'Subcity/request/ApproveRequestSubcity.html', context)

@role_auth_decorator(role=4)
def DeclineRequestSubcity(request, id):
    CurrentRequest = Request.objects.get(id=id)
    parking = Parking.objects.get(id=CurrentRequest.parking.id)
    approved_request_instance = ApprovedRequestAdmin.objects.filter(request_ref = CurrentRequest).first()
    if approved_request_instance:
        approved_request_instance.delete()
    request_instance = DecliendRequestAdmin.objects.filter(request_ref = CurrentRequest).first()
    legal_document = ParkingLegalDoc.objects.filter(parking = parking)
    if request.method == 'POST':
        form = DecliendRequestAdminForm(request.POST, instance=request_instance)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.request_ref = CurrentRequest
            form_instance.save()
            CurrentRequest.status = False
            CurrentRequest.save()
            parking.is_approved = False
            parking.save()
            messages.success(request, 'Decliend Successfuly')
            return redirect('subcity_request')
    else: 
        form = DecliendRequestAdminForm(instance = request_instance)
    context = {
        'CurrentRequest':CurrentRequest,
        'parking':parking,
        'form':form,
        'legalDocument':legal_document,
    }
    return render(request, 'Subcity/request/DeclineRequestSubcity.html', context)

@role_auth_decorator(role=4)
def ViewWoredaAdmin(request):
    try:
        role = UserRoles.objects.filter(user = request.user).first()
        woredaAdmins = UserRoles.objects.filter(subcity=role.subcity, role=3)
    except:
        messages.error(request,'User Role Is Not Found')
        return redirect('/admin')
    context = {
        'woredaAdmins':woredaAdmins
    }
    return render(request, 'Subcity/RegisterWoreda/ViewWoredaAdmin.html', context)

@role_auth_decorator(role=4)
def RegisterWoreda(request, id):
    user = User.objects.filter(id=id).first()
    logged_user = UserRoles.objects.filter(user=request.user).first()
    role = UserRoles.objects.filter(user=user, woreda__isnull=False).first()
    if request.method == 'POST':
        form = WoredaRegisterForm(request.POST, instance=user)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.set_password('123')
            form_instance.role = 3
            form_instance.save()  # Save the user first

            userRole = UserRoles(
                user=form_instance,  # Now form_instance has an ID
                subcity=logged_user.subcity,
                role=3
            )
            userRole.save()

            messages.success(request, 'Woreda Admin Created Successfully')
            return redirect('ViewWoredaAdmin')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = WoredaRegisterForm(instance=user)
    context = {
        'form': form,
        'role': role
    }
    return render(request, 'Subcity/RegisterWoreda/RegisterWoreda.html', context)

@role_auth_decorator(role=4)
def AddWoredaAdminsRole(request, id):
    user = get_object_or_404(User, id=id)
    role = UserRoles.objects.filter(user=user).first()

    if request.method == "POST":
            form = WoredaAdminRoleForm(request.POST, instance=role)
            if form.is_valid():
                role_instance = form.save(commit=False)
                role_instance.subcity = role.subcity
                role_instance.user = user  
                role_instance.role = 3 
                role_instance.save()
                messages.success(request, 'Operation successful')
                return redirect('ViewWoredaAdmin')
            else:
                for fields, errors in form.errors.items():
                    for error in errors:
                        messages.warning(request, f"{error}")
    else:
        form = WoredaAdminRoleForm(instance=role)

    context = {
        'form':form
    }
    return render(request, 'Subcity/RegisterWoreda/AddWoredaAdminsRole.html', context)

@role_auth_decorator(role=4)
def AdminWoredaDetail(request, id):
    user = get_object_or_404(User, id=id)
    role = UserRoles.objects.filter(user=user).first()

    context = {
        'user':user,
        'role':role
    }

    return render(request, 'Subcity/RegisterWoreda/AdminWoredaDetail.html', context)


@role_auth_decorator(role=4)
def subcity_profile(request):
  userForm = UserForm(request.POST, instance=request.user)
  profilePicture = Profile.objects.filter(user=request.user).first()
  profileForm = ProfileForm(request.POST, request.FILES,  instance=profilePicture)
  if request.method == 'POST':
    if userForm.is_valid():
      userForm.save()
      messages.success(request, 'Profile Have Been Updated')
      return redirect('admin_profile')
    else:
      messages.error(request, 'The Form Is Not Valid')
      return redirect('admin_profile')
  else:
    userForm = UserForm(instance=request.user)
    profileForm = ProfileForm(instance=profilePicture)

  return render(request, 'Subcity/profile/SubcityProfile.html', {'userForm': userForm, 'profileForm':profileForm,})

@role_auth_decorator(role=4)
def subcity_profile_update(request):
  profilePicture = Profile.objects.filter(user=request.user).first()
  form = ProfileForm(request.POST, request.FILES, instance=profilePicture)
  if request.method == "POST":
    if form.is_valid():
      form_instance = form.save(commit=False)
      form_instance.user = request.user
      form_instance.save()
      messages.success(request, 'Profile Picture Have Been Updated')
      return redirect('subcity_profile')



#  Report Update On The Data ==================================================================
@role_auth_decorator(role=4)
def SubcityReport(request):
    user = UserRoles.objects.filter(user=request.user).first()
    woredas = UserRoles.objects.filter(subcity = user.subcity, role = 3)
    context = {
        'woredas':woredas
    }
    return render(request, 'Subcity/Report/SubcityReport.html', context)

@role_auth_decorator(role=4)
def SubcityWoredaDetailReport(request, id):
    user = UserRoles.objects.filter(user=request.user).first()
    payment = Payment.objects.filter(status='successful', 
    request_id__parking__subcity=user.subcity, request_id__parking__woreda = id)
    queryset = payment.filter(date__date=datetime.now().date())
    context =   {
        'payments':queryset,
        'sum':sum(item.amount for item in queryset),
        'woreda_id':id,

    }
    return render(request, 'Subcity/Report/SubcityWoredaDetailReport.html', context)

@role_auth_decorator(role=4)
def SubcityIncomeReportPerMonth(request, id, month_name):
    # Mapping of month names to numbers
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
    month = month_mapping.get(month_name, None)
    

    # Filter the payments based on the month number and other conditions
    user = UserRoles.objects.filter(user=request.user).first()
    payment = Payment.objects.filter(
        status='successful',
        request_id__parking__subcity=user.subcity,
        request_id__parking__woreda=id
    )
    queryset = payment.filter(date__year=datetime.now().year, date__month=month)

    # Prepare the context
    context = {
        'payments': queryset,
        'sum': sum(item.amount for item in queryset),
        'woreda_id': id,
    }

    # Return the rendered response
    return render(request, 'Subcity/Report/SubcityIncomeReportPerMonth.html', context)

@role_auth_decorator(role=4)
def SubcityIncomReportPerYear(request, id):
    user = UserRoles.objects.filter(user=request.user).first()
    payment = Payment.objects.filter(status='successful', request_id__parking__subcity=user.subcity, request_id__parking__woreda = id)
    queryset = payment.filter(date__year = datetime.now().year)
    context = {
        'payments':queryset,
        'sum':sum(item.amount for item in queryset),
        'woreda_id': id,
    }
    return render(request, 'Subcity/Report/SubcityIncomReportPerYear.html', context)

@role_auth_decorator(role=4)
def SubcityCustomerReportPerDay(request, id):
    user = UserRoles.objects.filter(user=request.user).first()
    payments = Payment.objects.filter(status='successful', request_id__parking__parking_group__subcity=user.subcity, request_id__parking__woreda = id, date__date=datetime.now().date())
    unique_emails = payments.filter(date__date=datetime.now().date()).values('user__email').distinct()
    queryset = []
    for email in unique_emails:
        payment = payments.filter(user__email=email['user__email']).first()
        car = Car.objects.filter(user=payment.user).first()
        queryset.append({'payment': payment, 'car': car})

    context = {
        'users': queryset,
        'woreda_id':id
    }
    return render(request, 'Subcity/Report/SubcityCustomerReportPerDay.html', context)

@role_auth_decorator(role=4)
def SubcityCustomerReportPerMonth(request, id, month_name):
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
    month = month_mapping.get(month_name, None)
    user = UserRoles.objects.filter(user=request.user).first()

    payments = Payment.objects.filter(status='successful', request_id__parking__parking_group__subcity=user.subcity, date__date=datetime.now().date())
    unique_emails = payments.filter(date__year = datetime.now().year, date__month=month).values('user__email').distinct()
    queryset = []
    for email in unique_emails:
        payment = payments.filter(user__email=email['user__email']).first()
        car = Car.objects.filter(user=payment.user).first()
        queryset.append({'payment': payment, 'car': car})

    context = {
        'users': queryset,
        'woreda_id':id
    }
    return render(request, 'Subcity/Report/SubcityCustomerReportPerMonth.html', context)

@role_auth_decorator(role=4)
def SubcityCustomerReportPerYear(request, id):
    user = UserRoles.objects.filter(user=request.user).first()
    payments = Payment.objects.filter(status='successful', request_id__parking__parking_group__subcity=user.subcity, request_id__parking__woreda = id,date__date=datetime.now().date())
    unique_emails = payments.filter(date__year = datetime.now().year).values('user__email').distinct()
    queryset = []
    for email in unique_emails:
        payment = payments.filter(user__email=email['user__email']).first()
        car = Car.objects.filter(user=payment.user).first()
        queryset.append({'payment': payment, 'car': car})

    context = {
        'users': queryset,
        'woreda_id':id
    }
    return render(request, 'Subcity/Report/SubcityCustomerReportPerYear.html', context)

