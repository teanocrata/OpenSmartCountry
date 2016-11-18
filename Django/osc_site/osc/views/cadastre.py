from django.http import JsonResponse
from osc.services import get_parcels_by_bbox, get_parcels_by_cadastral_code
from osc.services.climate import get_closest_station, get_aggregated_climate_measures
from osc.services.soil import get_closest_soil_measure

from osc.exceptions import OSCException


def is_valid_parcel(parcel):
    try:
        public_info = parcel['properties']['cadastralData']

        is_valid = not len(public_info['bico']['lspr']['spr'])
        for spr in public_info['bico']['lspr']['spr']:
            is_valid = is_valid or (spr['dspr']['ccc'] not in ['VT', 'OT', 'FF'])
    except KeyError:
        # As it does not have information about the type, we assume that it is OK
        is_valid = True

    return is_valid


def obtain_cadastral_parcels(request):
    try:
        bbox_param = request.GET.get('bbox', None)
        cadastral_code_param = request.GET.get('cadastral_code', None)
        retrieve_public_info_param = request.GET.get('retrieve_public_info', None)
        retrieve_climate_info_param = request.GET.get('retrieve_climate_info', None)
        retrieve_soil_info_param = request.GET.get('retrieve_soil_info', None)

        parcels = []

        if cadastral_code_param is not None:
            parcels = get_parcels_by_cadastral_code(cadastral_code_param, retrieve_public_info_param)

            # Add climate info
            if retrieve_climate_info_param == 'True':
                for parcel in parcels:
                    closest_station = \
                        get_closest_station(parcel['properties']['reference_point']['lat'],
                                            parcel['properties']['reference_point']['lon'])
                    parcel['properties']['closest_station'] = closest_station
                    climate_agg = get_aggregated_climate_measures(closest_station['IDESTACION'],
                                                                  closest_station['IDPROVINCIA'],
                                                                  3)
                    parcel['properties']['climate_aggregations'] = climate_agg
            
            # Add soil info
            if retrieve_soil_info_param == 'True':
                for parcel in parcels:
                    closest_soil_measure = \
                        get_closest_soil_measure(parcel['properties']['reference_point']['lat'],
                                            parcel['properties']['reference_point']['lon'])
                    parcel['properties']['closest_soil_measure'] = closest_soil_measure         
            

        elif bbox_param is not None:
            lat_min, lon_min, lat_max, lon_max = map(lambda x: float(x), bbox_param.split(','))

            parcels = get_parcels_by_bbox(lat_min, lon_min, lat_max, lon_max)

            # Filter the parcels that are roads, ways, etc.
            # (JLG ATTENTION: To be removed when we have everything in ELASTIC)
            parcels = filter(is_valid_parcel, parcels)

        # Convert into geojson
        for parcel in parcels:
            parcel['type'] = 'Feature'

        parcels_geojson = {'type': 'FeatureCollection',
                           'features': parcels}

        return JsonResponse(parcels_geojson)
    except OSCException as e:
        return JsonResponse({'error': str(type(e)) + ': ' + e.message})


