from rest_framework import serializers
from .models import SmAccount
from .models import SmDataSource
from .models import Profile, Post, PostHashTag, PostFilter, ProfileLike


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


class PostHashTagSerializer(serializers.ModelSerializer):
    '''
        Serializer for Post Ha  shtag model
    '''

    class Meta:
        model = PostHashTag
        fields = '__all__'


class PostFilterSerializer(serializers.ModelSerializer):
    '''
        Serializer for Post Filter model
    '''

    class Meta:
        model = PostFilter
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    '''
        Serializer for SmAccount model
    '''
    post_hash = serializers.ListField(
        child=serializers.CharField(required=False, allow_null=True), required=False, allow_null=True
    )
    post_filter = serializers.CharField(required=False, allow_null=True)

    def create(self, validated_data):
        post_hashes = validated_data.pop('post_hash', {})
        post_filter = validated_data.pop('post_filter',)
        post = Post.objects.create(**validated_data)

        if post_hashes:
            for post_hash in post_hashes:
                PostHashTag.objects.create(profile_id=validated_data[
                                           'profile_id'], post_id=post.post_id, name=post_hash)
        if post_filter:

            PostFilter.objects.create(profile_id=validated_data[
                                      'profile_id'], post_id=post.post_id, name=post_filter)

        return post

    # def update(self, instance, validated_data):
    #     import pdb
    #     pdb.set_trace()
    #     # Update the book instance
    #     # instance.title = validated_data['title']
    #     # instance.save()
    #
    #     # # Delete any pages not included in the request
    #     # page_ids = [item['page_id'] for item in validated_data['pages']]
    #     # for page in instance.books:
    #     #     if page.id not in page_ids:
    #     #         page.delete()
    #     #
    #     # # Create or update page instances that are in the request
    #     # for item in validated_data['pages']:
    #     #     page = Page(id=item['page_id'], text=item['text'], book=instance)
    #     #     page.save()
    #
    #     return instance

    class Meta:
        model = Post
        # fields = Post._meta.get_all_field_names() + ['post_hash', 'post_filter']
        fields = ('post_hash', 'post_filter', 'post_id', 'profile_id',
                  'created_at', 'body', 'engagement_total', 'likes_count',
                  'replies_count', 'shares_count', 'channel', 'url', 'target_url',
                  'sentiment', 'primary_content_type', 'language', 'province', 'image_urls', 'content_type',
                  'country', 'datarank'
                  )


class ProfileLikeSerializer(serializers.ModelSerializer):
    '''
        Serializer for Profile Like Filter model
    '''

    class Meta:
        model = ProfileLike
        fields = '__all__'


class PostsListSerializer(serializers.ModelSerializer):
    '''
        Serializer for getting list of Posts
    '''
    class Meta:
        model = Post
        fields = '__all__'


class PostsFilterUsageSerializer(serializers.ModelSerializer):
    '''
        Serializer for getting list of Posts
    '''
    class Meta:
        model = PostFilter
        fields = '__all__'


class PostsTagUsageSerializer(serializers.ModelSerializer):
    '''
        Serializer for getting list of Posts
    '''
    class Meta:
        model = PostHashTag
        fields = '__all__'
