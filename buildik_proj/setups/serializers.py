from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from setups.models import Setup, SetupItem
from setups.config import ITEMS_INFO
import pccomponents.models as pcc

class SetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setup
        exclude = ['user',]

    def to_representation(self, instance):
        setup = {
            'id': instance.id,
            'name': instance.name,
            'parts': [
                {'relation': setup_item.id, 'item': setup_item.item.id, 'model': str(setup_item.item), 'number': setup_item.number, 'price': setup_item.item.price} 
                if ITEMS_INFO[pcc.item_class_by_number(setup_item.item.category)][0] else
                {'relation': setup_item.id, 'item': setup_item.item.id, 'model': str(setup_item.item), 'price': setup_item.item.price}
                for setup_item in SetupItem.objects.filter(setup=instance)
            ],
            'total_price': 0
        }
        for item in setup['parts']:
            if 'number' in item:
                setup['total_price'] += item['price'] * item['number']
            else:
                setup['total_price'] += item['price']
        
        for item in setup['parts']:
            item['price'] = str(item['price']) + pcc.Item.currency
        setup['total_price'] = str(setup['total_price']) + pcc.Item.currency
        
        return setup

class SetupByUserField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = Setup.objects.filter(user=user)
        return queryset

class SetupItemSerializer(serializers.ModelSerializer):
    setup = SetupByUserField()

    def to_representation(self, instance):
        setup_item = {
            'name': str(instance.setup) + " : " + str(instance.item),
            'id': instance.id, 'setup': instance.setup.id, 'item': instance.item.id
        }
        if ITEMS_INFO[pcc.item_class_by_number(instance.item.category)][0]:
            setup_item['number'] = instance.number

        return setup_item
    
    class Meta:
        model = SetupItem
        fields = ['id', 'setup', 'item', 'number']