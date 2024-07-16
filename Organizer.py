import os
from distutils.dir_util import copy_tree
from glob import glob
from os.path import normpath, basename

ORGANIZE_BY = ["user_is_colorblind:", "user_gender:", "user_works_with_colors:"]
USER_ID = "user_nickname:"  # String in user_details.txt that determine user_id

# Choose an existing folder where to look for the CSVs
path = input("Enter the path of the directory: ")
if len(path) == 0:
    path = '.'
assert os.path.exists(path), "I did not find the file at " + str(path)

# Look recursively for the CSVs in directory and subdirectories
os.chdir(path)
EXT = "test_results.csv"    # Name of the files containing test results
csv_files = [file
             for path, subdir, files in os.walk(path)
             for file in glob(os.path.join(path, EXT))]
print(f"Loaded {len(csv_files)} csv files.")

print("\nOrganize data by:")
i = 0
while i < len(ORGANIZE_BY):
    print(f"\t[{i}] {ORGANIZE_BY[i]}")
    i += 1
organize_by = -1
while organize_by < 0 or organize_by > len(ORGANIZE_BY):
    organize_by = int(input("select: "))

# Iterate through CSV files
for csv_path in csv_files:
    actual_csv_rows = {}
    user_details_file = os.path.dirname(csv_path) + "/user_details.txt"
    is_colorblind = ""
    user_id = ""
    found_strings = 0
    with open(user_details_file, mode='r') as user_details:
        for line in user_details:
            if ORGANIZE_BY[organize_by] in line:
                is_colorblind = (line.split(ORGANIZE_BY[organize_by], 1)[1]).strip()
                found_strings += 1
            elif USER_ID in line:
                user_id = (line.split(USER_ID, 1)[1]).strip()
                found_strings += 1
            if found_strings == 2:
                break
    new_path = os.path.join(path, f"{ORGANIZE_BY[organize_by][:-1]}__{is_colorblind.upper()}")
    print(f'Copying "{basename(normpath(os.path.dirname(csv_path)))}" to {new_path}')
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    copy_tree(os.path.dirname(csv_path), os.path.join(new_path,user_id+"__"+(basename(normpath(os.path.dirname(csv_path))))))