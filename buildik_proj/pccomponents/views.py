import json
from typing import Optional
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from pccomponents.api import PCComponentsAPI
from setups.api import SetupsAPI
from setups.models import Setup


@api_view()
def get_all_pccomponents(request):
    search_name = request.GET.get('name')
    return Response(PCComponentsAPI.get_all_items(search_name))

@api_view()
def get_pccomponent(request, pk: int):
    try:
        return Response(PCComponentsAPI.get_item(pk))
    except ValueError as err:
        return Response({'detail':str(err)}, status=status.HTTP_404_NOT_FOUND)

@api_view()
def get_category(request, category: str):
    search_name = request.GET.get('name')
    if 'filter-json' in request.GET:
        try:
            filters = PCComponentsAPI.filter_translate_from_query(
                json.loads(request.GET.get('filter-json'))
            )       
            return Response(PCComponentsAPI.get_items_filtered(category, filters, search_name))

        except ValueError as err:
            try:
                return Response({'detail':json.loads(str(err))}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'detail':str(err)}, status=status.HTTP_400_BAD_REQUEST)
    elif 'filter-items' in request.GET:
        filters = SetupsAPI.get_filter_params_by_items(
            json.loads(request.GET.get('filter-items'))
        )
        return Response(PCComponentsAPI.get_items_filtered(category, filters, search_name, error_check=False))
    else:
        return Response(PCComponentsAPI.get_items(category, search_name))

@api_view()
@permission_classes([permissions.IsAuthenticated])
def get_category_for_setup(request, category: str, pk: int, exclude_item_pk: Optional[int] = None):
    search_name = request.GET.get('name')
    try:
        setup = Setup.objects.get(id=pk, user=request.user)
    except:
        return Response(
            {'detail': 'setup does not exist or belongs to different user'}, 
            status=status.HTTP_403_FORBIDDEN
        )

    if exclude_item_pk is not None:
        exclude_item_pk = int(exclude_item_pk)
    filters = SetupsAPI.get_filter_params_by_setup(setup, exclude_item_pk)

    return Response(PCComponentsAPI.get_items_filtered(category, filters, search_name, error_check=False))


@api_view()
def get_specification(request, specification: str):
    return Response(PCComponentsAPI.get_specifications(specification))

@api_view()
def get_belonging(request, belonging: str):
    return Response(PCComponentsAPI.get_belongings(belonging))
