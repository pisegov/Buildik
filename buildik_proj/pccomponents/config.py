from typing import Dict, List, Tuple, Type
import pccomponents.models as pcc

# regexs

CATEGORIES_REGEX = ''
for t in pcc.ITEMS:
    CATEGORIES_REGEX += t[1] + '|'
CATEGORIES_REGEX = CATEGORIES_REGEX[:-1]

SPECIFICATIONS_REGEX = ''
for s in pcc.SPECIFICATIONS:
    SPECIFICATIONS_REGEX += s + '|'
SPECIFICATIONS_REGEX = SPECIFICATIONS_REGEX[:-1]

BELONGINGS_REGEX = ''
for s in pcc.BELONGINGS:
    BELONGINGS_REGEX += s + '|'
BELONGINGS_REGEX = BELONGINGS_REGEX[:-1]

# Filter config

EQUAL_RELATIONS: Dict[str, Type[pcc.SpecificationAbstract]] = {
    'socket': pcc.Socket,
    'memorytype': pcc.MemoryType,
    'formfactor': pcc.FormFactor,
}


GREATER_OR_EQUAL_RELATIONS: Dict[str, str] = {
    'memory_slots': 'total_memory_modules',
    'max_memory': 'total_memory',
    'free_memory': 'memory',
    'free_memory_modules': 'memory_modules',
    
    'max_ram_clock': 'memory_clock',
    'max_gpu_length': 'gpu_length',
}
LESS_OR_EQUAL_RELATIONS: Dict[str, str] = {value: key for key, value in GREATER_OR_EQUAL_RELATIONS.items()}

BELONGING_TO_RELATIONS: Dict[str, str] = {
    'socket': 'sockets',
    'formfactor': 'formfactors',
}

NUMBERED_BELONGING_TO_RELATIONS: Dict[str, str] = {
    'interface': 'free_interfaces',
}

HAVING_ALL_RELATIONS: Dict[Type[pcc.Item], List[Tuple[Type[pcc.BelongingAbstract], str]]] = {
    pcc.CPUCooler: [(pcc.Socket, pcc.CPUCoolerSocket, 'required_sockets')],
    pcc.Case: [(pcc.FormFactor, pcc.CaseFormFactor, 'required_formfactors')],
}

NUMBERED_HAVING_ALL_RELATIONS: Dict[Type[pcc.Item], List[Tuple[Type[pcc.BelongingAbstract], str]]] = {
    pcc.Motherboard: [(pcc.Interface, pcc.MotherboardInterface, 'required_interfaces')],
}

OTHER_RELATIONS: List[str] = [
    'interfaces',
]