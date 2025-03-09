from django import forms
from core.models import DeletedInstance, ApprovedRequestAdmin, DecliendRequestAdmin

class DeletedInstanceForm(forms.ModelForm):
  class Meta:
    model = DeletedInstance
    fields = ['reason']

  def __init__(self, *args, **kwarga):
    super(DeletedInstanceForm, self).__init__(*args, **kwarga)
    self.fields['reason'].widget.attrs.update({'class':'form-control'})

class ApprovedRequestAdminForm(forms.ModelForm):
    class Meta:
      model = ApprovedRequestAdmin
      fields = ['message']
    def __init__(self, *args, **kwarga):
      super(ApprovedRequestAdminForm, self).__init__(*args, **kwarga)
      self.fields['message'].widget.attrs.update({'class':'form-control'})

class DecliendRequestAdminForm(forms.ModelForm):
  class Meta:
    model = DecliendRequestAdmin
    fields = ['message']

  def __init__(self, *args, **kwarga):
    super(DecliendRequestAdminForm, self).__init__(*args, **kwarga)
    self.fields['message'].widget.attrs.update({'class':'form-control'})