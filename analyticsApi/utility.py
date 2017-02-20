import json
from django.core.exceptions import ObjectDoesNotExist


class Utility:
    '''
    Gernral Utility class for comman functions
    '''

    @staticmethod
    def save_and_update_data(serializer,
                             lst_data, model,
                             db_key=None, data_key=None):
        '''
        create or update the object according
        to specified serializer and model
        '''
        count_update = 0
        count_save = 0
        lst_errors = []

        for data in lst_data:
            if(db_key and data_key):
                try:
                    kw = {db_key: data[data_key]}
                    obj_model = model.objects.get(**kw)
                except ObjectDoesNotExist:
                    obj_model = None
            else:
                obj_model = None

            if not obj_model:
                # Perform creations.
                serialize_data = serializer(
                    data=data)
                if serialize_data.is_valid():
                    obj = serialize_data.save()
                    data['id'] = obj.id
                    count_save = count_save + 1
                else:
                    lst_errors.append(serialize_data.errors)

            else:
                # Perform updations.
                serialize_data = serializer(obj_model,
                                            data=data, partial=True)
                if serialize_data.is_valid():
                    count_update = count_update + 1
                    serialize_data.save()
                else:
                    lst_errors.append(serialize_data.errors)
        return count_save, count_update, lst_errors

    def list_to_comma_seperated_string(list):
        '''
        convert list to comma seperated strings
        '''
        return ",".join(str(entity) for entity in list)

    @staticmethod
    def dictfetchall(cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
