import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from sys import argv
import re

URL = argv[1]
r = requests.get(URL)

soup = bs(r.content, 'html5lib')
name = []
org = []
proj = []

# Extracting data from HTML code.
# card stores the div tag in raw HTML format corresponding to each student
# card_text stores the text from each div tag as a string
# card_split is two dimensional array , which further stores the splitted from card_text to separate name, organization, and project.
card = soup.find_all('div', 'md-padding archive-project-card__header archive-project-card__header--mod-0')
card_text = [i.get_text().strip() for i in card]
card_split = [re.split('[\n\t]+',text) for text in card_text]

# Loop to group all names, orgs and projs into their respective arrays
for cards in card_split :
    name.append(cards[0])
    org.append(cards[2][15:])
    proj.append(cards[1])

# Using pandas to export the dataframe to a csv file
df = pd.DataFrame({'Name':name, 'Organization':org, 'Project':proj})
df.to_csv('gsoc_data.csv',index=False)
print('Data saved to gsoc_data.csv')