# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from analyticsApi.models import Profile, SmAccount, ProfileLike, ProfileMetric, PostVision, Post, ProfileEngagementMetric
from analyticsApi.serializers import ProfileSerializer, PostSerializer, ProfileLikeSerializer, ProfileMetricSerializer
from analyticsApi.simplyMeasured.api.analytics.analytics import ApiAnalytics
from analyticsApi.utility import Utility
from analyticsApi.simplyMeasured.api.token.token import ApiToken
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from datetime import datetime
from analytics.celery import app
from django.db import connection
import json


def syncProfiles(is_hourly=False):
    '''
    SyncProfiless will create or update the profiles
    of simply measured  associated with the token and account id
    '''
    api_token = ApiToken()
    TOKEN = api_token.get_api_token()
    if (TOKEN):
        obj = ApiAnalytics(TOKEN)
        result = obj.get_profiles()
        if result:
            Profile.objects.all().update(is_active=False)

        r = Utility.save_and_update_data(
            ProfileSerializer, result, Profile, 'profile_id', 'profile_id')
        print(r)
        if is_hourly:
            ProfileMetric.objects.filter(
                is_latest=True).update(is_latest=False)
            Utility.save_and_update_data(
                ProfileMetricSerializer, result, ProfileMetric)
    else:
        print('Token Not Found')


def syncAllProfilesPost():
    '''
    SyncPost will create or update the posts
    of simply measured  associated with the token and profiles
    '''
    api_token = ApiToken()
    TOKEN = api_token.get_api_token()
    count = 0
    for profile in Profile.objects.filter(is_active=True):
        count = count + 1
        print('Profile Id Sync Starts for ' +
              str(profile.id) + ' at ' + str(datetime.now()))
        syncProfilePosts(profile.profile_id, profile.sm_account.sm_id, TOKEN)
        print('Profile Id Sync Completed for ' +
              str(profile.id) + ' at ' + str(datetime.now()))
        print('Count is ' + str(count))


def syncAllProfilesLikes():
    '''
    SyncPost will create or update the posts
    of simply measured  associated with the token and profiles
    '''

    for profile in Profile.objects.filter(is_active=True):
        syncProfileLikes(profile)


def syncProfileLikes(profile):
    '''
    syncProfilePosts will create or update the likes
    of simply measured  associated with the token and profile
    '''
    params = {'filter': [
        # 'post.creation_date.gte(2016-01-01)',
        'author.id.eq(' + str(profile.profile_id) + ')'],
        'dimensions': 'post.creation_date.by(hour)',
        'metrics': 'post.likes_count'
    }
    api_token = ApiToken()
    TOKEN = api_token.get_api_token()
    if TOKEN:
        obj = ApiAnalytics(TOKEN)
        ret_data = obj.get_profile_likes(
            profile.sm_account.sm_id, profile.profile_id, params)
        r = Utility.save_and_update_data(
            ProfileLikeSerializer, ret_data, ProfileLike, None, None)
        print(r)
    else:
        print('Token Not Found')


def syncProfilePosts(profile_id, sm_acc_id, TOKEN):
    print(profile_id, sm_acc_id, TOKEN)
    '''
    syncProfilePosts will create or update the posts
    of simply measured  associated with the token and profile
    '''
    params = {'filter': [
        'author.id.eq(' + str(profile_id) + ')'],
        'limit': 1000,
        'fields': 'post.url,post.target_url,post.sentiment,post.primary_content_type,post.language,post.province,post.is_brand,post.image_urls,post.distribution_type,post.country,data_source_id,datarank,channel,author.profile_link,author.image_url,author.display_name,post.geo,post.hashtags,post.instagram.image_filter,post.body,post.id,post.content_types,post.creation_date,author.id',
        'metrics': 'post.replies_count,post.shares_count,post.likes_count,post.engagement_total,post.dislikes_count'
    }
    # api_token = ApiToken()
    # TOKEN = api_token.get_api_token()
    if (TOKEN):
        obj = ApiAnalytics(TOKEN)
        # print(params)
        obj.get_posts(sm_acc_id, params)
    else:
        print('Token Not Found')


def syncSinglePost(post):
    params = {'filter': [
        'post.creation_date.gte(1970-01-01)',
        'author.id.eq(' + str(post.profile_id) + ')',
        'post.id.eq(' + post.post_id + ')'
    ]}
    obj = ApiAnalytics(TOKEN)
    # obj.get_posts_by_profile(profile, None, params)


def syncAllProfileAndPost():
    syncProfiles(is_hourly=True)
    syncAllProfilesPost()


def syncAudienceCount():
    syncProfiles()


