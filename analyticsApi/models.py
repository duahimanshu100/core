from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class SmAccount(models.Model):
    '''
    Simply Measured account model
    '''
    sm_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=200)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200, null=True)
    account_utilization = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.sm_id + ' - ' + self.name


class SmDataSource(models.Model):
    '''
    Simply Measured Data source model
    '''
    ds_id = models.CharField(max_length=200, unique=True)
    sm_account = models.ForeignKey(SmAccount)
    provided_name = models.CharField(
        max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    provided_description = models.CharField(
        max_length=200, null=True, blank=True)
    data_source_type = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    sentiment_enabled = models.BooleanField(default=False)
    elevated_access = models.BooleanField(default=False)
    canonical_id = models.BigIntegerField(default=0)

    def __str__(self):
        return self.ds_id + ' - ' + self.provided_name


class SmDataSourceFeature(models.Model):
    '''
    Simply Measured Data source Feature model
    '''
    feature_id = models.CharField(max_length=200, unique=True)
    sm_data_source = models.ForeignKey(SmDataSource)
    feature_type = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    provider = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    available_start_time = models.DateTimeField()
    available_end_time = models.DateTimeField()
    requested_start_time = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    metadata_list = JSONField()
