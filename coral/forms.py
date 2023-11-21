from django import forms
from django.forms import ModelForm, Select
from .models import Coral, Photos


class DateInput(forms.DateInput):
    input_type = 'date'

class photoForm(forms.ModelForm):
    class Meta:
        model = Photos
        fields = ['coral',"image_date","images"]
        widgets = {'image_date': DateInput(),}
class CoralForm(forms.ModelForm):

    class Meta:
        model = Coral
        fields = [
            "name",
            "description",
            "status",
            "source",
            "purchaseDate",
            "purchaseCost",
            "image",
            'user']
        widgets = {
            'purchaseDate': DateInput(),
            'status': Select(),
        }
class CoralFilterForm(forms.Form):
    species = forms.ModelChoiceField(
        queryset=Coral.objects.values_list('species', flat=True).distinct(),
        empty_label='All Species',
        required=False,
    )

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
