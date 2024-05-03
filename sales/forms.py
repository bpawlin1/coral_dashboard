from django import forms
from django.forms import ModelForm, Select
from sales.models import coral_sale
from coral.models import Coral

SPECIES_CHOICES= [
    ('SPS', 'SPS'),
    ('LPS', 'LPS'),
    ('Zoa', 'Zoa'),
    ('Algae', 'Algae'),
    ('Anemone','Anemone'),
    ('Gorgonian','Gorgonian'),
    ('Softy', 'Softy'),
    ]

class DateInput(forms.DateInput):
        input_type = 'date'
        
class saleform(forms.ModelForm):
    coral_name = coral_name = forms.ModelChoiceField(queryset=Coral.objects.all())
   
    class Meta:
        model = coral_sale
        fields = ["coral_name", "sale_price", "sale_date" , "species", 'user']
        widgets = {
            'sale_date': DateInput(),
            'species' : forms.Select(choices=SPECIES_CHOICES),
        }




