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
                result['attributes']['fields']['content_type'] = result[
                    'attributes']['fields'].pop('post.primary_content_type')
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

                lst_json.append(result['attributes']['fields'])
            except KeyError:
                pass

        return lst_json
