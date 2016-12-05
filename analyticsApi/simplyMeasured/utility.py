import json
from django.core.exceptions import ObjectDoesNotExist


class SmUtility:
    '''
    Gernral Utility class for comman functions
    '''
    def list_to_comma_seperated_string(list):
        '''
        convert list to comma seperated strings
        '''
        return ",".join(str(entity) for entity in list)

    @staticmethod
    def get_remaining_page_count(content):
        try:
            content = content.decode("utf-8")
            content = json.loads(content)
            return int(content['meta']['counts']['remaining'])
        except KeyError:
            return 0
