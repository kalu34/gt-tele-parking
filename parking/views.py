from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import Parking, WorkingHours, ParkingGroupMember
from geopy.distance import geodesic
import json
from json import JSONDecodeError
from .forms import  ParkingForm
from authentication.forms import UserForm, ProfileForm
from authentication.models import Profile, PlateNumber
from core.models import ApprovedRequest, ReservedRequest, Payment, Incident
from django.contrib.auth.hashers import check_password
from user.models import Car
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from collections import defaultdict
import datetime
from core.models import Request, ApprovedRequestAdmin,DecliendRequestAdmin
from datetime import datetime as dt
from django.shortcuts import get_object_or_404, render
from decimal import Decimal
from core.forms import IncidentForm
#  Pagination

from django.core.paginator import Paginator

from authentication.RoleDecorator.decorators import role_auth_decorator


@role_auth_decorator(role=2)
def parking_home(request):
    parking_member = ParkingGroupMember.objects.filter(user = request.user, is_admin = True).first()
    parking = Parking.objects.filter(id = parking_member.parking.id).first()
    customer = ApprovedRequest.objects.filter(parking=parking)
    customer_count = customer.values('user__email').distinct().count()

    if parking is None:
        messages.warning(request, 'Parking Not Found, Please Contact Superviser')
        return redirect('admin')
    
    if not parking.is_active:
        messages.warning(request, 'Parking Is Not Active, Please Contact Superviser')
        return redirect('admin')
    
    if parking.is_approved:
        pass
    else:
        messages.warning(request, 'Wait Until Your Request Been Approved')
        return redirect('admin')


    sale = Decimal('0.00')  

    for item in customer:
        if item.total_price is not None:  
            sale += item.total_price  

    sale = round(sale / 1000) 
   
    context = {
        'parking': parking,
        'customer': customer_count,
        'sale': sale
    }
    return render(request, 'ParkingHome.html', context)

@role_auth_decorator(role=2)
def parking_request(request):
    parking_admin = ParkingGroupMember.objects.filter(user = request.user).first()
    parking = Parking.objects.get(id = parking_admin.parking.id)
    new_request = ReservedRequest.objects.filter(parking=parking, status = False)
    approved_request = ApprovedRequest.objects.filter(parking=parking)
    request_stop = ApprovedRequest.objects.filter(parking=parking, is_active=True, stop=True).first()

    #  Let Create An object first
    NewRequestPaginatorObject = Paginator(new_request, 10)
    ApprovedRequestPaginatorObject = Paginator(approved_request, 10)
    page = request.GET.get('page')

    NewRequestPaginator = NewRequestPaginatorObject.get_page(page)
    ApprovedRequestPaginator = ApprovedRequestPaginatorObject.get_page(page)

    context ={
        'request_stop':request_stop,
        'NewRequestPaginator': NewRequestPaginator,
        'ApprovedRequestPaginator': ApprovedRequestPaginator,
    }
    
    return render(request, 'ParkingRequest.html', context)

@role_auth_decorator(role=2)
def parking_request_approved(request):
    parking_admin = ParkingGroupMember.objects.filter(user = request.user).first()
    parking = Parking.objects.get(id = parking_admin.parking.id)
    approved_request = ApprovedRequest.objects.filter(parking=parking)
    request_stop = ApprovedRequest.objects.filter(parking=parking, is_active=True, stop=True).first()

    #  Let Create An object first
    ApprovedRequestPaginatorObject = Paginator(approved_request, 10)
    page = request.GET.get('page')

    ApprovedRequestPaginator = ApprovedRequestPaginatorObject.get_page(page)
    print(ApprovedRequestPaginator)
    context ={
        'request_stop':request_stop,
        'ApprovedRequestPaginator': ApprovedRequestPaginator,
    }
    return render(request, 'ParkingApprovedRequest.html', context)

@role_auth_decorator(role=2)
def parking_new_request_detail(request, id):
    parking_request_new = ReservedRequest.objects.filter(id=id).first()
    parking_admin = ParkingGroupMember.objects.filter(user = request.user).first()
    parking = Parking.objects.get(id = parking_admin.parking.id)
    parking_approved_request = ApprovedRequest.objects.filter(parking=parking)
    car = Car.objects.filter(user=parking_request_new.user).first()
    spot_list = range(1, parking.slot_capacity+1)
    context = {
        'parking_request_new': parking_request_new,
        'parking_approved_request': parking_approved_request,
        'car':car,
        'spot_list':spot_list,
    }

    return render(request, 'ParkingRequestDetail.html', context)


