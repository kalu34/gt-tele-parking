from django import forms
from .models import Payment, Incident

class IncidentForm(forms.ModelForm):
  class Meta:
    model = Incident
    fields = ['incident_type','reason','evidence']

  def __init__(self, *args, **kwargs):
        super(IncidentForm, self).__init__(*args, **kwargs)
        for field_item in self.fields:
            self.fields[field_item].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter ' + field_item.capitalize()})

