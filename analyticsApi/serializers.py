from rest_framework import serializers
from .models import SmAccount
from .models import SmDataSource
from .models import Profile


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


class ProfileSerializer(serializers.ModelSerializer):
    '''
        Serializer for SmAccount model
    '''

    class Meta:
        model = Profile
        fields = '__all__'
