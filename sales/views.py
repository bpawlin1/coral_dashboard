from django.shortcuts import render

from coral.models import Coral
from sales.models import coral_sale
from django.db.models import Sum
from django.db.models import Count
from django.contrib import messages
from django.urls import reverse_lazy  # new
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ( CreateView, UpdateView,DeleteView,DetailView, ) # new
from sales.forms import saleform  # new
import datetime

def sale_tables(request):
    coral_species = coral_sale.objects.filter().values('species').order_by('species').annotate(species_amount=Count('species'))
    coral_sold = coral_sale.objects.filter().values('coral_name').order_by('coral_name').annotate(coral_sum=Sum('sale_price')).annotate(coral_amount=Count('coral_name'))
    values = coral_sale.objects.filter().values('sale_date').order_by('sale_date').annotate(sum=Sum('sale_price'))
    context = {
    'sale_date': values,
    'spi' : coral_species, 
    'coral' : coral_sold,
        
    }
    return render(request, 'tables.html', context)
    

def sales(request):
    #purchaseDate  = Coral.objects.values('purchaseDate', 'purchaseCost').distinct()
    today = datetime.date.today()
    labels = []
    data = []
    current_year = datetime.date.today().year
    values = coral_sale.objects.filter().values('sale_date').order_by('sale_date').annotate(sum=Sum('sale_price'))
    sales_total = coral_sale.objects.all().aggregate(Sum('sale_price'))['sale_price__sum'] or 0
    current_year_sales = coral_sale.objects.all().filter(sale_date__year = today.year).aggregate(Sum('sale_price'))['sale_price__sum'] or 0
    coral_sold = coral_sale.objects.filter().values('coral_name').order_by('coral_name').annotate(coral_sum=Sum('sale_price')).annotate(coral_amount=Count('coral_name'))
    current_year_bought = Coral.objects.all().filter(purchaseDate__year = today.year).aggregate(Sum('purchaseCost'))['purchaseCost__sum'] or 0
    net_total = current_year_sales - current_year_bought
    
    coral_count = coral_sale.objects.count()

    coral_species = coral_sale.objects.filter().values('species').order_by('species').annotate(species_amount=Count('species'))
    species =  coral_sale.objects.all().values('species').distinct()

    lps = coral_sale.objects.filter(species='LPS').count()
    lps = int(lps)
    Zoa = coral_sale.objects.filter(species='Zoa').count()
    Zoa = int(Zoa)
    Softy = coral_sale.objects.filter(species='Softy').count()
    Softy = int(Softy)
    Algae = coral_sale.objects.filter(species='Algae').count()
    Algaeps = int(Algae)
    Gorgonian = coral_sale.objects.filter(species='Gorgonian').count()
    Gorgonian = int(Gorgonian)
    Anemone = coral_sale.objects.filter(species='Anemone').count()
    Anemone = int(Anemone)
    sps = coral_sale.objects.filter(species='SPS').count()
    sps = int(sps)

    species_list = ['lps', 'Zoa', 'Softy','Algae','Gorgonian','Anemone','SPS' ]
    species_number = [lps, Zoa, Softy, Algae, Gorgonian, Anemone, sps   ]
    

    context = {

        'sum' : values, 
        'coral_sum' : coral_sold,
        'coral_amount' : coral_sold,
        'spi' : coral_species,
        'species_amount' : coral_species,
        'species_list' : species_list,
        'species_number' : species_number,
        'sales_total' : sales_total,
        'coral_count' : coral_count,
        'current_year_sales' : current_year_sales,
        'current_year_bought' : current_year_bought,
        'net_total': net_total,
     
        
    }
    return render(request, 'sales.html', context)

class CreateCoralSale(SuccessMessageMixin,CreateView):  # new
    model = coral_sale
    form_class = saleform
    template_name = "newSale.html"
    success_message = "Your sale was added!"
    success_url = reverse_lazy("sales")

    def form_valid(self, form):
        # Set the user field before saving the form
        form.instance.user = self.request.user

        # Call the parent class's form_valid method to save the form
        response = super().form_valid(form)

        return response