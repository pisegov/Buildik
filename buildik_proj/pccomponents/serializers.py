from rest_framework import serializers
import pccomponents.models as pcc
from typing import List

def _get_item_fields(model) -> List[str]:
    fields = [field.name for field in model._meta.fields]
    if 'item_ptr' in fields:
        fields.remove('item_ptr')
    if 'category' in fields:
        fields.remove('category')
    return fields

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = None

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = None

class BelongingSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = None
