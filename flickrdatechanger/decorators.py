"""
Based on require_flickr_auth from flickrapi-docs/documentation/#example-using-django
"""
import flickrapi
import logging
from django.conf import settings
from django.http import HttpResponseRedirect

log = logging.getLogger(__name__)

def require_flickr_auth(view):
    '''View decorator, redirects users to Flickr when no valid
    authentication token is available.
    '''
    def protected_view(request, *args, **kwargs):
        if 'token' in request.session:
            token = request.session['token']
            log.info('Getting token from session: %s' % token)
        else:
            token = None
            log.info('No token in session')

        f = flickrapi.FlickrAPI(settings.FLICKR_API_KEY,
                                settings.FLICKR_API_SECRET, token=token,
                                store_token=False)

        if token:
            # We have a token, but it might not be valid
            log.info('Verifying token')
            try:
                f.auth_checkToken()
            except flickrapi.FlickrError:
                token = None
                del request.session['token']

        if not token:
            # No valid token, so redirect to Flickr
            log.info('Redirecting user to Flickr to get frob')
            url = f.web_login_url(perms='write')
            return HttpResponseRedirect(url)

        # If the token is valid, we can call the decorated view.
        log.info('Token is valid')

        return view(request, f, *args, **kwargs)

    return protected_view