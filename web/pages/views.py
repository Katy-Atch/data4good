from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Site, CE, GEO
from django.urls import reverse
from django.core.serializers import serialize
from django.core.management import call_command
import json

def site(request):
    site_list = list(Site.objects.all())
    return render(request, "site.html", {'site_list': site_list})

def sponsor(request):
    ce_list = list(CE.objects.all())
    return render(request, "sponsor.html", {'ce_list': ce_list})

def get_site(request):
    geo_id = request.GET.get('geo_id')
    site = Site.objects.filter(geo_id=geo_id, most_current_record=True)[:1]
    site_to_return = serialize('json', site)
    geo = GEO.objects.filter(geo_id=geo_id)
    geo_to_return = serialize('json', geo)
    return JsonResponse({'site': site_to_return, 'geo': geo_to_return})

def get_sponsor(request):
    geo_id = request.GET.get('geo_id')
    sponsor = CE.objects.filter(geo_id=geo_id)[:1]
    sponsor_to_return = serialize('json', sponsor)
    geo = GEO.objects.filter(geo_id=geo_id)
    geo_to_return = serialize('json', geo)
    return JsonResponse({'sponsor': sponsor_to_return, 'geo': geo_to_return})

def get_geo(request):
    geo_id = request.GET.get('geo_id')
    geo = GEO.objects.filter(geo_id=geo_id)[:1]
    geo_to_return = serialize('json', geo)
    return JsonResponse({'geo': geo_to_return})

def site_data(request):
    sites = serialize('json', Site.objects.all())
    return HttpResponse(sites, content_type='json')

def site_details(request, siteid):
    site = get_object_or_404(Site, pk=siteid)
    return render(request, 'site_details.html', {'site': site})

def sponsor_details(request, ceid):
    sponsor = get_object_or_404(CE, pk=ceid)
    return render(request, 'sponsor_details.html', {'sponsor': sponsor})

def points(request):
    if request.method == 'GET':
        data_string = request.GET.get('json_data')
        data_dict = json.loads(data_string)
        min_lat = data_dict['min_lat']
        max_lat = data_dict['max_lat']
        min_long = data_dict['min_long']
        max_long = data_dict['max_long']
        entityType = data_dict['entityType']

        geo_list, geo_dict = get_geos(min_lat, max_lat, min_long, max_long, entityType)

        geos = serialize('json', geo_list)
        return JsonResponse({'result': 'success', 'geos': geos, 'entities': geo_dict})
    else:
        return JsonResponse({'result': 'unsuccessful'})


def get_geos(min_lat, max_lat, min_long, max_long, entityType):
    geo_list = GEO.objects.filter(valid_coordinates=True)
    geos_to_render = list()
    geo_dict = dict()
    for geo in geo_list:
        if geo.latitude != None and geo.longitude != None:
            if geo.latitude >= min_lat and geo.latitude <= max_lat \
                and geo.longitude >= min_long and geo.longitude <= max_long:
                if entityType == 'SITE':
                  site = Site.objects.values('pk', 'name', 'geo_id').filter(geo_id=geo.pk)
                  if site:
                    geos_to_render.append(geo)
                    geo_dict[str(geo.pk)] = json.dumps(list(site))
                elif entityType == 'SPONSOR':
                  ce = CE.objects.values('pk', 'name', 'geo_id').filter(geo_id=geo.pk)
                  if ce:
                    geos_to_render.append(geo)
                    geo_dict[str(geo.pk)] = json.dumps(list(ce))

    return (geos_to_render, geo_dict)
