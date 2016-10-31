import ast
from osc.services import retrieve_crops_from_elastic
from django.http import JsonResponse


def obtain_crops_elastic_query(request):
    query = ast.literal_eval(request.body)

    try:
        crops = retrieve_crops_from_elastic(query)
        return JsonResponse({'status': 'SUCCESS',
                             'result': crops})
    except Exception as e:
        return JsonResponse({'status': 'FAILURE',
                             'message': e.message})
