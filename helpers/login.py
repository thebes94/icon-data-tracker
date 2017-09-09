from selenium import webdriver
import config

# input : driver - should be the webdriver in use
# logs into the site
def login(driver):

    #find the fields/button we want based on type of login
    if config.use_facebook_login:
        facebook_button = driver.find_element_by_class_name('ui_facebook')
        facebook_button.click()
        username = driver.find_element_by_id('email')
        password = driver.find_element_by_id('pass')
        login_button = driver.find_element_by_id('loginbutton')
    else: #not fb, using a noun project account
        username = driver.find_element_by_id('user_id')
        password = driver.find_element_by_id('id_password')
        login_button = driver.find_element_by_class_name('ui_key')
    
    #enter our values and submit login
    username.send_keys(config.username)
    password.send_keys(config.password)
    login_button.click()