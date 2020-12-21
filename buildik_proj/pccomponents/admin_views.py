from rest_framework import generics, status, permissions
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import IntegrityError
from django.http import Http404
import pccomponents.models as pcc
import pccomponents.serializers as pccs

def prepare_item_model(obj):
    return pcc.item_class_by_category(obj.kwargs.get('category'))

def prepare_spec_model(obj):
    return pcc.SPECIFICATIONS[obj.kwargs.get('specification')]

def prepare_belonging_model(obj):
    return pcc.BELONGINGS[obj.kwargs.get('belonging')]

def prepare_queryset(model):
    try:
        return model.objects.all()
    except:
        return None

def prepare_serializer(model, serializer):
    try:
        serializer.Meta.model = model
        serializer.Meta.fields = pccs._get_item_fields(model)
        return serializer
    except:
        pccs.ItemSerializer.Meta.model = pcc.Item
        pccs.ItemSerializer.Meta.fields = []
        return pccs.ItemSerializer


class ItemList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return prepare_queryset(prepare_item_model(self))

    def get_serializer_class(self):
        return prepare_serializer(prepare_item_model(self), pccs.ItemSerializer)
    
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
        return prepare_queryset(prepare_item_model(self))

    def get_serializer_class(self):
        return prepare_serializer(prepare_item_model(self), pccs.ItemSerializer)


class SpecificationList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return prepare_queryset(prepare_spec_model(self))

    def get_serializer_class(self):
        return prepare_serializer(prepare_spec_model(self), pccs.SpecificationSerializer)

class SpecificationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return prepare_queryset(prepare_spec_model(self))

    def get_serializer_class(self):
        return prepare_serializer(prepare_spec_model(self), pccs.SpecificationSerializer)


class BelongingList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return prepare_queryset(prepare_belonging_model(self))

    def get_serializer_class(self):
        return prepare_serializer(prepare_belonging_model(self), pccs.BelongingSerializer)

class BelongingDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return prepare_queryset(prepare_belonging_model(self))

    def get_serializer_class(self):
        return prepare_serializer(prepare_belonging_model(self), pccs.BelongingSerializer)
