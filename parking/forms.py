from typing import Any
from django import forms
from .models import Parking, WorkingHours, ParkingGroup, ParkingGroupMember
from django.contrib.gis.geos import Point

class ParkingForm(forms.ModelForm):
    latitude = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    longitude = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Parking
        fields = ['name', 'address', 'location', 'is_sent','is_active', 'has_ev_charging', 'has_disabled_parking', 'is_covered', 'has_security_cameras', 'has_security_guard', 'payment_method', 'amenities', 'subcity', 'woreda', 'keble', 'price_per_hour', 'price_per_day', 'slot_capacity', 'available_slots', 'image1', 'image2','is_approved','is_sent','latitude','longitude']
        fields_control = ['name', 'address', 'location', 'subcity', 'woreda', 'keble', 'price_per_hour', 'price_per_day', 'slot_capacity', 'available_slots', 'payment_method', 'amenities', 'image1', 'image2','latitude','longitude']
        fields_check = ['has_ev_charging', 'has_disabled_parking', 'is_covered', 'has_security_cameras', 'has_security_guard']

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')

        if latitude and longitude: #Check if both are filled.
            try:
                cleaned_data['location'] = Point(float(longitude), float(latitude), srid=4326) #Convert to float.
            except (ValueError, TypeError):
                self.add_error('latitude', 'Invalid latitude or longitude.')
                self.add_error('longitude', 'Invalid latitude or longitude.')
                cleaned_data['location'] = None #Prevent error if Point creation fails.
        else:
            cleaned_data['location'] = None #Set location to None if lat/long are not filled.

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name in self.Meta.fields_control:
                field.widget.attrs.update({
                    'class': 'form-control',
                })
            elif field_name in self.Meta.fields_check:
                field.widget.attrs.update({
                    'class': 'form-check-input',
                })

class ParkingGroupForm(forms.ModelForm):
    class Meta:
        model = ParkingGroup
        fields = ['subcity', 'woreda', 'kebele', 'name']

    def __init__(self, *args, **kwargs):
        super(ParkingGroupForm, self).__init__(*args, **kwargs)
        for field_item in self.fields:
            self.fields[field_item].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter ' + field_item.capitalize()})

class ParkingGroupMemberForm(forms.ModelForm):
    class Meta:
        model = ParkingGroupMember
        fields = ['is_admin','end_date']

    def __init__(self, *args, **kwargs):
        super(ParkingGroupMemberForm, self).__init__(*args, **kwargs)
        self.fields['is_admin'].widget.attrs.update({'class': 'form-check-input ms-2'})
        self.fields['end_date'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