@role_auth_decorator(role=2)
def parking_new_approve_request(request, id):
    try:
        data = json.loads(request.body)
    except JSONDecodeError as e:
        return redirect('parking_request')

    value = data.get('key')
    if value is not None:
        parking_request_new = ReservedRequest.objects.filter(id=id).first()
        approved_parking_request = ApprovedRequest(
            user=parking_request_new.user,
            parking=parking_request_new.parking,
            slot=data['key'],
            payment_per_hour=parking_request_new.parking.price_per_hour,
            reference_trx=parking_request_new.requset_rfe
        )
        approved_parking_request.save()
        parking_request_new.delete()
        messages.success(request, 'Parking Request has been successfully created')
        return redirect('parking_request')
    else:
        messages.error(request, 'Please Insert A slot')
        return redirect('parking_new_request_detail', id)

    

@role_auth_decorator(role=2)
def parking_approved_request_detail(request, id):
    approved_request = ApprovedRequest.objects.filter(id=id).first()
    car = PlateNumber.objects.filter(user=approved_request.user).first()
    parking_admin = ParkingGroupMember.objects.filter(user = request.user).first()
    parking = Parking.objects.get(id = parking_admin.parking.id)
    approved_parking_requsts = ApprovedRequest.objects.filter(parking=parking)
    spot_list = range(1, parking.slot_capacity+1)

    context = {
        'approved_request': approved_request,
        'approved_parking_requsts': approved_parking_requsts,
        'car': car,
        'parking': parking,
        'spot_list': spot_list,
        'incident':Incident.objects.filter(request = approved_request).first()
    }
    return render(request,'ParkingApprovedReqeuestDetail.html', context)

@role_auth_decorator(role=2)
def incident_report(request, id, id2):
    parking = Parking.objects.get(id = id)
    request_new = ApprovedRequest.objects.get(id = id2)
    if request.method == 'POST':
        form = IncidentForm(request.POST, request.FILES)
        if form.is_valid():
            form_instance = form.save(commit = False)
            form_instance.parking = parking
            form_instance.request = request_new
            form_instance.save()
            messages.success(request, 'Incident Sent Successfuly')
            return redirect('parking_approved_request_detail', id=parking.id)
    else:
        form = IncidentForm()
    context = {
        'form':form
    }
    return render(request, 'IncidentReport.html', context)

@role_auth_decorator(role=2)
def view_incident(request):
    parking_admin = ParkingGroupMember.objects.filter(user = request.user).first()
    parking = Parking.objects.get(id = parking_admin.parking.id)
    incident = Incident.objects.filter(parking = parking)

    context = {
        'incidents':incident
    }
    return render(request, 'ViewIncident.html')

@role_auth_decorator(role=2)
def parking_approve_request_stop(request, id):
    parking_request = ApprovedRequest.objects.get(id=id)
    start_time = parking_request.start_time
    current_time = dt.now()
    parking_request.end_time = dt.now().strftime("%H:%M")
    
    if not isinstance(start_time, dt):
        start_time = dt.combine(parking_request.date, start_time)
    
    duration_seconds = (current_time - start_time).total_seconds()
    duration_hours = duration_seconds / 3600
    price_per_hour = parking_request.payment_per_hour
    total_cost = float(duration_hours) * float(price_per_hour)
    parking_request.total_price = total_cost
    parking_request.stop = False
    parking_request.is_active = False  # Set stop to True
    parking_request.save()

    parking = parking_request.parking
    parking.available_slots += 1
    parking.save()
        
    messages.success(request, 'Request Time Ended Successfully')    
    return redirect('parking_request')

