import csv
import os
from glob import glob

from ColorUtils.RGB2Lab import rgb2xyz

USER_ID = "user_nickname:"  # String in user_details.txt followed by user_id
IS_COLORBLIND = "user_is_colorblind:"
DEST_FOLDER = "xyY_values"


def get_chromaticity(xyz_array):
    output = {"x": xyz_array[0][0] / (xyz_array[0][0] + xyz_array[1][0] + xyz_array[2][0]),
              "y": xyz_array[1][0] / (xyz_array[0][0] + xyz_array[1][0] + xyz_array[2][0]),
              "Y": xyz_array[1][0]*100}
    return output


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

# Choose the column to extract
column_to_extract = "picked_color"

# All possible charts IDs
chart_ids = ["b_wn", "bm", "by", "c_wn", "cg", "cr", "g_wn", "gc", "gm", "m_wn", "mb", "mg", "r_wn", "rc", "ry",
             "y_wn", "yb", "yr"]
rows_number = len(chart_ids)

extracted_results = {}  # Lists of all the extracted results from the CSVs, one list for each chart
for chart_id in chart_ids:
    extracted_results[chart_id] = {}

# Set the header of the output CSV file to contain the user id taken from user_details.txt file
users = []
incomplete_users = []
colorblinds = {}

# Iterate through CSV files
for csv_path in csv_files:
    actual_csv_rows = {}
    user_details_file = os.path.dirname(csv_path) + "\\user_details.txt"
    user_nickname = ""
    user_colorblind = False
    with open(user_details_file, mode='r') as user_details:
        for line in user_details:
            if USER_ID in line:
                user_nickname = (line.split(USER_ID, 1)[1]).strip()
                users.append(user_nickname)
            if IS_COLORBLIND in line:
                colorblind_ans = (line.split(IS_COLORBLIND, 1)[1]).strip()
                user_colorblind = not (colorblind_ans == "no")
                colorblinds[user_nickname] = user_colorblind
    with open(csv_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 1
        for row in csv_reader:
            # hsl_dists[row["chart_id"]].append(row["hsl_dist"])
            actual_csv_rows[row["chart_id"]] = row[column_to_extract]
            line_count += 1
        print(f'User "{user_nickname}": processed {line_count - 1}/{rows_number} lines of file {csv_path}.')
    for chart_id in chart_ids:
        if chart_id in actual_csv_rows:
            extracted_results[chart_id][user_nickname] = actual_csv_rows[chart_id]
        else:
            extracted_results[chart_id][user_nickname] = "n/a"
            incomplete_users.append(user_nickname)
            break

for chart_id in chart_ids:
    output_rows = []
    for user in users:
        if user not in incomplete_users:
            xyz = rgb2xyz(extracted_results[chart_id][user])
            xyY = get_chromaticity(xyz)
            row_array = [f"user_{(users.index(user))}", colorblinds[user], xyY["x"], xyY["y"], xyY["Y"]]
            output_rows.append(row_array)
    filename = os.path.join(path, DEST_FOLDER, f"{chart_id}.csv")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["user", "is_colorblind", "x", "y", "Y"])
        writer.writerows(output_rows)

colors_csv_rows = [["chart_id", "file_path", "target_x", "target_y", "target_Y"]]
with open(os.path.join(path, "colors.csv"), mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 1
    for row in csv_reader:
        filepath = os.path.join(DEST_FOLDER, f"{row['chart_id']}.csv")
        assert os.path.exists(os.path.join(path, filepath))
        xyz = rgb2xyz(row["first_foreground"])
        xyY = get_chromaticity(xyz)
        colors_csv_rows.append([
            row["chart_id"],
            filepath,
            xyY["x"], xyY["y"], xyY["Y"]
        ])

filename = os.path.join(path, "CHARTS.csv")
with open(filename, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(colors_csv_rows)
