from typing import Any, Dict, List
from setups.models import Setup, SetupItem
import setups.config as setup_conf
import pccomponents.models as pcc
import pccomponents.config as conf


class SetupsAPI:
    def get_filter_params(setup: Setup, exclude_item_id: int = None) -> Dict[str, Any]:
        filters = {
            category[1]+'_number': 0
            for category in pcc.ITEMS
        }

        for setup_item in SetupItem.objects.filter(setup=setup):
            if setup_item.item.id == exclude_item_id:
                continue

            model = pcc.item_class_by_number(setup_item.item.category)
            model_item = model.objects.get(id=setup_item.item.id)
            item = {
                **model_item.get_full_item(),
                'number': setup_item.number,
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
                     field in list(conf.NUMBERED_BELONGING_TO_RELATIONS.values()):
                    filters[field] = item[field]

            for kmodel, l in conf.HAVING_ALL_RELATIONS.items():
                for t in l:
                    spec = t[0]._meta.model_name
                    if spec in item:
                        if t[2] in filters:
                            filters[t[2]] += [item[spec]]
                        else:
                            filters[t[2]] = [item[spec]]

            for l in list(conf.NUMBERED_HAVING_ALL_RELATIONS.values()):
                for t in l:
                    spec = t[0]._meta.model_name
                    if spec in item:
                        if t[2] in filters:
                            filters[t[2]] = filters[t[2]].update({item[spec]: item['number']})
                        else:
                            filters[t[2]] = {item[spec]: item['number']}

        filters['total_memory_modules'] = filters['ram_number']

        return filters