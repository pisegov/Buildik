from typing import Any, Dict, List
from setups.models import Setup, SetupItem
import setups.config as setup_conf
import pccomponents.models as pcc
import pccomponents.config as conf


class SetupsAPI:
    def get_filter_params(setup: Setup) -> Dict[str, Any]:
        filters = {
            pcc.item_category_by_number(category[0])+'_number': 0
            for category in pcc.ITEM_CATEGORY_CHOICES
        }


        for setup_item in SetupItem.objects.filter(setup=setup):
            item = {
                **pcc.item_class_by_number(setup_item.item.category).objects.get(id=setup_item.item.id).get_full_item(),
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
                     field in conf.LESS_OR_EQUAL_RELATIONS:
                    filters[field] = item[field]

        # TODO: belongings, having_all

        filters['total_memory_modules'] = filters['RAM_number']

        for f in filters:
            filters[f] = str(filters[f])
        return filters

        return filters