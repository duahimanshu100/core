class JsonAnalytics:

    @staticmethod
    def get_post_json(results):
        '''
        Convert simply measured data sources to json array according to model
        '''
        lst_json = []
        for result in results:
            try:
                result['attributes']['fields']['channel'] = result[
                    'attributes']['fields'].pop('channel')
                result['attributes']['fields']['post_id'] = result[
                    'attributes']['fields'].pop('post.id')
                result['attributes']['fields']['profile_id'] = result[
                    'attributes']['fields'].pop('author.id')
                result['attributes']['fields']['body'] = result[
                    'attributes']['fields'].pop('post.body')
                # result['attributes']['fields']['content_type'] = result[
                #     'attributes']['fields'].pop('post.primary_content_type')
                result['attributes']['fields']['url'] = result[
                    'attributes']['fields'].pop('post.url')
                result['attributes']['fields']['target_url'] = result[
                    'attributes']['fields'].pop('post.target_url')

                result['attributes']['fields']['sentiment'] = result[
                    'attributes']['fields'].pop('post.sentiment')

                result['attributes']['fields']['primary_content_type'] = result[
                    'attributes']['fields'].pop('post.primary_content_type')
                result['attributes']['fields']['language'] = result[
                    'attributes']['fields'].pop('post.language')
                result['attributes']['fields']['province'] = result[
                    'attributes']['fields'].pop('post.province')
                result['attributes']['fields']['image_urls'] = result[
                    'attributes']['fields'].pop('post.image_urls')
                result['attributes']['fields']['post_hash'] = result[
                    'attributes']['fields'].get('post.hashtags', {})
                if result['attributes']['fields']['post_hash']:
                    result['attributes']['fields']['has_hashtag'] = True
                result['attributes']['fields']['post_filter'] = result[
                    'attributes']['fields'].pop('post.instagram.image_filter', None)
                result['attributes']['fields']['country'] = result[
                    'attributes']['fields'].pop('post.country', None)
                result['attributes']['fields']['datarank'] = result[
                    'attributes']['fields'].pop('datarank')
                # result['attributes']['fields']['geo'] = result[
                #     'attributes']['fields'].pop('post.geo')
                result['attributes']['fields']['content_types'] = result[
                    'attributes']['fields'].pop('post.content_types')
                result['attributes']['fields']['created_at'] = result[
                    'attributes']['fields'].pop('post.creation_date')

                metrics = result['attributes']['metrics']
                result['attributes']['fields']['engagement_total'] = metrics[
                    'post.engagement_total'] if metrics['post.engagement_total'] else 0
                result['attributes']['fields']['likes_count'] = metrics[
                    'post.likes_count'] if metrics['post.likes_count'] else 0
                result['attributes']['fields'][
                    'replies_count'] = metrics['post.replies_count'] if metrics['post.replies_count'] else 0
                result['attributes']['fields'][
                    'shares_count'] = metrics['post.shares_count'] if metrics['post.shares_count'] else 0

                print(result['attributes']['fields']['post_hash'])
                lst_json.append(result['attributes']['fields'])
            except (KeyError, TypeError) as tp:
                import traceback
                print(traceback.print_exc())

        return lst_json

    @staticmethod
    def get_profiles_json(results, account_id):
        '''
        Convert simply measured data sources to json array according to model
        '''
        lst_json = []
        for result in results:
            try:
                result['attributes']['fields']['profile_id'] = int(result[
                    'attributes']['fields'].pop('profile.id'))
                result['attributes']['fields']['channel_type'] = result[
                    'attributes']['fields'].pop('channel')
                result['attributes']['fields']['link'] = result[
                    'attributes']['fields'].pop('profile.link')
                result['attributes']['fields']['handle'] = result[
                    'attributes']['fields'].pop('profile.handle')
                result['attributes']['fields']['display_name'] = result[
                    'attributes']['fields'].pop('profile.display_name')
                result['attributes']['fields']['audience_count'] = result[
                    'attributes']['metrics'].pop('profile.audience_count')
                result['attributes']['fields']['sm_account'] = account_id
                result['attributes']['fields']['is_active'] = True
                lst_json.append(result['attributes']['fields'])
            except KeyError:
                pass

        return lst_json

    @staticmethod
    def get_profiles_likes_json(results, profile_id):
        '''
        Convert simply measured data sources to json array according to model
        '''
        lst_json = []
        for result in results:
            if(result['attributes']['metrics']['post.likes_count'] > 0):
                # try:
                result['attributes']['metrics']['like_count'] = result[
                    'attributes']['metrics'].pop('post.likes_count')
                result['attributes']['metrics']['profile_id'] = profile_id
                result['attributes']['metrics']['updated_at'] = result[
                    'attributes']['dimensions'].pop('post.creation_date.by(hour)')
                lst_json.append(result['attributes']['metrics'])
                # except KeyError:
                #     pass

        return lst_json
