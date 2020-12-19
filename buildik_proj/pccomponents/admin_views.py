from rest_framework import generics, status, permissions
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import IntegrityError
from django.http import Http404
import pccomponents.models as pcc
import pccomponents.serializers as pccs

class ItemList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        try:
            model = pcc.item_class_by_category( self.kwargs.get('category') )
            return model.objects.all()
        except:
            return None

    def get_serializer_class(self):
        try:
            model = pcc.item_class_by_category( self.kwargs.get('category') )
            pccs.ItemSerializer.Meta.model = model
            pccs.ItemSerializer.Meta.fields = pccs._get_item_fields(model)
        except:
            pccs.ItemSerializer.Meta.model = pcc.Item
            pccs.ItemSerializer.Meta.fields = []
        return pccs.ItemSerializer
    

    # def list(self, request, *args, **kwargs):
    #     try:
    #         return super(generics.ListCreateAPIView,self).list(request, *args, **kwargs)
    #     except IntegrityError as err:
    #         return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    # def create(self, request, *args, **kwargs):
        # try:
        #     return super(generics.ListCreateAPIView,self).create(request, *args, **kwargs)
        # except Exception as err:
        #     return Response({'error':str(err)}, status=status.HTTP_400_BAD_REQUEST)

class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        try:
            model = pcc.item_class_by_category( self.kwargs.get('category') )
            return model.objects.all()
        except:
            return None

    def get_serializer_class(self):
        try:
            model = pcc.item_class_by_category( self.kwargs.get('category') )
            pccs.ItemSerializer.Meta.model = model
            pccs.ItemSerializer.Meta.fields = pccs._get_item_fields(model)
        except:
            pccs.ItemSerializer.Meta.model = pcc.Item
            pccs.ItemSerializer.Meta.fields = []
        return pccs.ItemSerializer


class SpecificationList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        try:
            model = pcc.SPECIFICATIONS[ self.kwargs.get('specification') ]
            return model.objects.all()
        except:
            return None

    def get_serializer_class(self):
        try:
            model = pcc.SPECIFICATIONS[ self.kwargs.get('specification') ]
            pccs.SpecificationSerializer.Meta.model = model
            pccs.SpecificationSerializer.Meta.fields = pccs._get_item_fields(model)
            return pccs.SpecificationSerializer
        except:
            pccs.ItemSerializer.Meta.model = pcc.Item
            pccs.ItemSerializer.Meta.fields = []
            return pccs.ItemSerializer

class SpecificationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        try:
            model = pcc.SPECIFICATIONS[ self.kwargs.get('specification') ]
            return model.objects.all()
        except:
            return None

    def get_serializer_class(self):
        try:
            model = pcc.SPECIFICATIONS[ self.kwargs.get('specification') ]
            pccs.SpecificationSerializer.Meta.model = model
            pccs.SpecificationSerializer.Meta.fields = pccs._get_item_fields(model)
            return pccs.SpecificationSerializer
        except:
            pccs.ItemSerializer.Meta.model = pcc.Item
            pccs.ItemSerializer.Meta.fields = []
            return pccs.ItemSerializer

class BelongingList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        try:
            model = pcc.BELONGINGS[ self.kwargs.get('belonging') ]
            return model.objects.all()
        except:
            return None

    def get_serializer_class(self):
        try:
            model = pcc.BELONGINGS[ self.kwargs.get('belonging') ]
            pccs.BelongingSerializer.Meta.model = model
            pccs.BelongingSerializer.Meta.fields = pccs._get_item_fields(model)
            return pccs.BelongingSerializer
        except:
            pccs.ItemSerializer.Meta.model = pcc.Item
            pccs.ItemSerializer.Meta.fields = []
            return pccs.ItemSerializer


class BelongingDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        try:
            model = pcc.BELONGINGS[ self.kwargs.get('belonging') ]
            return model.objects.all()
        except:
            return None

    def get_serializer_class(self):
        try:
            model = pcc.BELONGINGS[ self.kwargs.get('belonging') ]
            pccs.BelongingSerializer.Meta.model = model
            pccs.BelongingSerializer.Meta.fields = pccs._get_item_fields(model)
            return pccs.BelongingSerializer
        except:
            pccs.ItemSerializer.Meta.model = pcc.Item
            pccs.ItemSerializer.Meta.fields = []
            return pccs.ItemSerializer