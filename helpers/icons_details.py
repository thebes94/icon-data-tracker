from selenium import webdriver
from helpers.scroll_page import scroll

# input: driver - a valid webdriver
# needs to be logged in to work
def get_icons(driver):
    #navigate to page and load all the icons
    driver.get('https://thenounproject.com/dashboard/uploads/')
    finished_scroll = scroll(driver)

    all_icon_cards = driver.find_elements_by_class_name('icon-card-inner')

    for icon_card in all_icon_cards:
        number_downloads_text = icon_card.find_elements_by_css_selector('span')[0].text
        number_downloads = number_downloads_text[:number_downloads_text.find('download')-1]
        icon_url = icon_card.find_element_by_css_selector('a').get_attribute('href')
        icon_id = icon_url[icon_url.rfind('/')+1:]
        icon_url = icon_url[:icon_url.rfind('/')]
        icon_name = icon_url[icon_url.rfind('/')+1:]
        print('Downloads: ', number_downloads, ' Icon Id: ', icon_id, ' Name: ', icon_name)


