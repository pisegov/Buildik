from typing import Dict, Tuple, Any, Type
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

MINIMUN_OF_RESTRICTIONS = [
    'max_memory',
    'memory_clock',
]
# MAXIMUM_OF_RESTRICTIONS = []

CUMULATIVE_RESTRICTIONS = {
    'memory': 'total_memory',
}