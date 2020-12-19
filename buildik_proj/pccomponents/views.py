from rest_framework import status, permissions
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.decorators import api_view
from pccomponents.api import PCComponentsAPI


@api_view()
def get_all_pccomponents(request):
    return Response(PCComponentsAPI.get_all_items())

@api_view()
def get_pccomponent(request, pk: int):
    try:
        return Response(PCComponentsAPI.get_item(pk))
    except ValueError as err:
        return Response({'error':str(err)}, status=status.HTTP_404_NOT_FOUND)

@api_view()
def get_category(request, category: str):
    import json
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
def get_specification(request, specification: str):
    return Response(PCComponentsAPI.get_specifications(specification))

@api_view()
def get_belonging(request, belonging: str):
    return Response(PCComponentsAPI.get_belongings(belonging))
