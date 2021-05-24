import csv
from ColorUtils.RGB2Lab import RGB2Lab
from ColorUtils.ciede2000 import CIEDE2000

USER_ID = "user_nickname:"  # String in user_details.txt followed by user_id


#
#
#
#   PARSE TESTS GROUPED BY CHART
#
def by_chart(CSVs, chart_ids, column_to_extract, verbose=False, ignore_na=True):
    rows_number = len(chart_ids)

    extracted_results = {}  # Lists of all the extracted results from the CSVs, one list for each chart
    for chart_id in chart_ids:
        extracted_results[chart_id] = []

    # Iterate through CSV files
    for user_id in CSVs:
        skip_user = False
        csv_path = CSVs[user_id]
        if verbose:
            print(f"CSV_PATH:{csv_path}")
        actual_csv_rows = {}

        with open(csv_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 1
            for row in csv_reader:
                if column_to_extract == "delta_e":
                    val = CIEDE2000(RGB2Lab.rgb2lab(RGB2Lab, row["actual_color"]),
                                    RGB2Lab.rgb2lab(RGB2Lab, row["picked_color"]))
                else:
                    val = row[column_to_extract]
                actual_csv_rows[row["chart_id"]] = val
                line_count += 1
            if verbose:
                print(f'User "{user_id}": processed {line_count - 1}/{rows_number} lines of file {csv_path}.')

        for chart_id in chart_ids:
            if chart_id not in actual_csv_rows and ignore_na:
                skip_user = True
                continue
        if skip_user:
            print(f"User '{user_id}' skipped: one or more 'n/a' values found")
            continue

        for chart_id in chart_ids:
            if chart_id in actual_csv_rows:
                extracted_results[chart_id].append(float(actual_csv_rows[chart_id]))
            else:
                extracted_results[chart_id].append("n/a")

    return extracted_results


#
#
#
#   PARSE TESTS GROUPED BY USER
#
def by_user(CSVs, chart_ids, column_to_extract, verbose=False, ignore_na=True):
    rows_number = len(chart_ids)

    extracted_results = {}  # Lists of all the extracted results from the CSVs, one list for each chart

    user_list = []

    # Iterate through CSV files
    for user_id in CSVs:
        skip_user = False
        user_list.append(user_id)
        extracted_results[user_id] = []

        csv_path = CSVs[user_id]
        if verbose:
            print(f"CSV_PATH:{csv_path}")
        actual_csv_rows = {}

        with open(csv_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 1
            for row in csv_reader:
                if column_to_extract == "delta_e":
                    val = CIEDE2000(RGB2Lab.rgb2lab(RGB2Lab, row["actual_color"]),
                                    RGB2Lab.rgb2lab(RGB2Lab, row["picked_color"]))
                else:
                    val = row[column_to_extract]
                actual_csv_rows[row["chart_id"]] = val
                line_count += 1
            if verbose:
                print(f'User "{user_id}": processed {line_count - 1}/{rows_number} lines of file {csv_path}.')

        for chart_id in chart_ids:
            if chart_id not in actual_csv_rows and ignore_na:
                skip_user = True
                continue
        if skip_user:
            extracted_results.pop(user_id)
            print(f"User '{user_id}' skipped: one or more 'n/a' values found")
            continue

        for chart_id in chart_ids:
            if chart_id in actual_csv_rows:
                extracted_results[user_id].append(float(actual_csv_rows[chart_id]))
            else:
                extracted_results[user_id].append("n/a")

    return user_list, extracted_results


#
#
#
#   PARSE TESTS a AND b VALUES GROUPED BY CHART
#
def get_picked_lab(CSVs, chart_ids, verbose=False, ignore_na=True):
    rows_number = len(chart_ids)

    extracted_results = {}  # Lists of all the extracted results from the CSVs, one list for each chart
    for chart_id in chart_ids:
        extracted_results[chart_id] = []

    # Iterate through CSV files
    for user_id in CSVs:
        skip_user = False
        csv_path = CSVs[user_id]
        if verbose:
            print(f"CSV_PATH:{csv_path}")
        actual_csv_rows = {}

        with open(csv_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 1
            for row in csv_reader:
                actual_csv_rows[row["chart_id"]] = RGB2Lab.rgb2lab(RGB2Lab, row["picked_color"])
                line_count += 1
            if verbose:
                print(f'User "{user_id}": processed {line_count - 1}/{rows_number} lines of file {csv_path}.')
        for chart_id in chart_ids:
            if chart_id not in actual_csv_rows and ignore_na:
                skip_user = True
                continue
        if skip_user:
            print(f"User '{user_id}' skipped: one or more 'n/a' values found")
            continue
        for chart_id in chart_ids:
            if chart_id in actual_csv_rows:
                extracted_results[chart_id].append(actual_csv_rows[chart_id])
            else:
                extracted_results[chart_id].append("n/a")

    return extracted_results