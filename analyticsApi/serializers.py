from rest_framework import serializers
from .models import SmAccount


class SmAccountSerializer(serializers.ModelSerializer):
    '''
        Serializer for SmAccount model
    '''
    class Meta:
        model = SmAccount
        fields = '__all__'
