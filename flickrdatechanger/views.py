from flickrdatechanger.forms import DateAdjustmentForm
from flickrdatechanger.decorators import require_flickr_auth
from flickrdatechanger.shifting import set_new_date, shift_date
from django.shortcuts import redirect, render_to_response

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
            if form.cleaned_data['use_shift']:
                for photo in photos:
                    years_shift = form.cleaned_data['shift_years']
                    days_shift = form.cleaned_data['shift_days']
                    if form.cleaned_data['shift_direction'] == "-":
                        years_shift = 0 - years_shift
                        days_shift = 0 - days_shift
                    shift_date(flickr, photo, years_shift, days_shift)
            else:
                #Just setting a new date.
                for photo in photos:
                    set_new_date(flickr, photo, form.cleaned_data['new_date'])
            return redirect('home')
    return render_to_response("flickrdatechanger/home.html", {'form' : form})

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