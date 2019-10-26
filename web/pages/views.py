from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Site, CE
from django.urls import reverse
from django.core.serializers import serialize
from django.core.management import call_command

# Create your views here.
def map(request):
    # Needs to be site list OR sponsor list,
    site_list = list(Site.objects.all().values(''))
    return render(request, "map.html", {'site_list': site_list})

def sponsor(request):
    ce_list = list(CE.objects.all())
    return render(request, "sponsor.html", {'ce_list': ce_list})

def update(request):
    call_command('fetchdata')
    return HttpResponseRedirect(reverse('map'))

def site_data(request):
    sites = serialize('json', Site.objects.all())
    return HttpResponse(sites, content_type='json')

def details(request, siteid):
    site = get_object_or_404(Site, pk=siteid)
    return render(request, 'details.html', {'site': site})
