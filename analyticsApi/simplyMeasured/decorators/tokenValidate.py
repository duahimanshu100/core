from analyticsApi.simplyMeasured.api.token.token import ApiToken


def token_validate():
    def wrap(f):
        def wrapped_f(*args):
            func_result = f(*args)
            if func_result.status and func_result.status == 403:
                obj = ApiToken()
                new_token = obj.get_api_token()
                agrs[0].payload['Authorization'] = 'Bearer ' + new_token
                return f(*args)
            else:
                return func_result
        return wrapped_f
    return wrap
