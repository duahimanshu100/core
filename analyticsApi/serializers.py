from rest_framework import serializers
from .models import SmAccount
from .models import SmDataSource


class SmAccountSerializer(serializers.ModelSerializer):
    '''
        Serializer for SmAccount model
    '''
    class Meta:
        model = SmAccount
        fields = '__all__'


class SmDataSourceSerializer(serializers.ModelSerializer):
    '''
        Serializer for SmAccount model
    '''

    class Meta:
        model = SmDataSource
        fields = '__all__'

