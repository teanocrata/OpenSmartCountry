import logging

from osc.services import cadastre
from osc.services import climate
from osc.services import soil

logger = logging.getLogger(__name__)


def is_valid_parcel(parcel):
    try:
        public_info = parcel['properties']['cadastralData']

        is_valid = not len(public_info['bico']['lspr']['spr'])
        for spr in public_info['bico']['lspr']['spr']:
            is_valid = is_valid or \
                (spr['dspr']['ccc'] not in ['VT', 'OT', 'FF'])
    except KeyError:
        # As it does not have information about the type,
        # we assume that it is OK
        is_valid = True

    return is_valid


def update_parcel_by_cadastral_code(cadastral_code):
    logger.info('update_parcel_by_cadastral_code(%s)', cadastral_code)
    parcels_geojson = obtain_parcels_by_cadastral_code(
        cadastral_code,
        retrieve_public_info=True,
        retrieve_climate_info=False,
        retrieve_soil_info=True,
        retrieve_google_info=False)
    logger.debug('parcels_geojson[\'features\'][0] = %s',
                 parcels_geojson['features'][0])
    json2source(parcels_geojson['features'][0])
    cadastre.index_parcel(json2source(parcels_geojson['features'][0]))


def json2source(json):
    source = {}
    source['geometry'] = json['geometry']
    source['properties'] = json['properties']
    source['bbox'] = json['bbox']
    return source


def obtain_parcels_by_cadastral_code(cadastral_code,
                                     retrieve_public_info=False,
                                     retrieve_climate_info=False,
                                     retrieve_soil_info=False,
                                     retrieve_google_info=False):
    logger.debug('obtain_parcels_by_cadastral_code(%s,%s,%s,%s)',
                 cadastral_code,
                 retrieve_public_info,
                 retrieve_climate_info,
                 retrieve_soil_info)
    parcels = cadastre.get_parcels_by_cadastral_code(cadastral_code,
                                                     retrieve_public_info,
                                                     retrieve_google_info)

    # Add climate info
    if retrieve_climate_info:
        for parcel in parcels:
            closest_station = \
                climate.get_closest_station(
                    parcel['properties']['reference_point']['lat'],
                    parcel['properties']['reference_point']['lon'])
            parcel['properties']['closest_station'] = closest_station
            climate_agg = climate.get_aggregated_climate_measures(
                closest_station['IDESTACION'],
                closest_station['IDPROVINCIA'],
                3)
            parcel['properties']['climate_aggregations'] = climate_agg

    # Add soil info
    if retrieve_soil_info:
        for parcel in parcels:
            closest_soil_measure = \
                soil.get_closest_soil_measure(
                    parcel['properties']['reference_point']['lat'],
                    parcel['properties']['reference_point']['lon'])
            parcel['properties']['closest_soil_measure'] = closest_soil_measure

    parcels_geojson = {'type': 'FeatureCollection',
                       'features': parcels}

    return parcels_geojson


def obtain_parcels_by_bbox(lat_min, lon_min, lat_max, lon_max, precision):

    if precision == 0:
        parcels = cadastre.get_parcels_by_bbox(
            lat_min, lon_min, lat_max, lon_max)

        # Filter the parcels that are roads, ways, etc.
        # (JLG ATTENTION: To be removed when we have everything in ELASTIC)
        # parcels = filter(is_valid_parcel, parcels)
        return parcels
    else:
        parcels_bucket = cadastre.get_bucket_of_parcels_by_bbox_and_precision(
            lat_min, lon_min, lat_max, lon_max, precision)

        return parcels_bucket


def scan_parcels(update):
    cadastre.scan_parcels(update)
