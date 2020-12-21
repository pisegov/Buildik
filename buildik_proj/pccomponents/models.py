import json
from typing import Dict, List, Tuple, Any, Type, Optional
from django.db import models


ITEM_CATEGORY_CHOICES: Tuple[int, str] = (
    (1, 'CPU'),
    (2, 'Motherboard'),
    (3, 'GPU'),
    (4, 'RAM'),
    (5, 'Storage'),
    (6, 'Power supply unit'),
    (7, 'CPU Cooler'),
    (8, 'Case'),
)

class Item(models.Model):
    manufacturer = models.CharField(max_length=30, default=None)
    model = models.CharField(max_length=30, default=None)
    category = models.IntegerField(choices=ITEM_CATEGORY_CHOICES, default=None)
    price = models.FloatField()
    # image_url = models.URLField(max_length=200)

    currency = '$'

    class Meta:
        unique_together = ("manufacturer", "model")

    def save(self, *args, **kwargs) -> None:
        raise ValueError('Item cannot be created without category')

    def __str__(self) -> str:
        return self.get_category_display() + " " + self.manufacturer + " " + self.model

class ItemAbstract(Item):
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs) -> None:
        model = type(self)
        if self.category is None or self.category == item_number_by_class(model):
            self.category = item_number_by_class(model)
            models.Model.save(self, *args, **kwargs)
        else:
            raise ValueError(f'Attempt to create {item_category_by_class(model)} '\
                            f'with category {item_category_by_number(self.category)}')
    
    def get_item_fields(self) -> Dict[str, Any]:
        fields = {field.name: getattr(self, field.name) for field in type(self)._meta.fields}
        fields.pop('item_ptr')
        return fields
    
    def get_full_item(self) -> Dict[str, Any]:
        model = type(self)
        fields = {field.name: getattr(self, field.name) for field in model._meta.fields}
        fields.pop('item_ptr')

        if model in REFERENCES:
            for t in REFERENCES[model]:
                queryset = t[1].objects.filter(**{model._meta.model_name: self})
                if t[2] is None:
                    fields[t[3]] = [
                        getattr(item, t[0]._meta.model_name) for item in queryset
                    ]
                else:
                    fields[t[3]] = {
                        getattr(item, t[0]._meta.model_name): getattr(item, t[2]) for item in queryset
                    }
        return fields
    
    def to_json(self) -> Dict[str, Any]:
        model = type(self)
        jsoned_item = self.get_item_fields()
        jsoned_item['category'] = self.get_category_display()
        jsoned_item['price'] = str(jsoned_item['price']) + Item.currency

        for key in jsoned_item:
            if key in SPECIFICATIONS:
                jsoned_item[key] = getattr(jsoned_item[key], key+'_name')

        if model in REFERENCES:
            for t in REFERENCES[model]:
                queryset = t[1].objects.filter(**{model._meta.model_name: self})
                if t[2] is None:
                    jsoned_item[t[3]] = [
                        str(getattr(item, t[0]._meta.model_name)) for item in queryset
                    ]
                else:
                    jsoned_item[t[3]] = {
                        str(getattr(item, t[0]._meta.model_name)): getattr(item, t[2]) for item in queryset
                    }

        for key in model.measure_units:
            if jsoned_item[key] is not None:
                jsoned_item[key] = str(jsoned_item[key]) + ' ' + model.measure_units[key]

        return jsoned_item

class SpecificationAbstract(models.Model):
    class Meta:
        abstract = True
    def save(self, *args, **kwargs) -> None:
        if self.id is None:
            models.Model.save(self, *args, **kwargs)
        else:
            raise Exception(f'{type(self).__name__} updating is prohibited')
    def get_item_fields(self) -> Dict[str, Any]:
        fields = {field.name: getattr(self, field.name) for field in type(self)._meta.fields}
        return fields
    def __str__(self) -> str:
        name = ''
        fields = self.get_item_fields()
        for key in fields:
            if key != 'id':
                name += str(fields[key]) + ' '
        return name[:-1]

class BelongingAbstract(models.Model):
    class Meta:
        abstract = True

    def get_item_fields(self) -> Dict[str, Any]:
        fields = {field.name: getattr(self, field.name) for field in type(self)._meta.fields}
        return fields
    def __str__(self) -> str:
        name = ''
        fields = self.get_item_fields()
        for key in fields:
            if key != 'id':
                name += str(fields[key]) + ' : '
        return name[:-3]
            

class Socket(SpecificationAbstract):
    socket_name = models.CharField(max_length=30, unique=True, default=None)

class MemoryType(SpecificationAbstract):
    memorytype_name = models.CharField(max_length=30, unique=True, default=None)

class FormFactor(SpecificationAbstract):
    formfactor_name = models.CharField(max_length=30, unique=True, default=None)

class Interface(SpecificationAbstract):
    interface_name = models.CharField(max_length=30, unique=True, default=None)


class CPU(ItemAbstract):
    socket = models.ForeignKey(Socket, on_delete=models.PROTECT)
    core_clock = models.FloatField()
    cores = models.IntegerField()
    L3_cache = models.IntegerField()
    max_memory_clock = models.IntegerField()
    max_memory = models.IntegerField()
    TDP = models.IntegerField(null=True)
    process = models.IntegerField(null=True)
    integrated_graphics = models.CharField(max_length=30, default=None, null=True)

    measure_units: Dict[str, str] = {
        'core_clock': 'GHz',
        'L3_cache': 'MB',
        'TDP': 'W',
        'process': 'nm',
        'max_memory_clock': 'MHz',
        'max_memory': 'GB',
    }    


