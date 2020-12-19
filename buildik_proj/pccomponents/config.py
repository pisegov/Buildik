from typing import Dict, List, Tuple, Type
import pccomponents.models as pcc

# Filter config

# SPECIFICATIONS are part of filter
EQUAL_RELATIONS = pcc.SPECIFICATIONS.keys()

# filter(model__field__in=[])
GREATER_OR_EQUAL_RELATIONS: Dict[str, str] = {
    'memory_slots': 'total_memory_modules',
    'max_memory': 'total_memory',
    
    'max_ram_clock': 'memory_clock',
    'max_gpu_length': 'gpu_length',
}
LESS_OR_EQUAL_RELATIONS: Dict[str, str] = {value: key for key, value in GREATER_OR_EQUAL_RELATIONS.items()}

BELONGING_TO_RELATIONS: Dict[str, str] = {
    'socket': 'sockets',
    'formfactor': 'formfactors',
}

NUMBERED_BELONGING_TO_RELATIONS: Dict[str, str] = {
    'interface': 'interfaces',
}

HAVING_ALL_RELATIONS: Dict[Type[pcc.Item], List[Tuple[Type[pcc.BelongingAbstract], str]]] = {
    pcc.CPUCooler: [(pcc.Socket, pcc.CPUCoolerSocket, 'required_sockets')],
    pcc.Case: [(pcc.FormFactor, pcc.CaseFormFactor, 'required_formfactors')],
}

NUMBERED_HAVING_ALL_RELATIONS: Dict[Type[pcc.Item], List[Tuple[Type[pcc.BelongingAbstract], str]]] = {
    pcc.Motherboard: [(pcc.Interface, pcc.MotherboardInterface, 'required_interfaces')],
}