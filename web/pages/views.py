from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Site, CE
from django.urls import reverse
from django.core.serializers import serialize
from django.core.management import call_command

# Create your views here.
def map(request):
    # Needs to be site list OR sponsor list,
    site_list = list(Site.objects.all())
    return render(request, "map.html", {'site_list': site_list})

def sponsor(request):
    ce_list = list(CE.objects.all())
    return render(request, "sponsor.html", {'ce_list': ce_list})

def site_data(request):
    sites = serialize('json', Site.objects.all())
    return HttpResponse(sites, content_type='json')

def details(request, siteid):
    site = get_object_or_404(Site, pk=siteid)
    return render(request, 'details.html', {'site': site})

def points(request):
    if request.method == 'GET':
        south_west = request.GET['south_west']
        north_east = request.GET['north_east']

        site_list = list(Site.objects.all())
        sites_to_render = list()
        for site in site_list:
            if site.latitude >= south_west.latitude and site.latitude <= north_east.latitude \
                and site.longitude >= south_west.longitude and site.longitude <= north_east.longitude:
                sites_to_render.append(site)

        return JsonResponse({'result': "success", 'sites': sites_to_render})
    else:
        return JsonResponse({'result': "unsuccessful"})
