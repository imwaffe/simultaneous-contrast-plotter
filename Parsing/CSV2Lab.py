from ColorUtils.RGB2Lab import RGB2Lab
from ColorUtils.ciede2000 import CIEDE2000
import csv
import os
from glob import glob

USER_ID = "user_nickname:"  # String in user_details.txt followed by user_id

# Choose an existing folder where to look for the CSVs
path = input("Enter the path of the directory: ")
if len(path) == 0:
    path = '.'
assert os.path.exists(path), "I did not find the file at " + str(path)

# Look recursively for the CSVs in directory and subdirectories
os.chdir(path)
EXT = "test_results.csv"  # Name of the files containing test results
csv_files = [file
             for path, subdir, files in os.walk(path)
             for file in glob(os.path.join(path, EXT))]
print(f"Loaded {len(csv_files)} csv files.")

# All possible charts IDs
chart_ids = ["b_wn", "bm", "by", "c_wn", "cg", "cr", "g_wn", "gc", "gm", "m_wn", "mb", "mg", "r_wn", "rc", "ry",
             "y_wn", "yb", "yr"]
rows_number = len(chart_ids)

extracted_results = {}  # Lists of all the extracted results from the CSVs, one list for each chart
for chart_id in chart_ids:
    extracted_results[chart_id] = []

# Set the header of the output CSV file to contain the user id taken from user_details.txt file
output_header = []
output_header.append("chart_id")

# Iterate through CSV files
for csv_path in csv_files:
    actual_csv_rows = {}
    user_details_file = os.path.dirname(csv_path) + "\\user_details.txt"
    user_nickname = ""
    with open(user_details_file, mode='r') as user_details:
        for line in user_details:
            if USER_ID in line:
                user_nickname = (line.split(USER_ID, 1)[1]).strip()
                output_header.append(user_nickname)
                break
    with open(csv_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 1
        for row in csv_reader:
            # hsl_dists[row["chart_id"]].append(row["hsl_dist"])
            deltaE = CIEDE2000(RGB2Lab.rgb2lab(RGB2Lab, row["actual_color"]),
                               RGB2Lab.rgb2lab(RGB2Lab, row["picked_color"]))
            actual_csv_rows[row["chart_id"]] = deltaE
            line_count += 1
        print(f'User "{user_nickname}": processed {line_count - 1}/{rows_number} lines of file {csv_path}.')
    for chart_id in chart_ids:
        if chart_id in actual_csv_rows:
            extracted_results[chart_id].append(actual_csv_rows[chart_id])
        else:
            extracted_results[chart_id].append("n/a")

tests_number = len(csv_files)

output_rows = []
for chart_id in chart_ids:
    row_array = [chart_id]
    row_array += extracted_results[chart_id]
    output_rows.append(row_array)

with open(path + '\\merged_results__CIEDE2000.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(output_header)
    writer.writerows(output_rows)
