from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Car, LegalDocument
from authentication.models import PlateNumber
from parking.models import Parking
from core.models import ApprovedRequest, ReservedRequest,Payment, ReserveParking
from django.views.decorators.csrf import csrf_exempt
from authentication.models import User, Profile, Wallet, Transaction
from .forms import CarForm, LegalDocumentForm
from authentication.forms import UserForm, ProfileForm
from django.contrib.auth.hashers import check_password
from django.contrib import messages

# Custom Decorator Import 

from authentication.RoleDecorator.decorators import role_user_decorator

@role_user_decorator(role=1)
def user_home(request):
    if request.user.is_authenticated: 
        # Proceed with your logic ONLY if the user is authenticated
        parking_appointment = ReserveParking.objects.filter(user=request.user, status=True).first()
        parking_reserved = ReservedRequest.objects.filter(user=request.user).first()
        preceding_parking_reserved_request = ReservedRequest.objects.all().count()
        parking_request_active = ApprovedRequest.objects.filter(user=request.user, is_active=True).first()
        parking_request_pending = ApprovedRequest.objects.filter(user=request.user, is_active=False, payment_status=False).first()
        car = None
        if request.user.role == User.USER_ROLE:
            car = PlateNumber.objects.filter(user=request.user).first()

        if not car:
            return redirect('user-login')

        profile, created = Profile.objects.get_or_create(user=request.user)
        if created:
            messages.warning(request, 'Profile Image is not updated, Please Upload Profile Picture')
            return redirect('user_profile')  # Or wherever you want to redirect

        context = {
            'parking_appointment': parking_appointment,
            'parking_request_active': parking_request_active,
            'parking_requests_pending': parking_request_pending,
            'parking_reserved_request': parking_reserved,
            'preceding_resrved': preceding_parking_reserved_request - 1,
            'car': car,
            'profile': profile,
        }
        return render(request, 'userHome.html', context)
    else:
        return redirect('user_login')  

@role_user_decorator(role=1)
def user_listing(request):
    parkings = Parking.objects.all()
    profile = Profile.objects.get(user=request.user)
    context ={
        'parkings': parkings,
        'profile':profile
    }
    return render(request, 'userListing.html', context)

@role_user_decorator(role=1)
def user_history(request):
    parking_payments = Payment.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    context = {
        'parking_payments':parking_payments,
        'no_parking_payment':not parking_payments,
         'profile':profile
    }
    return render(request, 'userHistory.html', context)

@role_user_decorator(role=1)
def remove_request(request, request_id):
     parking_request = ReservedRequest.objects.get(id=request_id)
     if parking_request.slot == None:
        parking_request.delete()
        messages.success(request, 'Parking request Deleted successfully!')
        return redirect('user_home')
     else:
        messages.error(request, 'Parking request Already Reserved, You Can Stop And Pay!')
        return redirect('user_home')

@role_user_decorator(role=1)
def stop_request(request, request_id):
     parking_request = ApprovedRequest.objects.get(id=request_id)
     parking_request.stop = True
     parking_request.save()
     messages.success(request, 'Parking request Stopped successfully!')
     return redirect('user_home')

@role_user_decorator(role=1)
def user_payment(request):
    payment_list = Payment.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    context = {
        'payment_historys': payment_list,
        'no_payments': not payment_list.exists(),  # Add a flag to check if there are no payments
        'profile':profile,
    }
    
    return render(request, 'userPayment.html', context)

@role_user_decorator(role=1)
@csrf_exempt
def create_payment(request):
    if request.method == 'GET':
        try:
            payment_status = request.GET.get('status')
            tx_ref = request.GET.get('trx_ref')

            parking_request = ApprovedRequest.objects.filter(reference_trx=tx_ref).first()

            if parking_request:
                if payment_status == 'success':
                    parking_request.payment_status = True
                    parking_request.save()

                    payment = Payment.objects.create(
                        request_id=parking_request,
                        tx_ref=tx_ref,
                        user=parking_request.user,
                        amount=parking_request.total_price,
                        status="SUCCESSFUL"
                    )
                    messages.success(request, 'Your Payment Has Been Processed Successfully. Please Check Your Email For More Details')
                    return redirect('user_payment')

                else:
                    return messages.error(request, 'Payment Is not successful, Plesase Try Again!!')

            else:
                return messages.error(request, 'Parking Request Not Found')

        except Exception as e:
            return messages.error(request, 'Exception Error ')

    else:
        return messages.error(request, 'Invalid Request Method ')

@role_user_decorator(role=1)
def user_profile(request):   
    car = Car.objects.filter(user=request.user).first()  
    
    # Use filter and first() to safely get the document or None
    document = LegalDocument.objects.filter(car=car).first()

    if request.method == "POST":
        car_form = CarForm(instance=car)
        legal_document_form = LegalDocumentForm(instance=document)
        profile_form = UserForm(instance=request.user)
        print('post request is activated')
    else:
        car_form = CarForm(instance=car)
        legal_document_form = LegalDocumentForm(instance=document)
        profile_form = UserForm(instance=request.user)

    context = {
        'car_form': car_form,
        'legal_document_form': legal_document_form,
        'profile_form': profile_form,
    }

    return render(request, 'profile/userProfile.html', context)

