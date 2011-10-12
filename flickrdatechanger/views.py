from flickrdatechanger.forms import DateAdjustmentForm
from flickrdatechanger.decorators import require_flickr_auth

@require_flickr_auth
def home(request):
    if request.method == "GET":
        form = DateAdjustmentForm()
    else:
        form = DateAdjustmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.cleaned_data
    