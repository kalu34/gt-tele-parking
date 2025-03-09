from django import forms
from .models import Car, LegalDocument, UserLegalDocument

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name','make', 'model', 'year', 'color', 'mileage', 'plate_number', 'image']
    
    def __init__(self, *args, **kwargs):
        super(CarForm, self).__init__(*args, **kwargs)
        self.apply_common_attrs()

    def apply_common_attrs(self):
        placeholders = {
            'name': 'Enter car name',
            'make': 'Enter car make',
            'model': 'Enter car model',
            'year': 'Enter manufacturing year',
            'color': 'Enter car color',
            'mileage': 'Enter mileage in km',
            'plate_number': 'Enter license plate number',
            'image': 'Upload car image',
            # Add more fields and their placeholders as needed
        }

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field_name, 'Enter ' + field.label)  # Default placeholder
            })

class LegalDocumentForm(forms.ModelForm):
    class Meta:
        model = LegalDocument
        fields = ['document', 'document_type', 'issue_date', 'expiry_date']

    def __init__(self, *args, **kwargs):
        super(LegalDocumentForm, self).__init__(*args, **kwargs)
        self.apply_common_attrs()

    def apply_common_attrs(self):
        placeholders = {
            'document': 'Legal Document',
            'document_type': 'Liberay',
            'issue_date': 'YYYY - MM - DD',
            'expiry_date': 'YYYY - MM - DD',
        }

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field_name, 'Enter ' + field.label)  # Default placeholder
            })

class UserLegalDocumentForm(forms.ModelForm):
    class Meta:
        model = UserLegalDocument
        fields = ['driving_licence','national_id']

    def __init__(self, *args, **kwargs):
        super(UserLegalDocumentForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
