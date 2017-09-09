from selenium import webdriver
import time

# input: driver should be an active webdriver
# output: returns true when it seems no more icons can be loaded
# need to scroll down the page until we've loaded all the desired icons
# todo partly relies on arbitary delay... try to find alternative
def scroll(driver):
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            try:
                if driver.find_element_by_class_name('hidden'):
                    return True
            except:
                pass
        lastHeight = newHeight