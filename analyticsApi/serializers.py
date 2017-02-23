from rest_framework import serializers

from .models import Profile, Post, PostHashTag, PostFilter, ProfileLike, PostLike, PostShare, PostComment, PostMetric, PostVision
from .models import SmAccount, ProfileMetric
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


class PostLikeSerializer(serializers.ModelSerializer):
    '''
        Serializer for Post Ha  shtag model
    '''

    class Meta:
        model = PostLike
        fields = '__all__'


class PostMetricSerializer(serializers.ModelSerializer):
    '''
        Serializer for Post Ha  shtag model
    '''

    class Meta:
        model = PostMetric
        fields = '__all__'


class PostWithMetricSerializer(serializers.ModelSerializer):
    '''
        Serializer for Post Ha  shtag model
    '''

    class Meta:
        model = PostMetric
        fields = '__all__'
        depth = 1


class PostMetricSerializerV2(serializers.ModelSerializer):
    '''
        Serializer for Post Ha  shtag model
    '''

    class Meta:
        model = PostMetric
        fields = '__all__'
        depth = 1


class PostShareSerializer(serializers.ModelSerializer):
    '''
        Serializer for Post Ha  shtag model
    '''

    class Meta:
        model = PostShare
        fields = '__all__'


class PostCommentSerializer(serializers.ModelSerializer):
    '''
        Serializer for Post Ha  shtag model
    '''

    class Meta:
        model = PostComment
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

        self.update_counts(post, validated_data)

        return post

    def update(self, instance, validated_data):
        update_response = super(PostSerializer, self).update(
            instance, validated_data)
        self.update_counts(instance, validated_data)

        return update_response

    def get_diff(self, post, model, field, count, count_field):
        instance = model.objects.filter(post_id=post).order_by(field).first()
        if instance:
            return getattr(instance, count_field) - count
        else:
            return count

    def update_counts(self, instance, validated_data):
        shares_count = validated_data.get('shares_count', 0)
        likes_count = validated_data.get('likes_count', 0)
        replies_count = validated_data.get('replies_count', 0)
        like_diff = self.get_diff(
            instance, PostLike, '-created_at', likes_count, 'like_count') if likes_count else 0
        share_diff = self.get_diff(instance, PostShare, '-created_at', shares_count,
                                   'share_count') if shares_count else 0
        comment_diff = self.get_diff(instance, PostComment, '-created_at', replies_count,
                                     'comment_count') if likes_count else 0

        PostLike.objects.create(
            post_id=instance, like_count=likes_count, like_diff=like_diff)

        PostShare.objects.create(
            post_id=instance, share_count=shares_count, share_diff=share_diff)

        PostComment.objects.create(
            post_id=instance, comment_count=replies_count, comment_diff=comment_diff)

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


class ProfileMetricSerializer(serializers.ModelSerializer):
    '''
        Serializer for Profile Like Filter model
    '''

    class Meta:
        model = ProfileMetric
        fields = '__all__'


class PostsListSerializer(serializers.ModelSerializer):
    '''
        Serializer for getting list of Posts
    '''

    class Meta:
        model = Post
        fields = '__all__'


class PostsVisionSerializer(serializers.ModelSerializer):
    '''
        Serializer for getting list of Posts
    '''

    class Meta:
        model = PostVision
        fields = '__all__'


class PostsListWithVisionSerializer(serializers.ModelSerializer):
    '''
        Serializer for getting list of Posts
    '''
    # post_vision = serializers.SerializerMethodField(read_only=True)
    # post_vision = PostsVisionSerializer(read_only=True)

    def to_representation(self, instance):
        data = super(PostsListWithVisionSerializer,
                     self).to_representation(instance)
        post_vision = PostVision.objects.filter(post=instance)
        post_metric = PostMetric.objects.filter(
            post_id=instance, is_latest=True).first()
        post_hash_tags = PostHashTag.objects.filter(
            post_id=instance)
        post_filters = PostFilter.objects.filter(
            post_id=instance)
        if post_vision:
            data['post_vision'] = PostsVisionSerializer(post_vision[0]).data
        if post_metric:
            data['post_metric'] = PostMetricSerializer(post_metric).data
        if post_hash_tags:
            data['post_hash_tags'] = PostHashTagSerializer(
                post_hash_tags, many=True).data
        if post_filters:
            data['post_filters'] = PostFilterSerializer(
                post_filters, many=True).data

        return data

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


class PostSerializerCreate(serializers.ModelSerializer):
    '''
        Serializer for SmAccount model
    '''
    class Meta:
        model = Post
        fields = '__all__'