@role_auth_decorator(role=2)
def parking_history(request):
    paring_admin = ParkingGroupMember.objects.filter(user = request.user, is_admin=True).first()
    parking = Parking.objects.get(id = paring_admin.parking.id)
    history = ApprovedRequest.objects.filter(parking=parking)

    # Prepare the context with history and related car model information
    context = {
        'historys': [
            {
                'request': req,
                'car_model': get_object_or_404(PlateNumber, user=req.user)
            }
            for req in history
        ],
    }
    
    return render(request, 'ParkingHistory.html', context)

@role_auth_decorator(role=2)
def parking_payment(request):
    parking_admin = ParkingGroupMember.objects.filter(user = request.user).first()
    parking = Parking.objects.get(id = parking_admin.parking.id)
    requestList = ApprovedRequest.objects.filter(parking=parking)

    payments = []
    for req in requestList:
        payment_data = Payment.objects.filter(request_id=req).first()  # Use filter().first() to avoid 404
        if payment_data:  # Check if payment_data is found
            payments.append({'payment_data': payment_data})

    # Check if payments list is empty
    if not payments:
        no_payments_message = "No payment records found. Please make a payment to see your payment history."
    else:
        no_payments_message = None  # No message if payments exist

    context = {
        'payments': payments,
        'no_payments_message': no_payments_message,
    }
    return render(request, 'ParkingPayment.html', context)


@role_auth_decorator(role=2)
def parking_report(request):
    now = timezone.now()
    today = now.date()

    # Daily report
    parking_requests_day = ApprovedRequest.objects.filter(date=today)

    # Define time interval (e.g., every hour)
    time_interval = datetime.timedelta(hours=1)
    start_time = timezone.make_aware(datetime.datetime.combine(today, datetime.time.min))

    # Create a dictionary to hold the total value and unique customer count for each interval
    daily_report = defaultdict(lambda: {'total_value': 0, 'total_customers': set()})

    # Iterate over the requests and populate the report
    for requests in parking_requests_day:
        if requests.start_time:  # Ensure start_time is not None
            request_datetime = datetime.datetime.combine(requests.date, requests.start_time)
            request_datetime = timezone.make_aware(request_datetime)  # Make it timezone aware

            # Find the interval start time
            interval_start = start_time + (request_datetime - start_time) // time_interval * time_interval
            daily_report[interval_start]['total_value'] += requests.total_price if requests.total_price is not None else 0
            daily_report[interval_start]['total_customers'].add(requests.user.email)

    # Prepare final report for daily chart
    formatted_daily_report = {
        'labels': [],
        'data': []
    }

    # Fill the formatted daily report
    for time in sorted(daily_report.keys()):
        formatted_daily_report['labels'].append(time.strftime("%H:%M"))  # Format the time for labels
        formatted_daily_report['data'].append({
            'total_value': daily_report[time]['total_value'],
            'total_customers': len(daily_report[time]['total_customers']),
        })

    # Weekly report
    start_date = now - timedelta(weeks=1)
    labels_week = []
    data_week = []

    for i in range(7):
        date = (start_date + timedelta(days=i)).date()
        parking_requests_week = ApprovedRequest.objects.filter(date=date)
        total_value_week = sum(request.total_price for request in parking_requests_week if request.total_price is not None)
        unique_customers_count_week = parking_requests_week.values('user__email').distinct().count()

        labels_week.append(str(date))
        data_week.append({
            'total_value': total_value_week,
            'total_customers': unique_customers_count_week,
        })

    # Monthly report
    monthly_data = ApprovedRequest.objects.annotate(month=TruncMonth('date')).values('month').annotate(
        total_value=Sum('total_price'),
        total_customers=Count('user__email', distinct=True)
    ).order_by('month')

    labels_month = []
    data_month = []

    for entry in monthly_data:
        month_key = entry['month'].strftime('%Y-%m')
        labels_month.append(month_key)
        data_month.append({
            'total_value': entry['total_value'] or 0,
            'total_customers': entry['total_customers'],
        })

    # Prepare the context
    context = {
        'daily_report': {
            'labels': formatted_daily_report['labels'],
            'data': formatted_daily_report['data'],
        },
        'weekly_report': {
            'labels': labels_week,
            'data': data_week
        },
        'monthly_report': {
            'labels': labels_month,
            'data': data_month
        }
    }
    return render(request, 'report/parkingReport.html', context)

