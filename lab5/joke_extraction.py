import openpyxl
import os
import xlrd

jokes_file = openpyxl.load_workbook('Dataset3JokeSet.xlsx').active
jokes_text = dict()

for line in range(1,102):
    jokes_text[line] = jokes_file["A"+str(line)].value




jokes_ratings_files = ["jester-data-1.xls", "jester-data-2.xls", "jester-data-3.xls"]
jokes_ratings = dict()
for i in range(1,101):
    jokes_ratings[i] = list()
for file in jokes_ratings_files:
    file = xlrd.open_workbook(file).sheet_by_index(0)
    for row in file.get_rows():
        for column in range(1,101):
            if( row[column].value != 99):
                jokes_ratings[column].append(row[column].value)

for i in jokes_ratings:
    if(len(jokes_ratings[i]) != 0):
        jokes_ratings[i] = sum(jokes_ratings[i])/len(jokes_ratings[i])

print(jokes_ratings)
import json

with open('jokes_ratings.json', 'w') as fp:
    filedump = dict()
    for i in jokes_ratings:
        filedump[i] = dict()
        filedump[i]["rating"] = jokes_ratings[i]
        filedump[i]["text"] = jokes_text[i]
    json.dump(filedump, fp, indent=4)

fp.close()
