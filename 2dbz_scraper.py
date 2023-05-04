'''
2DBZ Web Scraper
Author: Robert Woodhouse
Modified: 04/05/2023
'''

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas
import sqlite3
import json

driver = webdriver.Chrome('/Applications/WebDrivers/chromedriver')

driver.delete_all_cookies()
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

# Read dictionary to dataframe
df = pandas.DataFrame(data=dict)

# Convert dataframe to JSON string
df.to_json('2dbz_posts.json', indent=3, orient='records')

# Open the JSON file
with open('2dbz_posts.json', 'r') as f:
    data = json.load(f)

# Connect to the SQLite database (creates the database if it doesn't exist)
conn = sqlite3.connect('2dbz_database.db')

# Create a cursor object
cursor = conn.cursor()

# Create the table
cursor.execute('''CREATE TABLE IF NOT EXISTS twodbz_table
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    category TEXT,
    image TEXT,
    link TEXT)''')

# Insert the data into the table
for item in data:
    cursor.execute('''INSERT INTO twodbz_table (title, description, category, image, link)
        VALUES (?, ?, ?, ?, ?)
    ''', (item['title'], item['description'], item['category'], item['image'], item['link']))

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

# Close the webdriver
driver.close()