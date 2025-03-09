from django.contrib import messages
from django.shortcuts import render, redirect
from authentication.forms import UserForm, ProfileForm
from authentication.models import User, Profile, UserRoles
from core.models import Request, DeletedInstance, Payment, Incident

# Woreda Import 
from parking.forms import ParkingGroupForm, ParkingGroupMemberForm, ParkingForm
from parking.models import ParkingGroup, ParkingGroupMember, Parking, WorkingHours
from authentication.forms import UserForm
from authentication.models import User
from user.forms import UserLegalDocumentForm
from django.contrib.gis.geos import Point
from woreda.forms import DeletedInstanceForm
from datetime import datetime
from user.models import Car
from authentication.forms import UserForm, ProfileForm
from authentication.models import Profile
# Paginator and Pagination Applied Here
from django.core.paginator import Paginator

from authentication.RoleDecorator.decorators import role_auth_decorator


@role_auth_decorator(role=3)
def woreda_dashboard(request):
    user = UserRoles.objects.filter(user=request.user).first()
    parkings_list = []
    parking_groups = ParkingGroup.objects.filter(is_active = True)
    for parking in parking_groups:
        parkings = Parking.objects.filter(is_active = True, parking_group = parking)
        parkings_list.append({'parking':parkings, 'parking_group':parking})

    print(parkings_list)
    context = {
        'data':parkings_list,
    }
    return render(request,'Woreda/WoredaDashboard.html', context)

@role_auth_decorator(role=3)
def woreda_parking_register(request):
    parking_group = ParkingGroup.objects.filter(is_active = True)
    context = {
        'parking_group': parking_group,
    }
    return render(request, 'Woreda/ParkingRegister/RegisterParkingGroup.html', context)

