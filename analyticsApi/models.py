from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import datetime

# Create your models here.


class SmToken(models.Model):
    '''
    Simply Measured Token
    '''
    TOKEN_CHOICES = (
        (1, "REFRESH"),
        (2, "API"))
    token = models.CharField(max_length=1000, unique=True)
    token_type = models.IntegerField(choices=TOKEN_CHOICES, default=1)
    is_active = models.BooleanField(default=True)
    sm_id = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token + ' - ' + str(self.token_type)


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
    feature = JSONField()

    def __str__(self):
        return self.ds_id + ' - ' + self.provided_name


class Profile(models.Model):
    '''
    Simply Measured Profiles
    '''
    profile_id = models.BigIntegerField(unique=True)
    sm_account = models.ForeignKey(SmAccount)
    link = models.CharField(max_length=500)
    handle = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200)
    audience_count = models.BigIntegerField(default=0)
    update_likes_time = models.DateTimeField(
        default=datetime(1979, 12, 11, 0, 0))
    channel_type = models.CharField(
        max_length=200, default='instagram')

    def __str__(self):
        return str(self.profile_id) + ' - ' + self.display_name


class Post(models.Model):
    '''
    Simply Measured Profiles
    '''
    post_id = models.CharField(unique=True, max_length=500)
    profile_id = models.BigIntegerField(max_length=500)
    created_at = models.DateTimeField()
    body = models.TextField(null=True, blank=True)
    engagement_total = models.BigIntegerField(default=0)
    likes_count = models.BigIntegerField(default=0)
    replies_count = models.BigIntegerField(default=0)
    shares_count = models.BigIntegerField(default=0)
    channel = models.CharField(
        max_length=200, default='instagram')
    url = models.CharField(max_length=500, null=True, blank=True)
    target_url = models.CharField(max_length=500, null=True, blank=True)
    sentiment = models.CharField(max_length=200, null=True, blank=True)
    primary_content_type = models.CharField(
        max_length=200, null=True, blank=True)
    language = models.CharField(max_length=200, null=True, blank=True)
    province = models.CharField(max_length=200, null=True, blank=True)
    # is_brand = array null
    image_urls = ArrayField(models.CharField(
        max_length=500, blank=True), blank=True, null=True)
    content_type = ArrayField(models.CharField(
        max_length=500, blank=True), blank=True, null=True)
    geo = ArrayField(models.FloatField(blank=True), blank=True, null=True)
    distribution_type = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    # ds_id = models.CharField(max_length=200, null=True, blank=True)
    datarank = models.FloatField(default=0)

    def __str__(self):
        return str(self.profile_id)


class PostHashTag(models.Model):
    '''
    Simply Measured Post Hashtags
    '''
    profile_id = models.CharField(max_length=200)
    post_id = models.CharField(max_length=200)
    name = models.CharField(max_length=500)

    def __str__(self):
        return str(self.post_id) + ' - ' + self.name


class PostFilter(models.Model):
    '''
    Simply Measured Post Filters
    '''
    profile_id = models.CharField(max_length=200)
    post_id = models.ForeignKey(Post, to_field='post_id')
    name = models.CharField(max_length=500)

    def __str__(self):
        return str(self.post_id) + ' - ' + self.name


class ProfileLike(models.Model):
    '''
    Simply Measured Profile Likes
    '''
    profile_id = models.CharField(max_length=200)
    like_count = models.BigIntegerField(max_length=200, default=0)
    updated_at = models.DateTimeField()

    def __str__(self):
        return str(self.profile_id)
