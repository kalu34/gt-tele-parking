from django.shortcuts import redirect
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from authentication.models import User,UserRoles


def role_auth_decorator(role):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                try:
                    user = User.objects.get(id=request.user.id)
                    # Check User.role first
                    if user.role == role:
                        return func(request, *args, **kwargs)

                    # If User.role doesn't match, check UserRoles
                    user_roles = UserRoles.objects.filter(user=user)
                    if user_roles.exists():
                        user_role = user_roles.first()
                        if user_role.role == role:
                            return func(request, *args, **kwargs)
                        
                        logout(request)
                        messages.error(request, 'You do not have permission to access this page.')
                        return redirect('/admin')


                    # If neither User.role nor UserRoles.role matches, deny access
                    logout(request)
                    messages.error(request, 'User is not found in the User Role Form')
                    return redirect('/admin')

                except ObjectDoesNotExist:
                    messages.error(request, 'User not found.')
                    return redirect('/admin')
            else:
                messages.error(request, 'Please log in to access this page.')
                return redirect('/admin')

        return wrapper
    return decorator

def role_user_decorator(role):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            try:
                user = request.user
                if user.role != role:
                      logout(request)
                      messages.error(request, 'User role is not correct')
                      return redirect('/user-login')
                else:
                    return func(request, *args, **kwargs)
            except ObjectDoesNotExist:
                return redirect('/user-login')
            except Exception as e:
                messages.error(request, 'anonymous user role, User Do not have role')
                return redirect('/user-login')
        return wrapper
    return decorator


