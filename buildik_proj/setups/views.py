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
                {'detail': f'attempt to create setup for different user {request.data["user"]} by {request.user}'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        name = request.data['name']
        if Setup.objects.filter(user=request.user, name=name):
            return Response(
                {'detail':f'{request.user} user already has setup called {name}'}, 
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
    
    filters = SetupsAPI.get_filter_params(setup, exclude_item_id=exclude_item_id)
    filtered_queryset = PCComponentsAPI.get_queryset_filtered(category, filters, False)


    filtered_queryset = [filtered_item.id for filtered_item in filtered_queryset]

    if item.id in filtered_queryset:
        if model == pcc.RAM and 'memory_slots' in filters:
            return filters['memory_slots'] - filters['total_memory_modules'] >= number
        elif model == pcc.Storage and 'interfaces' in filters:
            interface = item.interface
            interfaces = filters['interfaces']
            required = 0
            if 'required_interfaces' in filters:
                if interface in filters['required_interfaces']:
                    required = filters['required_interfaces'][interface]
            return interfaces[interface] - required >= number
        elif setup_conf.ITEMS_INFO[model][0] == False:
            return number == 1 and filters[category+'_number'] == 0
        return True
    else:
        return False

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
                return Response({'error':str(err)}, status=status.HTTP_400_BAD_REQUEST)
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
                return Response({'error':str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error':str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
        if is_allowed:
            return super(generics.RetrieveUpdateDestroyAPIView, self).update(request, *args, **kwargs)
        return Response(
            {'detail': 'item does not suit current setup'},
            status=status.HTTP_400_BAD_REQUEST
        )
    