@app.task()
def syncVisionByPost(post_id, post_image):
    print("INTO THE SYNC FOR %s IMAGE(%s)" % (post_id, post_image))
    from analyticsApi.vision import get_vision_results
    google_vision, aws_vision = get_vision_results(
        post_image)
    post_vision = PostVision(post=Post.objects.get(post_id=post_id))
    try:
        google_image_properties_annotation = google_vision[
            'responses'][0]['imagePropertiesAnnotation']
    except (KeyError, IndexError):
        google_image_properties_annotation = None

    try:
        google_label_annotation = google_vision[
            'responses'][0]['labelAnnotations']
    except (KeyError, IndexError):
        google_label_annotation = None

    try:
        google_face_annotation = google_vision[
            'responses'][0]['faceAnnotations']
    except (KeyError, IndexError):
        google_face_annotation = None

    try:
        aws_detect_faces = aws_vision['detect_faces']
    except (KeyError, IndexError):
        aws_detect_faces = None
    try:
        aws_detect_labels = aws_vision['detect_labels']
    except (KeyError, IndexError):
        aws_detect_labels = None

    post_vision.google_face_annotation = google_face_annotation
    post_vision.google_label_annotation = google_label_annotation
    post_vision.google_image_properties_annotation = google_image_properties_annotation
    post_vision.aws_detect_faces = aws_detect_faces
    post_vision.aws_detect_labels = aws_detect_labels
    post_vision.save()

    # post_vision


@periodic_task(run_every=(crontab(minute=0, hour='*/1')), name="syncAllVisionProfiles", ignore_result=True)
def syncVision():
    from analyticsApi.models import Post, PostVision
    already_visioned = PostVision.objects.all().values_list('post_id', flat=True)
    already_visioned = list(already_visioned)
    posts = Post.objects.filter(image_urls__isnull=False).exclude(
        post_id__in=already_visioned)
    for post in posts:
        print(post.id)
        if post.image_urls:
            try:
                syncVisionByPost(post.post_id, post.image_urls[0])
                # syncVisionByPost(post, google_vision, aws_vision)
            except Exception:
                import traceback
                print(traceback.print_exc())
                print('ERROR in *****************')
                print(post)


@app.task()
def saveEngagementAverage(profile_id):
    profile_engagement_metric, created = ProfileEngagementMetric.objects.get_or_create(
        profile_id=profile_id, engagement_type=1)
    sql = '''SELECT pm.engagement_count,
        CASE WHEN post.created_at::time < date_trunc('hour', post.created_at::time) + interval '45 minutes' 
        THEN EXTRACT(HOUR FROM post.created_at)::integer ELSE (EXTRACT(HOUR FROM post.created_at) + 1)::integer 
        END AS "HOUR_OF_POSTING", post.created_at::time, 
        EXTRACT(DOW FROM post.created_at)::integer as dayOfWeek FROM public."analyticsApi_post" post 
        LEFT JOIN public."analyticsApi_postmetric" pm ON (pm.post_id_id=post.post_id) 
        WHERE pm.is_latest=True AND post.profile_id = %s '''
    cursor = connection.cursor()
    try:
        cursor.execute(sql, [profile_id])
        arr = []
        for i in range(24):
            for j in range(7):
                arr.append([i, j, 0, 0])

        for row in cursor.fetchall():
            tmp_hour = row[1]
            tmp_day = row[3]
            if(tmp_hour == 24):
                tmp_hour = 0
                tmp_day += 1
                if(tmp_day == 7):
                    tmp_day = 0
            arr[tmp_hour * 7 + tmp_day][2] += 1
            arr[tmp_hour * 7 + tmp_day][3] += row[0]
        for elem in arr:
            tmp = 0
            if elem[2]:
                tmp = round(elem[3] / elem[2])
            elem.pop()
            elem.pop()
            elem.append(tmp)
        profile_engagement_metric.profile_id = profile_id
        profile_engagement_metric.json_response = arr
        profile_engagement_metric.engagement_type = 1
        profile_engagement_metric.save()
    finally:
        cursor.close()


@app.task()
def saveEngagementFrequency(profile_id):
    profile_engagement_metric, created = ProfileEngagementMetric.objects.get_or_create(
        profile_id=profile_id, engagement_type=2)
    sql = '''SELECT pm.engagement_count, 
    CASE WHEN post.created_at::time < date_trunc('hour', post.created_at::time) + interval '45 minutes' 
    THEN EXTRACT(HOUR FROM post.created_at)::integer 
    ELSE (EXTRACT(HOUR FROM post.created_at) + 1)::integer 
    END AS "HOUR_OF_POSTING", post.created_at::time, 
    EXTRACT(DOW FROM post.created_at)::integer as dayOfWeek FROM public."analyticsApi_post" post 
    LEFT JOIN public."analyticsApi_postmetric" pm ON (pm.post_id_id=post.post_id) 
    WHERE pm.is_latest=True AND post.profile_id = %s '''
    cursor = connection.cursor()
    try:
        cursor.execute(sql, [profile_id])
        arr = []
        for i in range(24):
            for j in range(7):
                arr.append([i, j, 0])

        for row in cursor.fetchall():
            tmp_hour = row[1]
            tmp_day = row[3]
            if(tmp_hour == 24):
                tmp_hour = 0
                tmp_day += 1
                if(tmp_day == 7):
                    tmp_day = 0
            arr[tmp_hour * 7 + tmp_day][2] += 1
        profile_engagement_metric.profile_id = profile_id
        profile_engagement_metric.json_response = arr
        profile_engagement_metric.engagement_type = 2
        profile_engagement_metric.save()
    finally:
        cursor.close()


