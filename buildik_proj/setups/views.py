import json
from rest_framework import generics, status, permissions, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from setups.models import Setup, SetupItem
from setups.serializers import SetupSerializer, SetupItemSerializer
from setups.api import SetupsAPI
import setups.config as setup_conf
import pccomponents.models as pcc
from pccomponents.api import PCComponentsAPI


class SetupList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SetupSerializer

    def get_queryset(self):
        return Setup.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        if 'user' in request.data and request.data['user'] != request.user:
            return Response(
                {'detail': 'attempt to create setup for different user'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        name = request.data['name']
        if Setup.objects.filter(user=request.user, name=name):
            return Response(
                {'detail':f'user already has setup called {name}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return super(generics.ListCreateAPIView, self).create(request, *args, **kwargs)

class SetupDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SetupSerializer

    def get_queryset(self):
        return Setup.objects.filter(user=self.request.user)
    

def is_item_allowed_for_setup(request, exclude_item_id: int = None):
    item = pcc.Item.objects.get(id=request.data['item'])
    number = request.data['number']
    number = 1 if number is None or number == '' else int(number)

    model = pcc.item_class_by_number(item.category)
    category = pcc.item_category_by_number(item.category)
    item = model.objects.get(id=item.id)
    
    if number < 1:
        raise ValueError(json.dumps({'detail': 'number must be a positive number'}))
    try:
        setup = Setup.objects.get(id=request.data['setup'], user=request.user)
    except:
        raise ValueError(json.dumps({'detail': 'setup does not exist or belongs to different user'}))
    

    filters = SetupsAPI.get_filter_params_by_setup(setup, exclude_item_id=exclude_item_id)
    filtered_queryset = PCComponentsAPI.get_queryset_filtered(category, filters, error_check=False)


    if not filtered_queryset.filter(id=item.id).exists():
        return False

    if model == pcc.RAM and 'free_memory' in filters:
        if 'free_memory_modules' in filters:
            max_number = min(
                filters['free_memory'] // item.memory,
                filters['free_memory_modules'] // item.memory_modules,
            )
        else:
            max_number = filters['free_memory'] // item.memory
    elif model == pcc.Storage and 'free_interfaces' in filters:
        max_number = filters['free_interfaces'][item.interface]
    elif setup_conf.ITEMS_INFO[model][0] == False:
        max_number = 1
    else:
        max_number = None
    
    return max_number is None or number <= max_number


class SetupItemList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SetupItemSerializer

    def get_queryset(self):
        return SetupItem.objects.filter(setup__user=self.request.user).order_by('setup')

    def create(self, request, *args, **kwargs):
        try:
            is_allowed = is_item_allowed_for_setup(request)
        except ValueError as err:
            try:
                return Response(json.loads(str(err)), status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'detail':str(err)}, status=status.HTTP_400_BAD_REQUEST)
        # except Exception as err:
        #     return Response({'error':str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
        if is_allowed:
            return super(generics.ListCreateAPIView, self).create(request, *args, **kwargs)
        return Response(
            {'detail': 'item does not suit current setup'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
class SetupItemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SetupItemSerializer

    def get_queryset(self):
        return SetupItem.objects.filter(setup__user=self.request.user).order_by('setup')
    
    def update(self, request, *args, **kwargs):
        try:
            item = SetupItem.objects.get(id=self.kwargs.get('pk')).item
            is_allowed = is_item_allowed_for_setup(request, item.id)
        except ValueError as err:
            try:
                return Response(json.loads(str(err)), status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'detail':str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error':str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
        if is_allowed:
            return super(generics.RetrieveUpdateDestroyAPIView, self).update(request, *args, **kwargs)
        return Response(
            {'detail': 'item does not suit current setup'},
            status=status.HTTP_400_BAD_REQUEST
        )
    