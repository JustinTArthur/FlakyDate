from flickrdatechanger.forms import DateAdjustmentForm
from flickrdatechanger.decorators import require_flickr_auth
from flickrdatechanger.shifting import set_new_date, shift_date

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
                    shift_date(flickr, photo.get('id'), years_shift, days_shift)
            else:
                #Just setting a new date.
                for photo in photos:
                    set_new_date(flickr, photo.get('id'), form.cleaned_data['new_date'])