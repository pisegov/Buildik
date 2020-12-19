from rest_framework import generics, status, permissions, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from setups.models import Setup, SetupItem
from setups.serializers import SetupSerializer, SetupItemSerializer
from setups.api import SetupsAPI

@api_view()
def api_check(request):
    return Response(SetupsAPI.get_filter_params(Setup.objects.all()[0]))

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
            return super(generics.ListCreateAPIView,self).create(request, *args, **kwargs)

class SetupDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SetupSerializer

    def get_queryset(self):
        return Setup.objects.filter(user=self.request.user)
    
    # def perform_update(self, serializer):
    #     serializer.save(user=self.request.user)


class SetupItemList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SetupItemSerializer

    def get_queryset(self):
        return SetupItem.objects.filter(setup__user=self.request.user).order_by('setup')

    
class SetupItemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SetupItemSerializer

    def get_queryset(self):
        return SetupItem.objects.filter(setup__user=self.request.user).order_by('setup')
    
    # def perform_update(self, serializer):
    #     serializer.save(user=self.request.user)
    