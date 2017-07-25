from django.http import HttpResponse
import json
from osc.services.parcels import obtain_parcels_by_cadastral_code


def parcel_detail(request, cadastralCode=""):
    parcels = obtain_parcels_by_cadastral_code(cadastralCode)
    return HttpResponse(json.dumps(parcels), content_type='application/json')


def parcel_list(request):
    return HttpResponse({'bla': 'ble'}, content_type='application/json')
