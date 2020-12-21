import json
from rest_framework import status, permissions
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.decorators import api_view
from pccomponents.api import PCComponentsAPI
from setups.api import SetupsAPI
from setups.models import Setup


@api_view()
def get_all_pccomponents(request):
    return Response(PCComponentsAPI.get_all_items())

@api_view()
def get_pccomponent(request, pk: int):
    try:
        return Response(PCComponentsAPI.get_item(pk))
    except ValueError as err:
        return Response({'detail':str(err)}, status=status.HTTP_404_NOT_FOUND)

@api_view()
def get_category(request, category: str):
    if 'filter-json' in request.GET:
        try:
            filters = PCComponentsAPI.filter_translate_from_query(
                json.loads(request.GET.get('filter-json'))
            )       
            return Response(PCComponentsAPI.get_items_filtered(category, filters))

        except ValueError as err:
            try:
                return Response({'error':json.loads(str(err))}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'error':str(err)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(PCComponentsAPI.get_items(category))

@api_view()
def get_category_for_setup(request, category: str, pk: int):
    try:
        setup = Setup.objects.get(id=pk, user=request.user)
    except:
        return Response(
            {'detail': 'setup does not exist or belongs to different user'}, 
            status=status.HTTP_403_FORBIDDEN
        )

    filters = SetupsAPI.get_filter_params(setup)
    return Response(PCComponentsAPI.get_items_filtered(category, filters, False))
        

@api_view()
def get_specification(request, specification: str):
    return Response(PCComponentsAPI.get_specifications(specification))

@api_view()
def get_belonging(request, belonging: str):
    return Response(PCComponentsAPI.get_belongings(belonging))
