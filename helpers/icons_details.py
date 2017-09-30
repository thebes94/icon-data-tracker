from selenium import webdriver
from helpers.scroll_page import scroll
from openpyxl import Workbook

# input: driver - a valid webdriver, wb - an existing excel workbook
# needs to be logged in to work
def get_icons(driver, wb):
    #navigate to page and load all the icons
    driver.get('https://thenounproject.com/dashboard/uploads/')
    finished_scroll = scroll(driver)

    #worksheet where we are gonna output our revenue data
    ws = wb.create_sheet("Icons", 0)
    ws.append(['Name', 'Icon ID', 'Downloads'])


    all_icon_cards = driver.find_elements_by_class_name('icon-card-inner')

    for icon_card in all_icon_cards:
        number_downloads_text = icon_card.find_elements_by_css_selector('span')[0].text
        number_downloads = number_downloads_text[:number_downloads_text.find('download')-1]
        icon_url = icon_card.find_element_by_css_selector('a').get_attribute('href')
        icon_id = icon_url[icon_url.rfind('/')+1:]
        icon_url = icon_url[:icon_url.rfind('/')]
        icon_name = icon_url[icon_url.rfind('/')+1:]
        #print('Downloads: ', number_downloads, ' Icon Id: ', icon_id, ' Name: ', icon_name)
        ws.append([icon_name, icon_id, number_downloads])