@role_auth_decorator(role=2)
def parking_profile(request):
    profile = Profile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        form = UserForm(request.POST, instance=request.user)

        # Initialize a flag to check if any form is valid
        is_valid = True

        # Validate UserForm
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Has Been Updated')
        else:
            is_valid = False
            messages.error(request, 'User  Form is not valid')

        # Validate ProfileForm
        if profile_form.is_valid():
            profile_form_instance = profile_form.save(commit=False)
            profile_form_instance.user = request.user
            profile_form_instance.save()
            messages.success(request, 'Profile Image Has Been Updated')
        else:
            is_valid = False
            messages.error(request, 'Profile Image Form is not valid')

        # Redirect if any of the forms were valid
        if is_valid:
            return redirect('parking_profile')

    else:
        form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'profile/parkingProfile.html', {'form': form, 'profile_form': profile_form})

@role_auth_decorator(role=2)
def parking_password(request):
            User = request.user
            if request.method == 'POST':
                  current_password = request.POST.get('oldPassword')
                  new_password = request.POST.get('newPassword')
                  confirm_password = request.POST.get('confirmPassword')

                  # Check if the current password is correct
                  if check_password(current_password, User.password) or current_password== User.password:
                        # Check if the new password and confirm password match
                        if new_password == confirm_password:
                              User.set_password(new_password)
                              User.save()
                              messages.success(request, 'Password has been updated successfully.')
                              return redirect('parking_login')
                        else:
                              messages.error(request, 'New password and confirmation do not match.')
                        return redirect('user_profile')
                  else:
                        messages.error(request, 'User  Password Is Incorrect')
                        return redirect('user_profile')
            else:
                  messages.error(request, 'Invalid request method. Only POST requests are allowed.') 
            return render(request, 'profile/parkingPassword.html')

@role_auth_decorator(role=2)
def parking_data(request):
    parking_admin = ParkingGroupMember.objects.filter(user = request.user).first()
    parking = Parking.objects.get(id = parking_admin.parking.id)
    
    if request.method == 'POST':
        form = ParkingForm(request.POST, request.FILES, instance=parking)
        
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user = request.user
            
            # Retain the is_sent value
            if parking is not None:
                form_instance.is_sent = parking.is_sent  # Always retain the current value
            else:
                form_instance.is_sent = False  # Set to False or handle accordingly if parking is None
            
            form_instance.save()  # Save the form instance
            messages.success(request, 'Parking Data Updated')
            
            return redirect('parking_home')
    else:
        form = ParkingForm(instance=parking)
    
    # Pass is_sent to the template context, with a check for None
    is_sent = parking.is_sent if parking else False
    
    return render(request, 'profile/parkingData.html', {'form': form, 'is_sent': is_sent})


@role_auth_decorator(role=2)
def parking_working_hour(request):
    parking_admin = ParkingGroupMember.objects.filter(user = request.user).first()
    parking = Parking.objects.get(id = parking_admin.parking.id)
    working_days = WorkingHours.objects.filter(parking=parking)
    context = {
        'working_days': working_days,
    }
    return render(request, 'profile/ParkingWorkingHour.html', context)

@role_auth_decorator(role=2)
def toggle_working_day(request, id):
    working_day = WorkingHours.objects.get(id=id)
    if working_day.is_available:
        working_day.is_available = False
        working_day.save()
        messages.success(request, 'Working Date Update Successfuly')
        return redirect('parking_working_hour')
    else:
        working_day.is_available = True
        working_day.save()
        messages.success(request, 'Working Date Update Successfuly')
        return redirect('parking_working_hour')

@role_auth_decorator(role=2)
def update_working_hour(request, id):
    if request.method == "POST":
        workingDay = WorkingHours.objects.get(id=id)
        start_time = request.POST['start_time'][:-3]
        end_time = request.POST['end_time'][:-3]

        if start_time is not None and end_time is not None:  # Check if start_time and end_time are not None
            workingDay.start_time = start_time  # Remove the comma after start_time
            workingDay.end_time = end_time  # Remove the comma after end_time
            workingDay.save()

            messages.success(request, 'Time Updated Successfully')
            return redirect('parking_working_hour')
        
    else:
        return redirect('parking_working_hour')

