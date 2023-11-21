from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from coral.models import Coral, Photos
from django.views.generic import ( CreateView, UpdateView,DeleteView,DetailView, ) # new
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy  # new
from .forms import CoralForm, LoginForm, photoForm  # new
from django.views.generic import CreateView
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

#@login_required
def accounting(request):
    #purchaseDate  = Coral.objects.values('purchaseDate', 'purchaseCost').distinct()

    

    values = Coral.objects.filter().values('purchaseDate').order_by('purchaseDate').annotate(sum=Sum('purchaseCost'))
    context = {
        'purchaseDate': values,
        'sum' : sum
        
    }
    return render(request, 'accounting.html', context)

def index(request):
    user = request.user
    coral_name_filter = request.GET.get('coral_name', '')
    species_filter = Coral.objects.all().values('species').distinct()
    #coral = Coral.objects.filter(user=request.user).order_by('name')
    coral_queryset = Coral.objects.filter(user=request.user).order_by('name')

    # Apply the search filter if a search term is provided
    if coral_name_filter:
        coral_queryset = coral_queryset.filter(name__icontains=coral_name_filter)

    # Apply the species filter if a species is selected
    if species_filter:
        coral_queryset = coral_queryset.filter(species=species_filter)

    paginator = Paginator(coral_queryset, per_page=12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'corals': page_obj,
        'coral_name_filter': coral_name_filter,
        'species_filter': species_filter,  # Pass the filter value to the template
    }
    return render(request, 'index.html', context)

#@login_required
def coral_detail(request, pk):
    coral = Coral.objects.get(pk=pk)
    images = Photos.objects.filter(coral=coral)
    print(images)
    context = {
        'coral': coral,
        'images': images
    }
    return render(request, 'coral_detail.html', context)
#@login_required
class CreateCoralView(SuccessMessageMixin,CreateView):  # new
    model = Coral
    form_class = CoralForm
    template_name = "newCoral.html"
    success_message = "Your coral was added!"
    success_url = reverse_lazy("index")
    
#@login_required
class UpdatePhotoView(SuccessMessageMixin, CreateView):
    model = Photos
    form_class = photoForm
    template_name = "growthShotUpdate.html"
    

    success_message = "Your photo was added!"
    success_url = reverse_lazy("index")

#@login_required
class UpdateCoralView(SuccessMessageMixin, UpdateView):
    model = Coral
    template_name = "updateCoral.html"
    form_class = CoralForm

    success_message = "Your entry was updated!"
    success_url = reverse_lazy("index")
    
#@login_required
class DeleteCoralView(DeleteView):
    model = Coral
    form_class = CoralForm
    template_name = "coralDelete.html"
    success_message = "Your entry was deleted!"
    success_url = reverse_lazy("index")
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

