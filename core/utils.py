from django.utils import timezone
# Importing Model
from .models import ReserveParking, ApprovedRequest



def generate_time_interval(start_time, end_time):
    now = timezone.now()
    if(start_time > now):
        return ((now - start_time).total_seconds(), False)
    
    return((end_time -now).total_seconds(), True)


def check_reserve_or_approved(user):
    
    if(ReserveParking.objects.filter(user = user, status = True)).first():
        if(ApprovedRequest.objects.filter(user = user).first()):
            return True
        
    return False
    

    