@role_auth_decorator(role=2)    
def request_send(request):
    parking_admin = ParkingGroupMember.objects.filter(user = request.user).first()
    parking = Parking.objects.get(id = parking_admin.parking.id)
    if parking is  None:
        messages.error(request, 'No Parking Profile Is Set Up, Please Set Up Now')
        return redirect('parking_data')
    else:
        if parking.is_sent:
            messages.error(request, 'Reqest Have Already Been Sent')
            return redirect('parking_home')
        else:
            requestList = Request(
                parking=parking
            )
            requestList.save()
            parking.is_sent =True
            parking.save()
            messages.success(request, 'Request Have Been Sent Successfuly')
            return redirect('parking_home')
    

@role_auth_decorator(role=2)
def check_status(request, parkings):
    avaliable_parking = []
    current_date = dt.now().date().weekday()  # Get current day of the week as an integer
    current_time = dt.now().time()  # Get current time

    for park in parkings:
        working_days = WorkingHours.objects.filter(parking=park)
        
        for day in working_days:
            # Convert day.day to an integer for comparison
            day_of_week = int(day.day)  # Assuming day.day is a string like "0", "1", etc.
            
            if day_of_week == current_date:
                if day.start_time <= current_time <= day.end_time:
                    avaliable_parking.append(park)
                    break  # No need to check other days for this parking

    if not avaliable_parking:
        messages.warning(request, 'Looks like there are no available parkings at this time.')
        return redirect('user_home')
    
    return avaliable_parking
            
class NearestParkingView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Get the user's location from the request body
            data = json.loads(request.body.decode('utf-8'))
            user_location = (data['latitude'], data['longitude'])
            # Fetch all parking spots from the database
            parkings = Parking.objects.filter(is_active=True, is_approved=True)
            # List to store parking spots with their distances
            parking_data = []
            parking_list = []

            for parking in parkings:
                # Extract latitude and longitude from the PointField
                if parking.location:
                    parking_location = (parking.location.y, parking.location.x)  # (latitude, longitude)

                    # Calculate the distance
                    distance = geodesic(user_location, parking_location).kilometers
                    # Only consider parking spots within a 10 km radius
                    if distance <= 10:
                        parking_data.append({
                            'id': parking.id,
                            'address': parking.address,
                            'slot_capacity': parking.slot_capacity,
                            'available_slots': parking.available_slots,
                            'image1': request.build_absolute_uri(parking.image1.url) if parking.image1 else None,
                            'image2': request.build_absolute_uri(parking.image2.url) if parking.image2 else None,
                            'name': parking.name,
                            'distance': round(distance, 2),
                            'price': str(parking.price_per_hour),
                            'latitude': parking_location[0],
                            'longitude': parking_location[1],
                        })
                        parking_list.append(parking)

            # Store the nearest parking spots in the session
            request.session['nearest_parkings'] = parking_data
            print(parking_list)

            # Call a helper function to filter further, if needed
            # avaliable_parking = check_status(request, parking_list)

            # Serialize the parking data
            serialized_data = [
                {
                    'id': park.id,
                    'address': park.address,
                    'available_slots': park.available_slots,
                    'slot_capacity': park.slot_capacity,
                    'image1': request.build_absolute_uri(park.image1.url) if park.image1 else None,
                    'image2': request.build_absolute_uri(park.image2.url) if park.image2 else None,
                    'name': park.name,
                    'price': str(park.price_per_hour),
                    'latitude': park.location.y,
                    'longitude': park.location.x,
                }
                for park in parking_list
            ]
            # print(avaliable_parking)

            # Prepare response data
            response_data = {
                'parkings': serialized_data,
            }

            return JsonResponse(response_data)

        except KeyError as e:
            return JsonResponse({'error': f"Missing key: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@role_auth_decorator(role=2)
def cash_payment(request, id):
    approved_request = ApprovedRequest.objects.get(id=id)
    payments = Payment(
        request_id = approved_request,
        tx_ref = approved_request.reference_trx,
        user = approved_request.user,
        amount = approved_request.total_price,
        currency = 'BIRR',
        status  = 'successful',
    )
    payments.save()
    approved_request.payment_status = True
    approved_request.save()
    messages.success(request, 'Payment Added Successfuly')

    return redirect('parking_approved_request_detail', id=approved_request.id)