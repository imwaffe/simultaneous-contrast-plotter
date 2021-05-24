import os
from glob import glob
from os.path import normpath, basename

USER_ID = "user_nickname:"  # String in user_details.txt that determine user_id


def GETCSVs(path, organize_by, min_rows=-1, verbose=False):
    CSVs = {}

    if len(path) == 0:
        path = '.'
    assert os.path.exists(path), "I did not find the file at " + str(path)

    # Look recursively for the CSVs in directory and subdirectories
    os.chdir(path)
    EXT = "test_results.csv"  # Name of the files containing test results
    csv_files = [file
                 for path, subdir, files in os.walk(path)
                 for file in glob(os.path.join(path, EXT))]

    if verbose:
        print(f"OrganizeTests:\tLoaded {len(csv_files)} csv files.")

    # Iterate through CSV files
    for csv_path in csv_files:
        file = open(csv_path)
        row_count = len(file.readlines())-1
        if min_rows > 0 and row_count < min_rows:
            if verbose:
                print(f'SKIPPED "{basename(normpath(os.path.dirname(csv_path)))}", {row_count} rows')
            continue
        user_details_file = os.path.dirname(csv_path) + "\\user_details.txt"
        organize_value = ""
        user_id = ""
        found_strings = 0
        with open(user_details_file, mode='r') as user_details:
            for line in user_details:
                if organize_by in line:
                    organize_value = (line.split(organize_by, 1)[1]).strip()
                    found_strings += 1
                elif USER_ID in line:
                    user_id = (line.split(USER_ID, 1)[1]).strip()
                    found_strings += 1
                if found_strings == 2:
                    break
        if organize_value not in CSVs:
            CSVs[organize_value] = {}
        original_user_id = user_id
        progressive = 1
        while user_id in CSVs[organize_value]:
            user_id = original_user_id+"_"+str(progressive)
            progressive += 1

        if verbose:
            print(f'LOADED "{basename(normpath(os.path.dirname(csv_path)))}" by user "{user_id}", {organize_by}:{organize_value}, {row_count} ROWS')

        CSVs[organize_value][user_id] = csv_path

    return CSVs
