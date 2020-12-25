from social_core.pipeline.partial import partial

@partial
def get_username(backend, details, response, is_new=False, *args, **kwargs):
    return {'username': details['username'] + '~' + backend.__class__.__name__}