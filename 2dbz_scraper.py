'''
2DBZ Web Scraper
Author: Robert Woodhouse
Modified: 03/02/2023
'''

from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pandas
import sqlite3

driver = webdriver.Chrome('/Applications/chromedriver_mac64/chromedriver')
driver.delete_all_cookies()
number_of_products = 0
#search_input = input()

def open_browser_soup():
    #driver.get("https://2dopeboyz.com/?s="+search_input)
    driver.get("https://2dopeboyz.com/?s=kendrick")
    return BeautifulSoup(driver.page_source, "html.parser")

dict = {"title": [],
        "description": [],
        "category": [],
        "image": [],
        "link": []}

soup = open_browser_soup()
root = soup.find('ul', {'class':'penci-grid'})
posts = root.find_all('li', {'class':'list-posttt'})

for post in posts:
    title = post.find('h2', {'class':'grid-title'})
    description = post.find('div', {'class':'item-content'})
    category = post.find('a', {'class':'penci-cat-name'})
    image = post.find('div', {'class':'thumbnail'})
    link = post.find('h2', {'class':'grid-title'})

    dict["title"] += [title.getText()]
    dict["description"] += [description.getText().strip()]
    dict["category"] += [category.getText()]
    dict["image"] += [image]
    dict["link"] += [link.getText()]

print(dict)

driver.close()

'''
res = soup.find('div', class_="product-detail small-12 medium-offset-1 medium-11 large-offset-2 large-10")
title_id = res.find_all('p', class_="title")
value = res.find('span', class_="price") #TODO stop json from changing char uni code
brand = res.find('span', class_="base")
description = res.find('div', class_="description").find('p') #TODO change to find_all list and seperate with /n

product_dict["name"] += [title_id[0].getText()]
product_dict["sku"] += [title_id[1].getText()]
product_dict["value"] += [value.getText().replace('\u00a3', '£')]
product_dict["brand"] += [brand.getText().strip()]
product_dict["description"] += [description.getText()]
'''