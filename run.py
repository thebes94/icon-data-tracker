# from flask import Flask
#from lxml import html
import requests
from selenium import webdriver
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import csv
import config
# app = Flask(__name__)

#@app.route('/')
# def index():
#    return '<h1>Hello World</h1>'

# if __name__ == '__main__':
#    app.run(debug=True)

# the current time, we will need since datetimes are relative to the now
now = datetime.now()

# Optional argument, if not specified will search path.
driver = webdriver.Chrome('/Applications/chromedriver')
# options = webdriver.ChromeOptions()
# options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
# options.add_argument('window-size=800x841')
# options.add_argument('headless')
# driver = webdriver.Chrome(chrome_options=options)
driver.get('https://thenounproject.com/'+config.noun_project_username+'/activity/')

# need to log in first to the noun project
facebook_button = driver.find_element_by_class_name('ui_facebook')
facebook_button.click()
username = driver.find_element_by_id('email')
username.send_keys(config.facebook_username)
password = driver.find_element_by_id('pass')
password.send_keys(config.facebook_password)
login_button = driver.find_element_by_id('loginbutton')
login_button.click()

# need to scroll down the page until we've loaded all the desired icons
# todo bad cause it relies on arbitary delay... try to find alternative
lastHeight = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    newHeight = driver.execute_script("return document.body.scrollHeight")
    if newHeight == lastHeight:
        try:
            if driver.find_element_by_class_name('hidden'):
        # todo perhaps check if loading symbol hidden
                break
        except:
            pass
    lastHeight = newHeight


# read the info we care about from each activity entry
activities_list = driver.find_element_by_id('activity-list')
activities = activities_list.find_elements_by_css_selector('li')
with open(config.csv_file_name, 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Icon Id','Username', 'Action', 'Datetime']) #headers

    for activity in activities:
        # determine the id of the icon
        action_user_full = activity.find_elements_by_css_selector('a')[0].get_attribute('href')
        icon_link = activity.find_elements_by_css_selector('a')[1].get_attribute('href')
        last_slash = icon_link.rfind('/')
        last_slash_user = action_user_full.rfind('/')
        icon_id = icon_link[last_slash + 1:]
        action_user = action_user_full[last_slash_user + 1:]

        # the nature of the activity (purchased, downloaded, self-action)
        activity_type_full = activity.find_element_by_css_selector('span').get_attribute('class')
        activity_type = 'Download'
        if activity_type_full == 'action ui_dollar-sign-circle-filled':
            activity_type = 'Purchase'
        elif activity_type_full == 'action ui_heart':
            activity_type = 'Favorite'
        elif activity_type_full == 'action ui_kit':
            activity_type = 'Kit'

        # calculate the datetime of the activity, best we can
        activity_datetime = now.replace(second=0,microsecond=0) #todo implement rounding yourself if you care
        activity_time = activity.find_element_by_class_name('date-of-action').text
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

        # enter into database the info we've collected
        filewriter.writerow([icon_id,action_user, activity_type, activity_datetime])

driver.quit()
