from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime

from zones.api.serializers import ZoneSerializer
from zones.models import Zone
from zones.models import Distribution

@api_view(['POST'])
def edit(request):
    '''
        Edita el nombre de Zone y sus distributions
    '''
    zone_id = request.data.get('id')
    name = request.data.get('name')
    distributions = request.data.get('distributions')
    error = None
    try:
        zone = Zone.objects.filter(pk=zone_id).first()
        if not zone:
            return Response('', status=status.HTTP_400_BAD_REQUEST)

        if zone.name != name:
            zone.updated_at = datetime.now()
        zone.name = name

        # Recorre la lista de distributions si el id es 0 lo agrega si no lo edita
        for ds in distributions:
            if ds['id'] == 0:
                distribution = Distribution.objects.create(percentage = ds['percentage'],zone_id= zone_id)
            else:
                distribution = Distribution.objects.filter(pk=ds['id']).first()
                distribution.percentage = ds['percentage']
            distribution.save()

        zone.save()
    except Exception as err:
        error = f"Unexpected {err=}, {type(err)=}"
    response = {}
    response['success'] = True if error is None else False
    response['message'] = "Ok" if error is None else error
    response['zone'] =ZoneSerializer(zone, many=False).data
    response['status'] = status.HTTP_201_CREATED
    return Response(response)

@api_view(['POST'])
def remove_distribution(request):
    '''
        Elimina un distribution por su id de la tabla
    '''
    id_dist = request.data.get('id')
    error = None
    try:
        Distribution.objects.filter(pk= id_dist).delete()
    except Exception as err:
        error = f"Unexpected {err=}, {type(err)=}"
    response = {}
    response['success'] = True if error is None else False
    response['message'] = "Ok" if error is None else error
    response['status'] = status.HTTP_201_CREATED
    return Response(response)
