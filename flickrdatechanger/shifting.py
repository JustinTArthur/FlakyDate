from datetime import timedelta, datetime, date
import time

def set_new_date(flickr, photo, new_date, new_time):
    old_datetime = photo.get('dateupload', None) or photo.find('dates').attrib['posted']
    old_datetime = datetime.fromtimestamp(float(old_datetime))
    new_datetime = datetime.combine(new_date or old_datetime.date(), new_time or old_datetime.time())
    new_timestamp = time.mktime(new_datetime.timetuple()) 
    flickr.photos_setDates(photo_id=photo.get('id'), date_posted=new_timestamp)
    return (photo.get('id'), old_datetime, new_datetime)

def shift_date(flickr, photo, year_shift, days_shift):
    current_datetime = photo.get('dateupload', None) or photo.find('dates').attrib['posted']
    current_datetime = datetime.fromtimestamp(float(current_datetime))
    new_date = date(current_datetime.year + year_shift, current_datetime.month, current_datetime.day)
    if days_shift is not None:
        new_date = new_date + timedelta(days=days_shift)
    return set_new_date(flickr, photo, new_date, current_datetime.time())