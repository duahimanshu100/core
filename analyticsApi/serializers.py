from rest_framework import serializers

from .models import Profile, Post, PostHashTag, PostFilter, ProfileLike, PostLike, PostShare, PostComment
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
        post_filter = validated_data.pop('post_filter')
        post = Post.objects.create(**validated_data)

        if post_hashes:
            for post_hash in post_hashes:
                PostHashTag.objects.create(profile_id=validated_data[
                    'profile_id'], post_id=post, name=post_hash)
        if post_filter:
            PostFilter.objects.create(profile_id=validated_data[
                'profile_id'], post_id=post, name=post_filter)

        return post

    def update(self, instance, validated_data):
        import pdb
        pdb.set_trace()
        update_response = super(PostSerializer, self).update(instance, validated_data)

        return update_response

    def get_diff(self, post, model, field, count, count_field):
        instance = model.objects.filter(post_id=post).order_by(field).latest()
        if instance:
            return instance.count_field - count
        else:
            return count

    def update_counts(self, instance, validated_data):
        shares_count = validated_data('shares_count', 0)
        likes_count = validated_data('likes_count', 0)
        replies_count = validated_data('replies_count', 0)
        like_diff = self.get_diff(instance, PostLike, 'created_at', likes_count, 'like_count') if likes_count else 0
        share_diff = self.get_diff(instance, PostShare, 'created_at', shares_count,
                                   'share_count') if shares_count else 0
        comment_diff = self.get_diff(instance, PostComment, 'created_at', replies_count,
                                     'comment_count') if likes_count else 0

        PostLike.objects.create(post_id=instance, like_count=likes_count, like_diff=like_diff)

        PostShare.objects.create(post_id=instance, share_count=shares_count, share_diff=share_diff)

        PostComment.objects.create(post_id=instance, comment_count=replies_count, comment_diff=comment_diff)

    class Meta:
        model = Post
        # fields = Post._meta.get_all_field_names() + ['post_hash', 'post_filter']
        fields = ('post_hash', 'post_filter', 'post_id', 'profile_id',
                  'created_at', 'body', 'engagement_total', 'likes_count',
                  'replies_count', 'shares_count', 'channel', 'url', 'target_url',
                  'sentiment', 'primary_content_type', 'language', 'province', 'image_urls', 'content_type',
                  'country', 'datarank', 'has_hashtag'
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
