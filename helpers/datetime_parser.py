import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# input: activity_time - string - any of the standard nounproject relative 'datestamps'
#        now - datetime - time the page was loaded
# output: datetime - stamp with the best persion possible
# choices: x year(s), y month(s) | x month(s), y week(s) | x week(s), y day(s)
#          x day(s), y hour(s) | x hour(s), y minute(s) | x year(s) | x month(s)
#          x week(s) | x day(s) | x hours(s) | x minutes(s)
def parse_noun_date(activity_time, now):
    activity_datetime = now.replace(second=0,microsecond=0) #todo implement rounding yourself if you care
    comma_index = activity_time.find(',')
    minute_index = activity_time.find('minute')
    hour_index = activity_time.find('hour')
    day_index = activity_time.find('day')
    week_index = activity_time.find('week')
    month_index = activity_time.find('month')
    year_index = activity_time.find('year')

    if minute_index >=0 and hour_index < 0: #just minutes
        activity_datetime = activity_datetime - timedelta(minutes=int(activity_time[:minute_index])) 
    elif minute_index >=0 and hour_index >=0: #mintes and hours eg. 1 hour, 5 minutes ago
        activity_datetime = activity_datetime - timedelta(hours=int(activity_time[:hour_index]),minutes=int(activity_time[comma_index+2:minute_index])) 
    elif hour_index >= 0 and day_index < 0: #just hours
        activity_datetime = activity_datetime - timedelta(days=int(activity_time[:hour_index])) 
    elif hour_index >= 0 and day_index >= 0: #days and hours eg. 1 day, 5 hours ago
        activity_datetime = activity_datetime - timedelta(hours=int(activity_time[:day_index]),minutes=int(activity_time[comma_index+2:hour_index])) 
    elif day_index >= 0 and week_index < 0: #just days
        activity_datetime = activity_datetime - timedelta(days=int(activity_time[:day_index])) 
    elif day_index >= 0 and week_index >= 0: #weeks and days eg. 1 week, 5 days
        activity_datetime = activity_datetime - timedelta(days=int(activity_time[:week_index])+int(activity_time[comma_index+2:day_index])) 
    elif week_index >= 0 and month_index < 0: #just weeks
        activity_datetime = activity_datetime - timedelta(days=7*int(activity_time[:week_index-1])) 
    elif week_index >= 0 and month_index >=0: #months and weeks eg. 1 month, 2 weeks
        activity_datetime = activity_datetime - timedelta(days=7*int(activity_time[comma_index+2:week_index])) 
        activity_datetime = activity_datetime - relativedelta(months=int(activity_time[:month_index]))
    elif month_index >= 0 and year_index <=0: #just months
        activity_datetime = activity_datetime - relativedelta(months=int(activity_time[:month_index]))
    elif month_index >= 0 and year_index > 0: #all that could be left is years and months, eg. 1 year, 5 months ago
        activity_datetime = activity_datetime - relativedelta(years=int(activity_time[:year_index]),months=int(activity_time[comma_index+2:month_index])) 
    else:#just year
        activity_datetime = activity_datetime - relativedelta(years=int(activity_time[:year_index])) 

    return activity_datetime