# WHAT WE NEED TO CHANGE TO MAKE THIS WORK FOR US:
# 1. The user needs to be able to input any city and the driver should automatically pull up results (currently requires manual input of url)

"""
Install webdriver-manager in Command Prompt
pip install webdriver-manager
"""

import sys
import csv
from selenium import webdriver
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# default path to file to store data
path_to_file = "/Users/gius/Desktop/reviews.csv"

# default number of scraped pages
num_page = 10

"""Trying to make this API work for any city/attraction"""
CITY_NAME = input('What is the city name?: ')
ATTRACTION_NAME = input('What attraction are you looking to see?: ') 

# default tripadvisor website of hotel or things to do (attraction/monument) 
# url = f'https://www.tripadvisor.com/Hotel_Review-g60763-d1218720-Reviews-{ATTRACTION_NAME}-{CITY_NAME}.html'
url = f'https://www.tripadvisor.com/Attraction_Review-g187791-d192285-{ATTRACTION_NAME}-{CITY_NAME}.html'
# url = f'https://www.tripadvisor.com'


# if you pass the inputs in the command line
if (len(sys.argv) == 4):
    path_to_file = sys.argv[1]
    num_page = int(sys.argv[2])
    url = sys.argv[3]

# import the webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

"""Julia's attempt to fix things"""
# enter_searchbar = driver.find_element_by_id("id-search-field")
# enter_searchbar.send_keys('Museum of Modern Art Boston')
# click_button = driver.find_element_by_xpath("//button[normalize-space()='GO']")
# click_button.click()


# open the file to save the review
csvFile = open(path_to_file, 'a', encoding="utf-8")
csvWriter = csv.writer(csvFile)

# change the value inside the range to save more or less reviews
for i in range(0, num_page):

    # expand the review 
    time.sleep(2)
    driver.find_element_by_xpath(".//div[contains(@data-test-target, 'expand-review')]").click()

    container = driver.find_elements_by_xpath("//div[@data-reviewid]")
    dates = driver.find_elements_by_xpath(".//div[@class='_2fxQ4TOx']")

    for j in range(len(container)):

        rating = container[j].find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class").split("_")[3]
        title = container[j].find_element_by_xpath(".//div[contains(@data-test-target, 'review-title')]").text
        review = container[j].find_element_by_xpath(".//q[@class='IRsGHoPm']").text.replace("\n", "  ")
        date = " ".join(dates[j].text.split(" ")[-2:])
    
        csvWriter.writerow([date, rating, title, review]) 
        
    # change the page            
    driver.find_element_by_xpath('.//a[@class="ui_button nav next primary "]').click()

driver.quit()