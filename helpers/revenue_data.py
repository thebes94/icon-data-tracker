from selenium import webdriver
import config
from openpyxl import Workbook

# input: driver - a valid webdriver, wb - an excel workbook
# goes to revenue page and collects all pas
def all_revenues(driver, wb):
    #worksheet where we are gonna output our revenue data
    ws = wb.create_sheet("Revenues", 0)
    ws.append(['Month', 'Year', 'Income', 'Paid', 'Purchases', 'Per Perchase', 'Subscriptions', 'Per Subscription', 'API', 'Per API'])

    # the nounproject page that 
    driver.get('https://thenounproject.com/'+config.noun_project_username+'/royalties/')

    months_revenues = driver.find_elements_by_class_name('data')
    
    for month_info in months_revenues:
        month_year = month_info.find_element_by_class_name('royalty-col-year').text
        month_number = month_year[:2]
        year_number = '20' + month_year[3:5]
        income = month_info.find_elements_by_class_name('royalty-col-total')[0].text[1:]
        paid_out = month_info.find_elements_by_class_name('royalty-col-total')[1].text[1:] 
       
        #okay, now we are parsing the numbers out of each
        purchases_text = month_info.find_elements_by_css_selector('td')[2].find_element_by_css_selector('span').text
        purchases_count = purchases_text[:purchases_text.find('icon')-1]
        purchase_revenue_each = purchases_text[purchases_text.find('$')+1:]
     
        subscriptions_text = month_info.find_elements_by_css_selector('td')[3].find_element_by_css_selector('span').text
        subscriptions_count = subscriptions_text[:subscriptions_text.find('icon')-1]
        subscription_revenue_each = subscriptions_text[subscriptions_text.find('$')+1:]

        api_text = month_info.find_elements_by_css_selector('td')[4].find_element_by_css_selector('span').text
        api_count = api_text[:api_text.find('icon')-1]
        api_revenue_each = api_text[api_text.find('$')+1:]

        ws.append([month_number, year_number, income, paid_out, purchases_count, purchase_revenue_each, 
                    subscriptions_count, subscription_revenue_each, api_count, api_revenue_each])
