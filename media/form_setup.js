$(function() {
	$("#id_new_date").datepicker();
	toggle_date_change_approach();
	$('input[name=use_shift]').change(toggle_date_change_approach);
});

function toggle_date_change_approach() {
	if ($('input[name=use_shift]:checked').length > 0) {
		$('fieldset#date_form_fields').hide();
		$('fieldset#shift_form_fields').show();
	} else {
		$('fieldset#date_form_fields').show();
		$('fieldset#shift_form_fields').hide();
	}
}