@periodic_task(run_every=(crontab(minute=0, hour=0)), name="saveProfileEngagementDaily", ignore_result=True)
def saveProfileEngagementDaily():
    for profile in Profile.objects.filter(is_active=True):
        print('Saving Engagement for Profile Id - ' +
              str(profile.profile_id) + ' Starts')
        saveEngagementAverage(str(profile.profile_id))
        saveEngagementFrequency(str(profile.profile_id))
        print('Saving Engagement for Profile Id - ' +
              str(profile.profile_id) + ' Finished')


@periodic_task(run_every=(crontab(minute=0, hour='*/2')), name="saveProfileCompleteMetric", ignore_result=True)
def saveProfileCompleteMetric():
    for profile in Profile.objects.filter(is_active=True):
        print('Saving saveProfileCompleteMetric for Profile Id - ' +
              str(profile.profile_id) + ' Starts')
        saveProfileCompleteMetricByProfile(str(profile.profile_id))
        print('Saving saveProfileCompleteMetric for Profile Id - ' +
              str(profile.profile_id) + ' Finished')


def saveProfileCompleteMetricByProfile(profile_id):
    profile_engagement_metric, created = ProfileEngagementMetric.objects.get_or_create(
        profile_id=profile_id, engagement_type=3)
    import datetime
    daysago = datetime.datetime.now() + datetime.timedelta(-10)
    daysago = daysago.strftime("%Y-%m-%d")
    result = []
    sql = '''
    SELECT audience_count
    FROM public."analyticsApi_profilemetric"
    WHERE profile_id = %s ORDER BY created_at DESC LIMIT 1
    '''
    cursor = connection.cursor()
    try:
        cursor.execute(sql, [profile_id])
        query_result = cursor.fetchone()
        if query_result:
            totalFollowerCount = query_result[0]
        else:
            totalFollowerCount = 0
    finally:
        cursor.close()

    result.append(totalFollowerCount)
    sql = '''
    SELECT SUM(pm.comment_count) as totalCommentCount,SUM(pm.like_count) as totalLikeCount 
    FROM public."analyticsApi_postmetric" pm
    WHERE pm.profile_id = %s AND pm.is_latest = True
    '''
    cursor = connection.cursor()
    try:
        cursor.execute(sql, [profile_id])
        query_result = cursor.fetchone()
        totalCommentCount = query_result[0]
        totalLikeCount = query_result[1]
        result.append(totalCommentCount)
        result.append(totalLikeCount)
    finally:
        cursor.close()

    sql = '''
    SELECT SUM(a.like_count) as totalLike, SUM(a.comment_count)
     as totalComment, SUM(a.engagement_count) as totalEngage
     FROM (SELECT  DISTINCT ON (post_id_id)
     like_count, engagement_count,comment_count
     FROM public."analyticsApi_postmetric"
     WHERE profile_id = %s
     AND created_at::date = %s) a
    '''
    cursor = connection.cursor()
    try:
        cursor.execute(sql, [profile_id, daysago])
        query_result = cursor.fetchone()
        if not query_result:
            query_result = (0, 0, 0)
    finally:
        cursor.close()

    daysAgoLikeCount = query_result[0]
    if not daysAgoLikeCount:
        daysAgoLikeCount = 0
    daysAgoCommentCount = query_result[1]
    if not daysAgoCommentCount:
        daysAgoCommentCount = 0
    daysAgoEngagementCount = query_result[2]
    if not daysAgoEngagementCount:
        daysAgoEngagementCount = 0

    like = totalLikeCount - daysAgoLikeCount
    comment = totalCommentCount - daysAgoCommentCount
    result.append(like + comment)

    sql = '''
    SELECT DISTINCT ON (created_at::date) audience_count
    FROM public."analyticsApi_profilemetric"
    WHERE profile_id = %s AND created_at::date = %s
    ORDER BY created_at::date DESC
    '''
    cursor = connection.cursor()
    try:
        cursor.execute(sql, [profile_id, daysago])
        query_result = cursor.fetchone()
        if not query_result:
            daysAgoFollowerCount = 0
        else:
            daysAgoFollowerCount = query_result[0]
            if not daysAgoFollowerCount:
                daysAgoFollowerCount = 0
    finally:
        cursor.close()
    result.append(totalFollowerCount - daysAgoFollowerCount)
    result.append(comment)
    result.append(like)
    result = list(map(int, result))
    profile_engagement_metric.profile_id = profile_id
    profile_engagement_metric.json_response = result
    profile_engagement_metric.engagement_type = 3
    profile_engagement_metric.save()
