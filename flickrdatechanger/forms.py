from django import forms

class DateAdjustmentForm(forms.Form):
    set_or_photo = forms.ChoiceField(choices=(('photo',"Photograph"),('set',"Set")))
    item_id = forms.CharField()
    new_date = forms.DateTimeField(required=False)
    use_shift = forms.BooleanField()
    shift_direction = forms.ChoiceField(choices=(("-","Backward"),('+',"Forward")))
    shift_years = forms.IntegerField(required=False)
    shift_days = forms.IntegerField(required=False)