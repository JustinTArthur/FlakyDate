from datetime import timedelta, datetime, date

def set_new_date(flickr_api, photo_id, new_date):
    pass

def shift_date(flickr_api, photo_id, year_shift, days_shift):
    current_datetime = None
    new_date = date(current_datetime.year + year_shift, current_datetime.month, current_datetime.day)
    new_datetime = datetime.combine(new_date, current_datetime.time())
    new_datetime = new_datetime + timedelta(days=days_shift)