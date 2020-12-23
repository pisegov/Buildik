from typing import Any, Dict, List, Tuple, Optional
from setups.models import Setup, SetupItem
import setups.config as setup_conf
import pccomponents.models as pcc
import pccomponents.config as conf


class SetupsAPI:
    def get_filter_params_by_items(items: List[Tuple[int, int]], exclude_item_id: Optional[int]=None) -> Dict[str, Any]:
        filters = {
            category[1]+'_number': 0
            for category in pcc.ITEMS
        }

        for titem in items:
            item_id = titem[0]
            item_number = titem[1]

            if item_id == exclude_item_id:
                continue
            
            model = pcc.item_class_by_number(pcc.Item.objects.get(id=item_id).category)
            model_item = model.objects.get(id=item_id)
            item = {
                **model_item.get_full_item(),
                'number': item_number,
            }

            filters[pcc.item_category_by_number(item['category'])+'_number'] += item['number']

            for field in item:
                if field in setup_conf.MINIMUN_OF_RESTRICTIONS:
                    if field in filters:
                        filters[field] = min(filters[field], item[field])
                    else:
                        filters[field] = item[field]
                elif field in setup_conf.CUMULATIVE_RESTRICTIONS:
                    value = setup_conf.CUMULATIVE_RESTRICTIONS[field]
                    if field in filters:
                        filters[value] += item[field] * item['number']
                    else:
                        filters[value] = item[field] * item['number']

                elif field in conf.EQUAL_RELATIONS or\
                     field in conf.GREATER_OR_EQUAL_RELATIONS or\
                     field in conf.LESS_OR_EQUAL_RELATIONS or\
                     field in list(conf.BELONGING_TO_RELATIONS.values()) or\
                     field in list(conf.NUMBERED_BELONGING_TO_RELATIONS.values()) or\
                     field in conf.OTHER_RELATIONS:
                    filters[field] = item[field]

            for kmodel, l in conf.HAVING_ALL_RELATIONS.items():
                for t in l:
                    spec = t[0]._meta.model_name
                    if spec in item:
                        if t[2] in filters:
                            if item[spec] not in filters[t[2]]:
                                filters[t[2]] += [item[spec]]
                        else:
                            filters[t[2]] = [item[spec]]

            for l in list(conf.NUMBERED_HAVING_ALL_RELATIONS.values()):
                for t in l:
                    spec = t[0]._meta.model_name
                    if spec in item:
                        if t[2] in filters:
                            if item[spec] not in filters[t[2]]:
                                filters[t[2]].update({item[spec]: item['number']})
                            else:
                                filters[t[2]][item[spec]] += item['number']
                        else:
                            filters[t[2]] = {item[spec]: item['number']}

        for kfield, tfields in setup_conf.DIFFERENCE_RESTRICTIONS.items():
            if tfields[0] in filters:
                filters[kfield] = filters[tfields[0]]
                if tfields[1] in filters:
                    filters[kfield] -= filters[tfields[1]]
                    

        for kfield, tfields in setup_conf.DICT_DIFFERENCE_RESTRICTIONS.items():
            if tfields[0] in filters:
                filters[kfield] = filters[tfields[0]].copy()
                if tfields[1] in filters:
                    for field in filters[tfields[1]]:
                        filters[kfield][field] -= filters[tfields[1]][field]
                filters[kfield] = {key: value for key, value in filters[kfield].items() if value > 0}

        return filters

    def get_filter_params_by_setup(setup: Setup, exclude_item_id: Optional[int] = None) -> Dict[str, Any]:
        return SetupsAPI.get_filter_params_by_items(
            list(SetupItem.objects.filter(setup=setup).values_list('item__id', "number")),
            exclude_item_id
        )
