import json
import pandas as pd
import sys
import re

# Remove multiple spaces between two words
# I figured out that the json file often has the name of students separated by two(or more) spaces which lead
# to less number of matches with the csv file. 
def cleanstr(str):
    return re.sub(' +', ' ',str)

csv_file, json_file = sys.argv[1:]
with open(json_file, 'r') as f :
    students = json.load(f) # array of dicts

df = pd.read_csv(csv_file)
dropped = []
for i in range(len(df['Name'])):
    str = df['Name'][i]
    match = re.match('[^a-zA-Z ]', str)
    if (match or (str.count(' ')==0) or str.islower()):
        dropped.append(i)
        #print(str)

df.drop(dropped, inplace = True)
for i in df.index :
    name = df['Name'][i]
    for j in students : 
        if cleanstr(j['n']) == name :
            print(f'{name} {j["i"]} {j["d"]} {df["Organization"][i]} {df["Project"][i]}')
