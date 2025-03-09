from django import forms
from .models import User,Profile, UserRoles
from django.core.exceptions import ValidationError

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_parking = True
        if commit:
            user.save()
        return user
    

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.apply_common_attrs()    

    def apply_common_attrs(self):
        placeholders = {
            'username': '@Jhon',
            'email': 'Jhon@gmail.coom',
            'first_name': 'Jhon',
            'last_name': 'James',
            'phone_number': '222-111-233',
            'address': 'Addis Ababa',
        }
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field_name, 'Enter ' + field.label)  # Default placeholder
            })

        

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.apply_common_attrs()

    def apply_common_attrs(self):
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
            })

class RoleForm(forms.ModelForm):
    class Meta:
        model = UserRoles
        fields = ['subcity']

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        data = super().clean()
        woreda = data.get('woreda')
        subcity = data.get('subcity')
        form_instance = self.instance

        # Check if the instance exists (edit mode)
        if form_instance and form_instance.pk:
            # Edit mode validation: Prevent duplicate subcity/woreda for role 4
            if UserRoles.objects.filter(role=4, woreda=woreda, subcity=subcity).exclude(pk=form_instance.pk).exists():
                raise ValidationError('Another User Has The Assigned Role, Please Check Again')
            return data

        # Check if subcity and woreda already have a role 4 assignment
        if UserRoles.objects.filter(role=4, subcity=subcity).exists():
            raise ValidationError('The Assigned subcity and woreda have an admin assigned for them, please check the admin list')

        return data