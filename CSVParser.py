import csv
import os
from glob import glob
import numpy as np

from Parsing.OrganizeTests import GETCSVs
from Parsing.ParseTests import by_chart

USER_ID = "user_nickname:"  # String in user_details.txt followed by user_id

# Choose an existing folder where to look for the CSVs
test_results_path = input("Enter the path of the directory: ")
if len(test_results_path) == 0:
    test_results_path = '.'
assert os.path.exists(test_results_path), "I did not find the file at " + str(test_results_path)

if not os.path.exists(test_results_path + "\\parsed"):
    os.makedirs(test_results_path + "\\parsed")

CHARTIDS = ["b_wn", "bm", "by", "c_wn", "cg", "cr", "g_wn", "gc", "gm", "m_wn", "mb", "mg", "r_wn", "rc", "ry",
            "y_wn", "yb", "yr"]
rows_number = len(CHARTIDS)

GROUP_1_ANSWER = "yes"
GROUP_2_ANSWER = "no"
ORGANIZE_BY = "user_is_colorblind:"


def merge_data(dict_1, dict_2):
    for id in dict_1:
        for val in dict_2[id]:
            dict_1[id].append(val)
    return dict_1


def serialize(dict):
    output_string = "\""
    for val in dict:
        output_string += (val + "\",\"")
    return output_string[:-2]


csvs = GETCSVs(test_results_path, ORGANIZE_BY, min_rows=len(CHARTIDS), verbose=True)

column_to_extract = input("Enter the column you want to extract from the CSV files: ")

bychart_group1 = by_chart(csvs[GROUP_1_ANSWER], CHARTIDS, column_to_extract=column_to_extract)
bychart_group1 = merge_data(bychart_group1, by_chart(csvs["unsure"], CHARTIDS, column_to_extract=column_to_extract))
bychart_group2 = by_chart(csvs[GROUP_2_ANSWER], CHARTIDS, column_to_extract=column_to_extract)

results_group1 = {}
results_group2 = {}

if np.all(np.char.isnumeric(bychart_group1[CHARTIDS[0]])) or np.all(np.char.isnumeric(bychart_group2[CHARTIDS[0]])):
    decimal_places = input("How many decimal places? ")
    for id in CHARTIDS:
        results_group1[id] = np.around(np.median(bychart_group1[id]), int(decimal_places))
        results_group2[id] = np.around(np.median(bychart_group2[id]), int(decimal_places))
else:
    for id in CHARTIDS:
        results_group1[id] = bychart_group1[id]
        results_group2[id] = bychart_group2[id]

with open(test_results_path + '\\parsed\\results_cdo__' + column_to_extract + '.csv', 'w', encoding='UTF8',
          newline='') as f:
    #writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    for key, value in results_group1.items():
        f.write("\""+key+"\","+serialize(value))
        f.write("\n")

with open(test_results_path + '\\parsed\\results_cno__' + column_to_extract + '.csv', 'w', encoding='UTF8',
          newline='') as f:
    #writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    for key, value in results_group2.items():
        f.write("\""+key+"\","+serialize(value))
        f.write("\n")