@role_auth_decorator(role=3)
def RegisterParkingGroupDetail(request, id):
    parking_group = ParkingGroup.objects.filter(id=id, is_active = True).first()
    parking = Parking.objects.filter(parking_group = parking_group, is_active = True)
    if request.method == "POST":
        form = ParkingGroupForm(request.POST, instance = parking_group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Parking Group Is Added Successfulyl')
            return redirect('woreda_parking_register')
        else:
            messages.error(request, 'Form Is not valid')
            return redirect('woreda_parking_register')
    else:
        form = ParkingGroupForm(instance=parking_group)
    context = {
        'form': form, 
        'parking_group':parking_group, 
        'parkings':parking
               }
    return render(request, 'Woreda/ParkingRegister/RegisterParkingGroupDetail.html', context)

@role_auth_decorator(role=3)
def ViewParkingMember(request, id):
    parking = Parking.objects.get(id=id)
    parking_members = ParkingGroupMember.objects.filter(parking = parking, is_active = True)
    context = {
        'parking_members':parking_members,
        'parking':parking,
    }
    return render(request, 'Woreda/ParkingRegister/ViewParkingMember.html', context)

@role_auth_decorator(role=3)
def RegisterParkingGroupMember(request, id, id2):
    parking = Parking.objects.filter(id = id, is_active = True).first()
    user = User.objects.filter(id=id2, is_active = True).first()
    if request.method == "POST":
        formUser = UserForm(request.POST, instance=user)
        formGroupMember = ParkingGroupMemberForm(request.POST,request.FILES,)
        formUserLegalDocument = UserLegalDocumentForm(request.POST, request.FILES, instance=user)

        if formUser.is_valid():
            if formGroupMember.is_valid():
                if formUserLegalDocument.is_valid():
                    user_instance = formUser.save(commit=False)
                    user_instance.role = User.PARKING_ROLE
                    user_instance.set_password("123")
                    user_instance.save()
                    group_member_instance = formGroupMember.save(commit=False)
                    group_member_instance.parking = parking
                    group_member_instance.user = user_instance
                    group_member_instance.save()
                    formUserLegalDocument_instance = formUserLegalDocument.save(commit=False)
                    formUserLegalDocument_instance.user = user_instance
                    formUserLegalDocument_instance.save()

                    messages.success(request, 'Member Added Successfully')
                    return redirect('ViewParkingMember', id=parking.id)
                else:
                    user_legal_document_errors = formUserLegalDocument.errors
                    messages.error(request, f'User Legal Document Form Errors: {user_legal_document_errors}')
            else:
                group_member_errors = formGroupMember.errors
                messages.error(request, f'Group Member Form Errors: {group_member_errors}')
        else:
            user_errors = formUser.errors
            messages.error(request, f'User Form Errors: {user_errors}')
    else:
        formUser = UserForm(instance=user)
        formGroupMember = ParkingGroupMemberForm()
        formUserLegalDocument = UserLegalDocumentForm(instance=user)
    context = {
        'formUser': formUser,
        'formGroupMember': formGroupMember,
        'userLegalDocument': formUserLegalDocument,
        'user':user,
        'parking':parking
    }
    return render(request, 'Woreda/ParkingRegister/RegisterParkingGroupMember.html', context)

from django.contrib.gis.geos import Point

@role_auth_decorator(role=3)
def RegisterParking(request, id, status):
    if status == 'new':
        parking_group = ParkingGroup.objects.filter(id=id, is_active = True).first()
        parking = None
    else:
        parking = Parking.objects.filter(id=id, is_active = True).first()
        parking_group = parking.parking_group

    if request.method == "POST":
        try:
            latitude = request.POST['latitude']
            longitude = request.POST['longitude']
            location = Point(float(longitude), float(latitude), srid=4326)
        except KeyError as e:
            messages.error(request, f"Error: {e}")
            return redirect('RegisterParking', id=id)  # Redirect back to the form page with an error message

        form = ParkingForm(request.POST, request.FILES, instance=parking)
        
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.location = location
            form_instance.parking_group = parking_group
            form_instance.is_active = True
            form_instance.save()
            messages.success(request, 'Parking has been created successfully')
            return redirect('RegisterParkingGroupDetail', parking_group.id)
        else:
            form_errors = form.errors
            messages.error(request, f'Parking Form Errors: {form_errors}')
    else:
        form = ParkingForm(instance=parking)
    context  = {
        'parking_group':parking_group,
        'ParkingForm':form,
        'parking':parking,
    }
    return render(request, 'Woreda/ParkingRegister/RegisterParking.html', context)

@role_auth_decorator(role=3)
def InstanceDelete(request, id, id_2,id_3):
    # id = 1, id_2 = 0 , id_3 = 0
    if request.method == "POST":
        form = DeletedInstanceForm(request.POST)
        parking_groups = ParkingGroup.objects.filter(id=id, is_active = True).first()
        parking = Parking.objects.filter(id=id_2, is_active = True).first()
        user = User.objects.filter(id=id_3, is_active = True).first()
        parking_member = ParkingGroupMember.objects.filter(parking = parking, user = user).first()

        if id != 0 and id_2 == 0 and id_3 == 0:
            if form.is_valid():
                form_instance = form.save(commit=False)
                form_instance.parking_group = parking_groups
                form_instance.woreda_admin = request.user
                form_instance.save()
                parking_groups.is_active = False
                parking_groups.save()

                # parkings = Parking.objects.filter(parking_group = parking_groups)
                # for item in parkings:
                #     item.is_active = False
                #     item.save()
                messages.success(request, 'Parking Group Deleted Successfuly')
                return redirect('woreda_parking_register')
            else:
                messages.error(request, 'Form Error Detected')
                return redirect('woreda_parking_register')
            
        elif id != 0 and id_2 != 0 and id_3 == 0:
            if form.is_valid():
                form_instance = form.save(commit=False)
                form_instance.parking_group = parking_groups
                form_instance.woreda_admin = request.user
                form_instance.parking = parking
                form_instance.save()
                parking.is_active = False
                parking.save()
                messages.success(request, 'Parking Deleted Successfuly')
                return redirect('RegisterParkingGroupDetail', id=parking_groups.id)
            else:
                messages.error(request, 'Form Error Detected')
                return redirect('RegisterParkingGroupDetail', id=parking_groups.id)
        elif id != 0 and id_2!= 0 and id_3 != 0:
            if form.is_valid():
                form_instance = form.save(commit=False)
                form_instance.parking_groups = parking_groups
                form_instance.woreda_admin = request.user
                form_instance.parking = parking
                form_instance.user = user
                form_instance.save()
                user.is_active = False
                user.save()
                parking_member.is_active = False
                parking_member.save()
                messages.success(request, 'Parking Member Deleted Successfuly')
                return redirect('RegisterParkingGroupDetail', id=parking_groups.id)
            else:
                messages.error(request, 'Form Error Detected')
                return redirect('RegisterParkingGroupDetail', id=parking_groups.id)
    else:
        form = DeletedInstanceForm()
    return render(request, 'Woreda/ParkingRegister/DeleteInstance.html', {'form':form})

@role_auth_decorator(role=3)
def requestList(request):
    parking_group = ParkingGroup.objects.filter(is_active = True)
    context = {
        'parking_group': parking_group
    }
    return render(request, 'Woreda/ParkingRequest/ViewParkingRequest.html', context)

@role_auth_decorator(role=3)
def requestListDetail(request, id):
    parking_group = ParkingGroup.objects.filter(id=id, is_active = True).first()
    parkings = Parking.objects.filter(parking_group = parking_group, is_active = True)
    print(parkings)
    parking_with_working_hour =[]
    for parking in parkings:
        working_hour = WorkingHours.objects.filter(parking = parking)
        requestWoreda = Request.objects.filter(parking=parking, parking_group=parking_group)
        print(request)
        parking_with_working_hour.append({'parking':parking, 'working_hours':working_hour, 'requests':requestWoreda})
    context = {
        'parking_with_working_hours':parking_with_working_hour,
        'parking_group':parking_group,
    }
    return render(request, 'Woreda/ParkingRequest/ParkingRequestDetail.html', context)

@role_auth_decorator(role=3)
def sendRequestWoreda(request, id, id_2):
    parking_group = ParkingGroup.objects.filter(is_active = True, id=id).first()
    parking = Parking.objects.filter(is_active = True, id=id_2).first()

    ParkingRequest = Request(
        parking_group = parking_group,
        parking = parking,
        woreda = request.user,
        subcity = "Kirkos",
    )
    ParkingRequest.save()
    parking.is_sent = True
    parking.save()
    messages.success(request, 'Request Sent Successfuly')
    return redirect('requestListDetail', id=parking_group.id)

@role_auth_decorator(role=3)        
def ViewDeletedInstance(request):
    deleted_instance = DeletedInstance.objects.filter(woreda_admin = request.user, Instance_type = "Parking-Group")
    context = {
        'deleted_instances':deleted_instance,
    }
    return render(request, 'Woreda/RemovedInstance/RemovedInstance.html', context)


@role_auth_decorator(role=3)
def ViewDeletedInstanceParking(request):
    deleted_instance = DeletedInstance.objects.filter(woreda_admin = request.user, Instance_type = "Parking")
    print(deleted_instance)
    context = {
        'deleted_instances':deleted_instance,
    }
    return render(request, 'Woreda/RemovedInstance/RemovedParkingInstance.html', context)

@role_auth_decorator(role=3)
def ViewDeletedInstanceParkingMember(request):
    deleted_instance = DeletedInstance.objects.filter(woreda_admin = request.user, Instance_type = "Parking-Group-Member")
    context = {
        'deleted_instances':deleted_instance,
    }
    return render(request, 'Woreda/RemovedInstance/RemovedMemeberInstance.html', context)



@role_auth_decorator(role=3)
def IncomeReportWoredaPerDay(request):
    user = UserRoles.objects.filter(user=request.user).first()
    payment = Payment.objects.filter(status='successful', request_id__parking__parking_group__subcity=user.subcity)
    queryset = payment.filter(date__date=datetime.now().date())
    context =   {
        'payments':queryset,
        'sum':sum(item.amount for item in queryset)
    }
    return render(request, 'Woreda/Report/IncomeReportWoredaPerDay.html', context)

@role_auth_decorator(role=3)
def IncomeReportWoredaPerMonth(request, id):
    user = UserRoles.objects.filter(user=request.user).first()
    payment = Payment.objects.filter(status='successful', request_id__parking__parking_group__subcity=user.subcity)
    queryset = payment.filter(date__year = datetime.now().year, date__month=id)
    context = {
        'payments':queryset,
        'sum':sum(item.amount for item in queryset)
    }
    return render(request, 'Woreda/Report/IncomeReportWoredaPerMonth.html', context)

@role_auth_decorator(role=3)
def IncomeReportWoredaPerYear(request):
    user = UserRoles.objects.filter(user=request.user).first()
    payment = Payment.objects.filter(status='successful', request_id__parking__parking_group__subcity=user.subcity)
    queryset = payment.filter(date__year = datetime.now().year)
    context = {
        'payments':queryset,
        'sum':sum(item.amount for item in queryset)
    }
    return render(request, 'Woreda/Report/IncomeReportWoredaPerYear.html', context)

@role_auth_decorator(role=3)
def CustomerReportWoredaPerDay(request):
    user = UserRoles.objects.filter(user=request.user).first()
    payments = Payment.objects.filter(status='successful', request_id__parking__parking_group__subcity=user.subcity, date__date=datetime.now().date())
    unique_emails = payments.filter(date__date=datetime.now().date()).values('user__email').distinct()
    queryset = []
    for email in unique_emails:
        payment = payments.filter(user__email=email['user__email']).first()
        car = Car.objects.filter(user=payment.user).first()
        queryset.append({'payment': payment, 'car': car})

    context = {
        'users': queryset,
    }
    return render(request, 'Woreda/Report/CustomerReportWoredaPerDay.html', context)

@role_auth_decorator(role=3)
def CustomerReportWoredaPerMonth(request, id):
    user = UserRoles.objects.filter(user=request.user).first()
    payments = Payment.objects.filter(status='successful', request_id__parking__parking_group__subcity=user.subcity, date__date=datetime.now().date())
    unique_emails = payments.filter(date__year = datetime.now().year, date__month=id).values('user__email').distinct()
    queryset = []
    for email in unique_emails:
        payment = payments.filter(user__email=email['user__email']).first()
        car = Car.objects.filter(user=payment.user).first()
        queryset.append({'payment': payment, 'car': car})

    context = {
        'users': queryset,
    }
    return render(request, 'Woreda/Report/CustomerReportWoredaPerMonth.html', context)

@role_auth_decorator(role=3)
def CustomerReportWoredaPerYear(request):
    user = UserRoles.objects.filter(user=request.user).first()
    payments = Payment.objects.filter(status='successful', request_id__parking__parking_group__subcity=user.subcity, date__date=datetime.now().date())
    unique_emails = payments.filter(date__year = datetime.now().year).values('user__email').distinct()
    queryset = []
    for email in unique_emails:
        payment = payments.filter(user__email=email['user__email']).first()
        car = Car.objects.filter(user=payment.user).first()
        queryset.append({'payment': payment, 'car': car})

    context = {
        'users': queryset,
    }
    return render(request, 'Woreda/Report/CustomerReportWoredaPerYear.html', context)

@role_auth_decorator(role=3)
def IncidentReportWoredaPerDay(request):
    return render(request, 'Woreda/Report/IncidentReportWoredaPerDay.html')

@role_auth_decorator(role=3)
def IncidentReportWoredaPerMonth(request):
    return render(request, 'Woreda/Report/IncidentReportWoredaPerMonth.html')

@role_auth_decorator(role=3)
def IncidentReportWoredaPerYear(request):
    return render(request, 'Woreda/Report/IncidentReportWoredaPerYear.html')


@role_auth_decorator(role=3)
def ParkingReportWoredaPerDay(request):
    user = UserRoles.objects.filter(user=request.user).first()
    parking = Parking.objects.filter(is_active = True, subcity = user.subcity, woreda = user.woreda.name)
    context = {
        'parkings':parking,
        'count': sum(1 for item in parking)
    }
    return render(request, 'Woreda/Report/ParkingReportWoredaPerDay.html', context)


@role_auth_decorator(role=3)
def WoredaProfile(request):
   user = User.objects.filter(id = request.user.id).first()
   userRole = UserRoles.objects.filter(user=request.user).first()
   subcity = userRole.subcity
   woreda = userRole.woreda
   picture_instance = Profile.objects.filter(user = user).first()
   if request.method == 'POST':
       form = UserForm(request.POST, instance = user)
       profile_form = ProfileForm(request.POST, request.FILES, instance = picture_instance,)
       if form.is_valid():
           form_instance = form.save(commit=False)
           form_instance.subcity = subcity
           form_instance.woreda  = woreda
           form_instance.save()
           messages.success(request, 'Profile Updated Successfuly')
           return redirect('WoredaProfile')
       else:
           messages.error(request, 'Error Filling The Form')
           return redirect('WoredaProfile')
   else:
       form = UserForm(instance = user)
       profile_form = ProfileForm(instance = picture_instance)
   context = {
        'form':form,
        'profile_form': profile_form
    }
   return render(request, 'Woreda/Profile.html', context)

@role_auth_decorator(role=3)
def WoredaNotificationIncident(request):
    user = UserRoles.objects.filter(user=request.user).first()
    parkings = Parking.objects.filter(is_active = True, subcity = user.subcity, woreda = user.woreda.name)
    incidents = Incident.objects.filter(parking__in=parkings)

    context = {
        'incidents':incidents
    }
    return render(request, 'Woreda/Notification/WoredaNotificationIncident.html', context)


@role_auth_decorator(role=3)
def WoredaNotificationIncidentDetail(request, id):
    incidnet = Incident.objects.get(id = id)
    context = {
        'incidents':incidnet,
    }
    return render(request, 'Woreda/Notification/WoredaIncidentDetail.html', context)

@role_auth_decorator(role=3)
def WoredaNotificationChangePrice(request):
    return render(request, 'Woreda/Notification/WoredaNotificationChangePrice.html')

@role_auth_decorator(role=3)
def WoredaNotificationRequest(request):
    return render(request, 'Woreda/Notification/WoredaNotificationRequest.html')
