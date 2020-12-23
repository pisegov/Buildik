from typing import Dict, List, Tuple, Any, Type
import pccomponents.models as pcc


ITEMS_INFO: Dict[Type[pcc.Item], Tuple[bool]] = {
    # model: (isMany, )
    pcc.CPU: (False,),
    pcc.Motherboard: (False,),
    pcc.GPU: (False,),
    pcc.RAM: (True,),
    pcc.Storage: (True,),
    pcc.PowerSupplyUnit: (False,),
    pcc.CPUCooler: (False,),
    pcc.Case: (False,),
}

# filter fields configurator

MINIMUN_OF_RESTRICTIONS: List[str] = [
    'max_memory',
    'max_memory_clock',
    'memory_clock',
]
# MAXIMUM_OF_RESTRICTIONS = []

CUMULATIVE_RESTRICTIONS: Dict[str, str] = {
    'memory': 'total_memory',
    'memory_modules': 'total_memory_modules'
}

DIFFERENCE_RESTRICTIONS: Dict[str, Tuple[str, str]] = {
    'free_memory': ('max_memory', 'total_memory'),
    'free_memory_modules': ('memory_slots', 'total_memory_modules'),
}

DICT_DIFFERENCE_RESTRICTIONS: Dict[str, Tuple[str, str]] = {
    'free_interfaces': ('interfaces', 'required_interfaces'),
}