@role_user_decorator(role=1)
def create_or_update_car(request, user_id):
    # Get the user instance
    user = get_object_or_404(User, id=user_id)

    car = Car.objects.filter(user=user).first()

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            car_instance = form.save(commit=False)  # Save the form but do not commit to the database yet
            car_instance.user = user  # Assign the user to the car instance
            car_instance.save()  # Now save the car instance to the database

            messages.success(request, 'Car information saved successfully!')

            # Redirect to a success URL
            return redirect('user_profile')  # Replace with your success URL

    # If it's a GET request or the form is invalid, you can also add a message
    messages.error(request, 'Invalid request method or form submission failed.')
    return redirect('user_profile')  # Replace with the appropriate URL


@role_user_decorator(role=1)
def create_or_update_user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        form_image = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'User information saved successfully!')
            return redirect('user_profile')
        

    messages.error(request, 'Invalid request method or form submission failed.')
    return redirect('user_profile')  # Replace with the appropriate URL


@role_user_decorator(role=1)
def create_or_update_user_profile_image(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Use get_object_or_404 for user as well
    profile = get_object_or_404(Profile, user=user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile picture has been updated.')
            return redirect('user_profile')
        else:
            messages.error(request, 'Form submission failed. Please correct the errors.')
    else:
        messages.error(request, 'Invalid request method. Only POST requests are allowed.')

    return redirect('user_profile')


@role_user_decorator(role=1)
def create_or_update_document(request, user_id):
    user = get_object_or_404(User, id=user_id) 
    car = Car.objects.filter(user=user).first()
    document = LegalDocument.objects.filter(car=car).first()
    
    if request.method == 'POST':
        form = LegalDocumentForm(request.POST, request.FILES, instance=document)
        
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user = user
            form_instance.car = car
            form_instance.save()
            messages.success(request, 'File has been uploaded successfully.')
            return redirect('user_profile')
        else:
            messages.error(request, 'Form is not valid. Please correct the errors and try again.')
    
    # Handle the case for GET request or any other method
    return redirect('user_profile')

# User Wallet Logic Impliment

@role_user_decorator(role=1)
def user_wallet(reqeust):
    wallet = Wallet.objects.filter(user = reqeust.user).first()
    transactions = Transaction.objects.filter(wallet=wallet).order_by('-date')[:5]

    context = {
        'wallet':wallet,
        'transaction':transactions
    }
    return render(reqeust, 'userWallet.html', context)



@role_user_decorator(role=1)
def pay_now(request, id):
    pending_request = ApprovedRequest.objects.get(id=id)
    wallet = Wallet.objects.filter(user=request.user).first()

    wallet = wallet.debit(pending_request.total_price, pending_request.reference_trx)
    if(wallet):
        payment = Payment(
            request_id = pending_request,
            tx_ref = pending_request.reference_trx,
            user = request.user,
            amount = pending_request.total_price,
            status = "successful"
        )
        payment.save()
        pending_request.payment_status = True
        pending_request.save()
        messages.success(request, 'Payment Completed Successfuly')
        return redirect('user_wallet')
    else:
        messages.warning(request, 'Incefficient Balance, Recharge Your Wallet')
        return redirect('user_wallet')
    
@role_user_decorator(role=1)
def pay_reserve_now(request, id):
    reserved_request = ReserveParking.objects.get(id=id)
    wallet = Wallet.objects.filter(user=request.user).first()

    if not reserved_request.payment_status: 
        wallet = wallet.debit(reserved_request.total_price, reserved_request.request_ref)
        if(wallet):
            approved_request = ApprovedRequest(
                user = reserved_request.user,
                parking = reserved_request.parking,
                reference_trx = reserved_request.request_ref,
                slot = reserved_request.slot,
                start_time = reserved_request.start_time,
                end_time = reserved_request.end_time,
                payment_status = True,
                is_active = False,
                stop = False,
                payment_per_hour = reserved_request.parking.price_per_hour,
                total_price = reserved_request.total_price
            )
            approved_request.save()

            payment = Payment(
                request_id = approved_request,
                tx_ref = reserved_request.request_ref,
                user = request.user,
                amount = reserved_request.total_price,
                status = "successful"
            )
            payment.save()
            reserved_request.payment_status = True
            reserved_request.save()
            messages.success(request, 'Payment Completed Successfuly')
            return redirect('user_wallet')
        else:
            messages.warning(request, 'Incefficient Balance, Recharge Your Wallet')
            return redirect('user_wallet')
    else:
        messages.warning(request, 'payment already made, please check your history')
        return redirect('user_wallet')