from rest_framework import serializers
from .models import SmAccount
from .models import SmDataSource
from .models import SmDataSourceFeature


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


class SmDataSourceFeatureSerializer(serializers.ModelSerializer):
    '''
        Serializer for SmAccount model
    '''
    data_source = SmDataSourceSerializer(read_only=True)

    class Meta:
        model = SmDataSourceFeature
        fields = '__all__'
