from django import forms

"""
Here are some HTML5 widgets, since Django 1.3.1 doesn't have them.
"""
class NumberInput(forms.widgets.Input):
    input_type = 'number'

class NumberField(forms.IntegerField):
    widget = NumberInput
    def widget_attrs(self, widget):
        attrs = super(NumberField, self).widget_attrs(widget)
        if self.min_value is not None:
            attrs['min'] = self.min_value
        if self.max_value is not None:
            attrs['max'] = self.max_value
        attrs['step'] = 1
        return attrs

class DateAdjustmentForm(forms.Form):
    set_or_photo = forms.ChoiceField(choices=(('photo',"Photograph"),('set',"Set")))
    item_id = forms.CharField()
    new_date = forms.DateField(required=False)
    new_time = forms.TimeField(label="New time (24hr)", required=False)
    use_shift = forms.BooleanField(label="I just want to shift the dates by some amount of time.", initial=False, required=False)
    shift_direction = forms.ChoiceField(choices=(("-","backward"),('+',"forward")), initial="-")
    shift_years = NumberField(required=False, min_value=0)
    shift_days = NumberField(required=False, min_value=0)