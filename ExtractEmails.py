import csv
import os
from glob import glob

USER_EMAIL = "user_email_address:"  # String in user_details.txt followed by user email

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

email_addresses = []

# Iterate through test results
for csv_path in csv_files:
    actual_csv_rows = {}
    user_details_file = os.path.dirname(csv_path) + "\\user_details.txt"
    user_nickname = ""
    with open(user_details_file, mode='r') as user_details:
        for line in user_details:
            if USER_EMAIL in line:
                user_nickname = (line.split(USER_EMAIL, 1)[1]).strip()
                email_addresses.append(user_nickname)
                break

print(f"{len(email_addresses)} email addresses found")

with open(path + "\email_addresses.txt", "w") as txt_file:
    for line in email_addresses:
        txt_file.write(line + "\n")