class Motherboard(ItemAbstract):
    socket = models.ForeignKey(Socket, on_delete=models.PROTECT)
    formfactor = models.ForeignKey(FormFactor, on_delete=models.PROTECT)
    memorytype = models.ForeignKey(MemoryType, on_delete=models.PROTECT)
    max_memory = models.IntegerField()
    memory_slots = models.IntegerField()
    max_memory_clock = models.IntegerField()

    measure_units: Dict[str, str] = {
        'max_memory': 'GB',
        'max_memory_clock': 'MHz',
    }


class GPU(ItemAbstract):
    video_memory = models.IntegerField()
    core_clock = models.IntegerField()
    TDP = models.IntegerField(null=True)
    gpu_length = models.IntegerField()

    measure_units: Dict[str, str] = {
        'video_memory': 'GB',
        'core_clock': 'MHz',
        'gpu_length': 'mm',
        'TDP': 'W',
    }


class RAM(ItemAbstract):
    memory = models.IntegerField()
    memorytype = models.ForeignKey(MemoryType, on_delete=models.PROTECT)
    memory_clock = models.IntegerField()

    measure_units: Dict[str, str] = {
        'memory': 'GB',
        'memory_clock': 'MHz',
    }


class Storage(ItemAbstract):
    interface = models.ForeignKey(Interface, on_delete=models.PROTECT)
    capacity = models.IntegerField()
    cache = models.IntegerField()


    measure_units: Dict[str, str] = {
        'capacity': 'GB',
        'cache': 'MB',
    }


class PowerSupplyUnit(ItemAbstract):
    formfactor = models.ForeignKey(FormFactor, on_delete=models.PROTECT)
    wattage = models.IntegerField()
    efficiency_rating = models.CharField(max_length=30, default=None, null=True)

    measure_units: Dict[str, str] = {
        'wattage': 'W',
    }


class CPUCooler(ItemAbstract):
    # radiator_size = models.IntegerField()
    min_fan_rpm = models.IntegerField()
    max_fan_rpm = models.IntegerField()

    measure_units: Dict[str, str] = {
        # 'radiator_size': 'mm',
        'min_fan_rpm': 'rpm',
        'max_fan_rpm': 'rpm',
    }

class Case(ItemAbstract):
    case_type = models.CharField(max_length=30, default=None)
    max_gpu_length = models.IntegerField()

    measure_units: Dict[str, str] = {
        'max_gpu_length': 'mm',
    }

class CPUCoolerSocket(BelongingAbstract):
    cpucooler = models.ForeignKey(CPUCooler, on_delete=models.CASCADE)
    socket = models.ForeignKey(Socket, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("cpucooler", "socket")

class MotherboardInterface(BelongingAbstract):
    motherboard = models.ForeignKey(Motherboard, on_delete=models.CASCADE)
    interface = models.ForeignKey(Interface, on_delete=models.PROTECT)
    number = models.IntegerField()

    class Meta:
        unique_together = ("motherboard", "interface")

class CaseFormFactor(BelongingAbstract):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    formfactor = models.ForeignKey(FormFactor, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("case", "formfactor")



ITEMS: List[Tuple[int, str, Type[Item]]] = [
    (1, 'cpu', CPU),
    (2, 'motherboard', Motherboard),
    (3, 'gpu', GPU),
    (4, 'ram', RAM),
    (5, 'storage', Storage),
    (6, 'power_supply_unit', PowerSupplyUnit),
    (7, 'cpu_cooler', CPUCooler),
    (8, 'case', Case),
]

SPECIFICATIONS: Dict[str, Type[SpecificationAbstract]] = {
    'socket': Socket,
    'memorytype': MemoryType,
    'formfactor': FormFactor,
    'interface': Interface,
}

BELONGINGS: Dict[str, Type[BelongingAbstract]] = {
    'cpu_cooler_socket': CPUCoolerSocket,
    'motherboard_interface': MotherboardInterface,
    'case_formfactor': CaseFormFactor,
}

REFERENCES: Dict[Type[Item], List[Tuple[Type[Item], Type[BelongingAbstract], Optional[str], str]]] = {
    CPUCooler: [(Socket, CPUCoolerSocket, None, 'sockets')],
    Motherboard: [(Interface, MotherboardInterface, 'number', 'interfaces')],
    Case: [(FormFactor, CaseFormFactor, None, 'formfactors')],
}


def item_category_by_number(number: int) -> str:
    for t in ITEMS:
        if t[0] == number:
            return t[1]
    raise ValueError(f'No category with number {number}')

def item_category_by_class(model) -> str:
    for t in ITEMS:
        if t[2] == model:
            return t[1]
    raise ValueError(f'No category with class {model}')

def item_number_by_class(model) -> int:
    for t in ITEMS:
        if t[2] == model:
            return t[0]
    raise ValueError(f'No category with class {model}')

def item_class_by_category(category: str):
    for t in ITEMS:
        if t[1] == category:
            return t[2]
    raise ValueError(f'No class with category {category}')

def item_class_by_number(number: int):
    for t in ITEMS:
        if t[0] == number:
            return t[2]
    raise ValueError(f'No class with number {number}')
