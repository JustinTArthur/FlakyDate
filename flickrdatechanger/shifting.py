from datetime import timedelta, datetime, date

def set_new_date(flickr, photo, new_datetime):
    flickr.photos_setDates(photo_id=photo.get('id'), date_posted=new_datetime)

def shift_date(flickr, photo, year_shift, days_shift):
    current_datetime = photo.get('date_upload',photo.find('dates').attrib('posted'))
    new_date = date(current_datetime.year + year_shift, current_datetime.month, current_datetime.day)
    new_datetime = datetime.combine(new_date, current_datetime.time())
    new_datetime = new_datetime + timedelta(days=days_shift)
    
    set_new_date(flickr, photo, new_datetime)