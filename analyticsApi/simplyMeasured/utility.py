import json


class SmUtility:
    '''
    Gernral Utility class for comman functions
    '''
    @staticmethod
    def get_remaining_page_count(content):
        try:
            content = content.decode("utf-8")
            content = json.loads(content)
            return int(content['meta']['counts']['remaining'])
        except KeyError:
            return 0
