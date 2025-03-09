from django import forms
from authentication.models import User, UserRoles, Woreda
from django.core.exceptions import ValidationError

class WoredaRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number']
    
    def __init__(self, *args, **kwargs):
        super(WoredaRegisterForm, self).__init__(*args, **kwargs)
        self.apply_common_attrs()    

    def apply_common_attrs(self):
        placeholders = {
            'username': '@Jhon',
            'email': 'Jhon@gmail.coom',
            'first_name': 'Jhon',
            'last_name': 'James',
            'phone_number': '222-111-238',
        }
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field_name, 'Enter ' + field.label)  # Default placeholder
            })
    
    def clean(self):
        data = super().clean()

        username = data.get('username')
        email = data.get('email')  # Fixed typo: 'eamil' to 'email'
        phone_number = data.get('phone_number')
        
        if User.objects.filter(username=username).exists():
            raise ValidationError('User with this username already exists')
        
        if User.objects.filter(email=email).exists():
            raise ValidationError('User with this email already exists')
        
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('User with this phone number already exists')

        return data
    

class WoredaAdminRoleForm(forms.ModelForm):
    class Meta:
        model = UserRoles
        fields = ['woreda']

    def __init__(self, *args, **kwargs):
        super(WoredaAdminRoleForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
            })

        if self.instance and self.instance.subcity:
            subcity = self.instance.subcity
            self.fields['woreda'].queryset = Woreda.objects.filter(subcity=subcity)
        else:
            self.fields['woreda'].queryset = Woreda.objects.none()


    def clean(self):
        data = super().clean()

        woreda = data.get('woreda')
        subcity = self.instance.subcity
        
        if UserRoles.objects.filter(subcity=subcity, woreda=woreda).exists():
            raise ValidationError("This woreda is already assigned to this subcity.")
        
        return data

