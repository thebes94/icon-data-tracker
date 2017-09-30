import requests
from selenium import webdriver
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
#import csv
import config
from helpers.login import login
from helpers.scroll_page import scroll
from helpers.datetime_parser import parse_noun_date
from helpers.revenue_data import all_revenues
from helpers.icons_details import get_icons
from openpyxl import Workbook

# from flask import Flask
# app = Flask(__name__)

#@app.route('/')
# def index():
#    return '<h1>Hello World</h1>'

# if __name__ == '__main__':
#    app.run(debug=True)


# Optional argument, if not specified will search path
driver = webdriver.Chrome('/Applications/chromedriver')

#this workbook is where we are gonna write all our data to (for now)
wb = Workbook()

# options = webdriver.ChromeOptions()
# options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
# options.add_argument('window-size=800x841')
# options.add_argument('headless')
# driver = webdriver.Chrome(chrome_options=options)
driver.get('https://thenounproject.com/'+config.noun_project_username+'/activity/')

login(driver)       #login to the app using info from config
get_icons(driver, wb)
all_revenues(driver, wb)

#gotta save all that hard work
wb.save('test.xlsx')

driver.get('https://thenounproject.com/'+config.noun_project_username+'/activity/')
# the current time, we will need since datetimes are relative to the now
now = datetime.now()       
finished_scroll = scroll(driver)      #scrolls icons full page

ws = wb.create_sheet("Activity", 0)
ws.append(['Icon ID', 'Username', 'Action', 'DateTime'])


# read the info we care about from each activity entry
activities_list = driver.find_element_by_id('activity-list')
activities = activities_list.find_elements_by_css_selector('li')
with open(config.csv_file_name, 'wt') as csvfile:

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

        # # calculate the datetime of the activity, best we can
        # activity_datetime = now.replace(second=0,microsecond=0) #todo implement rounding yourself if you care
        activity_time = activity.find_element_by_class_name('date-of-action').text
        activity_datetime = parse_noun_date(activity_time, now)

        # enter into database the info we've collected
        ws.append([icon_id, action_user, activity_type, activity_datetime])
    
#gotta save all that hard work
wb.save('test.xlsx')
driver.quit()
