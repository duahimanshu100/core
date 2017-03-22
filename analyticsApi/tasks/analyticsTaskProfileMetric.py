# Create your tasks here
from __future__ import absolute_import, unicode_literals
from analyticsApi.models import Profile, ProfileEngagementMetric
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from analytics.celery import app
from django.db import connection
import datetime


@app.task
def saveEngagementAverageByMonths(profile_id, num_of_months, engagement_type):
    print('Engagement Avg For ' + str(profile_id))
    last_month_date = (datetime.date.today() -
                       datetime.timedelta(num_of_months * 365 / 12))
    profile_engagement_metric, created = ProfileEngagementMetric.objects.get_or_create(
        profile_id=profile_id, engagement_type=engagement_type)
    sql = '''SELECT pm.engagement_count,
        CASE WHEN post.created_at::time < date_trunc('hour', post.created_at::time) + interval '45 minutes' 
        THEN EXTRACT(HOUR FROM post.created_at)::integer ELSE (EXTRACT(HOUR FROM post.created_at) + 1)::integer 
        END AS "HOUR_OF_POSTING", post.created_at::time, 
        EXTRACT(DOW FROM post.created_at)::integer as dayOfWeek FROM public."analyticsApi_post" post 
        LEFT JOIN public."analyticsApi_postlatestmetric" pm ON (pm.post_id_id=post.post_id) 
        WHERE post.profile_id = %s AND post.created_at >= %s '''
    cursor = connection.cursor()
    try:
        cursor.execute(sql, [profile_id, last_month_date])
        arr = []
        for i in range(24):
            for j in range(7):
                arr.append([i, j, 0, 0])
        for row in cursor.fetchall():
            row_zero = row[0]
            if not row_zero:
                row_zero = 0
            tmp_hour = row[1]
            tmp_day = row[3]
            if(tmp_hour == 24):
                tmp_hour = 0
                tmp_day += 1
                if(tmp_day == 7):
                    tmp_day = 0
            arr[tmp_hour * 7 + tmp_day][2] += 1
            arr[tmp_hour * 7 + tmp_day][3] += row_zero
        for elem in arr:
            tmp = 0
            if elem[2]:
                tmp = round(elem[3] / elem[2])
            elem.pop()
            elem.pop()
            elem.append(tmp)
        profile_engagement_metric.profile_id = profile_id
        profile_engagement_metric.json_response = arr
        profile_engagement_metric.engagement_type = engagement_type
        profile_engagement_metric.save()
    finally:
        cursor.close()


@app.task
def saveEngagementFrequencyByMonths(profile_id, num_of_months, engagement_type):
    print('Engagement Freq For ' + str(profile_id))
    last_month_date = (datetime.date.today() -
                       datetime.timedelta(num_of_months * 365 / 12))
    profile_engagement_metric, created = ProfileEngagementMetric.objects.get_or_create(
        profile_id=profile_id, engagement_type=engagement_type)
    sql = '''SELECT pm.engagement_count, 
    CASE WHEN post.created_at::time < date_trunc('hour', post.created_at::time) + interval '45 minutes' 
    THEN EXTRACT(HOUR FROM post.created_at)::integer 
    ELSE (EXTRACT(HOUR FROM post.created_at) + 1)::integer 
    END AS "HOUR_OF_POSTING", post.created_at::time, 
    EXTRACT(DOW FROM post.created_at)::integer as dayOfWeek FROM public."analyticsApi_post" post 
    LEFT JOIN public."analyticsApi_postlatestmetric" pm ON (pm.post_id_id=post.post_id) 
    WHERE post.profile_id = %s AND post.created_at >= %s '''
    cursor = connection.cursor()
    try:
        cursor.execute(sql, [profile_id, last_month_date])
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
        profile_engagement_metric.engagement_type = engagement_type
        profile_engagement_metric.save()
    finally:
        cursor.close()


@periodic_task(run_every=(crontab(minute=0, hour=0, day_of_week='sunday')), name="saveProfileEngagementWeekly", ignore_result=True)
def saveProfileEngagementWeekly():
    for profile in Profile.objects.filter(is_active=True).order_by('profile_id'):
        print('Saving Engagement for Profile Id - ' +
              str(profile.profile_id) + ' Starts For 6 Months')
        # saveEngagementAverageByMonths(str(profile.profile_id), 6, 4)
        # saveEngagementFrequencyByMonths(str(profile.profile_id), 6, 6)
        saveEngagementAverageByMonths.apply_async(
            args=[str(profile.profile_id), 6, 4])
        saveEngagementFrequencyByMonths.apply_async(
            args=[str(profile.profile_id), 6, 6])
        print('Saving Engagement for Profile Id - ' +
              str(profile.profile_id) + ' Finished For 6 Months')
        print('Saving Engagement for Profile Id - ' +
              str(profile.profile_id) + ' Start For 1 year')
        # saveEngagementAverageByMonths(str(profile.profile_id), 12, 5)
        # saveEngagementFrequencyByMonths(str(profile.profile_id), 12, 7)
        saveEngagementAverageByMonths.apply_async(
            args=[str(profile.profile_id), 12, 5])
        saveEngagementFrequencyByMonths.apply_async(
            args=[str(profile.profile_id), 12, 7])
        print('Saving Engagement for Profile Id - ' +
              str(profile.profile_id) + ' Finished For 1 year')
