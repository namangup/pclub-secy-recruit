import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from sys import argv
import re
import os

URL = argv[1]
year = URL[44:48]
filename = f'gsoc{year}.csv'

r = requests.get(URL)
soup = bs(r.content, 'html5lib')
pages = soup.find('span','paginator__pages').get_text().split()[3]

name = []
org = []
proj = []

for i in range(1,int(pages)+1) :
    url = URL + f'?page={i}'
    r = requests.get(url)
    soup = bs(r.content, 'html5lib')
    # Extracting data from HTML code.
    # card stores the div tag in raw HTML format corresponding to each student
    # card_text stores the text from each div tag as a string
    # card_split is two dimensional array , which further stores the splitted from card_text to separate name, organization, and project.
    classstr = re.compile('md-padding archive-project-card__header archive-project-card__header--mod-[0-3]')
    card = soup.find_all('div', classstr)
    card_text = [i.get_text().strip() for i in card]
    card_split = [re.split('[\n\t]+',text) for text in card_text]

    # Loop to group all names, orgs and projs into their respective arrays
    for cards in card_split :
        name.append(cards[0])
        org.append(cards[2][15:])
        proj.append(cards[1])

    print(f'Page {i} Done')

# Using pandas to export the dataframe to a csv file
column_names = ['Name', 'Organization', 'Project']
df = pd.DataFrame({'Name':name, 'Organization':org, 'Project':proj})
df.to_csv(filename,index=False, header=column_names) 
print(f'Data saved to {filename}')