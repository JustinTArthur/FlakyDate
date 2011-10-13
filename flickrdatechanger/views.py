from django.contrib import messages
from django.shortcuts import redirect, render_to_response
from django.template.context import RequestContext

from flickrdatechanger.forms import DateAdjustmentForm
from flickrdatechanger.decorators import require_flickr_auth
from flickrdatechanger.shifting import set_new_date, shift_date

import logging
log = logging.getLogger(__name__)

@require_flickr_auth
def home(request, flickr):
    if request.method == "GET":
        form = DateAdjustmentForm()
    else:
        form = DateAdjustmentForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['set_or_photo'] == "set":
                photos = flickr.walk_set(form.cleaned_data['item_id'], extras="date_upload")
            else:
                photos = (flickr.photos_getInfo(photo_id=form.cleaned_data['item_id']),)
            changed_photos = []
            if form.cleaned_data['use_shift']:
                for photo in photos:
                    years_shift = form.cleaned_data['shift_years']
                    days_shift = form.cleaned_data['shift_days']
                    if form.cleaned_data['shift_direction'] == "-":
                        years_shift = 0 - years_shift
                        days_shift = 0 - days_shift
                    change = shift_date(flickr, photo, years_shift, days_shift)
                    changed_photos.append(change)
            else:
                #Just setting a new date.
                for photo in photos:
                    change = set_new_date(flickr, photo, form.cleaned_data['new_date'], form.cleaned_data['new_time'])
                    changed_photos.append(change)
            message = """Successfully updated the following photos:
<table>
 <thead><tr><td>Photo ID</td><td>Old Date</td><td>New Date</td></tr></thead>
 <tbody>%s</tbody>
</table>""" % (["<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % entry for entry in changed_photos],)
            messages.success(request, message)
            return redirect('home')
    return render_to_response("flickrdatechanger/home.html", {'form' : form}, RequestContext(request))

def flickr_authenticate(request):
    from django.conf import settings
    import flickrapi
    log.info('We got a callback from Flickr, store the token')

    f = flickrapi.FlickrAPI(settings.FLICKR_API_KEY,
                            settings.FLICKR_API_SECRET, store_token=False)

    frob = request.GET['frob']
    token = f.get_token(frob)
    request.session['token'] = token

    return redirect('home')