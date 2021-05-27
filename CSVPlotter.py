import os

import gc
import matplotlib.pyplot as plt

from Parsing.OrganizeTests import GETCSVs
from Parsing.ParseTests import get_picked_lab, by_user, by_chart
from Plotting.PlotLab import plot_three_charts as plot_ab
from Plotting.PlotCharts import  plots_group as plot_charts
from Plotting.Plotter import plot_style_1 as plotter_1

PARAMETERS_LIST = {
    "delta_e": "ΔE* CIEDE 2000 (sRGB, D65)",
    "hsl_dist": "HSL euclidean distance",
    "rgb_dist": "RGB euclidean distance",
    "hue_dist": "Hue distance",
    "saturation_dist": "Saturation distance",
    "luma_dist": "Lightness distance"
}
CHARTIDS = ["b_wn", "bm", "by", "c_wn", "cg", "cr", "g_wn", "gc", "gm", "m_wn", "mb", "mg", "r_wn", "rc", "ry",
            "y_wn", "yb", "yr"]

LABEL_1 = "colorblinds"
LABEL_2 = "non colorblinds"
GROUP_1_ANSWER = "yes"
GROUP_2_ANSWER = "no"
ORGANIZE_BY = "user_is_colorblind:"

def merge_data(dict_1, dict_2):
    for id in dict_1:
        for val in dict_2[id]:
            dict_1[id].append(val)
    return dict_1


test_results_path = input("Path of directory containing test results: ")
if len(test_results_path) == 0:
    test_results_path = '.'
assert os.path.exists(test_results_path), "I couldn't find the directory " + str(test_results_path)
csvs = GETCSVs(test_results_path, ORGANIZE_BY, min_rows=len(CHARTIDS), verbose=True)

saved_data_path = input("\nPath of directory where to save plots: ")
saved_data_path = os.path.join(saved_data_path, "Plots")

for parameter in PARAMETERS_LIST:
    print(f"Extracting {PARAMETERS_LIST[parameter]} from CSVs")
    (group_1, parsed_group_1) = by_user(csvs[GROUP_1_ANSWER], CHARTIDS, column_to_extract=parameter)
    (unsures, parsed_unsure) = by_user(csvs["unsure"], CHARTIDS, column_to_extract=parameter)
    (group_2, parsed_group_2) = by_user(csvs[GROUP_2_ANSWER], CHARTIDS, column_to_extract=parameter)

    path = os.path.join(os.path.join(saved_data_path, "by_user_grouped"), parameter)

    parsed_group_1 = {**parsed_group_1, **parsed_unsure}

    fig = plt.figure(dpi=300, figsize=(8.27, 11.69))
    for i in range(0, 6):
        print("\tPlotting charts " + (",").join(CHARTIDS[i * 3:(i + 1) * 3]) + "...")
        fig, plt = plot_charts(
            dict_1=parsed_group_1,
            dict_2=parsed_group_2,
            column_keys=CHARTIDS,
            sup_title=PARAMETERS_LIST[parameter],
            fig=fig,
            truncate=6,
            use_columns=CHARTIDS[i * 3:(i + 1) * 3],
            dpi=300,
            sort=True,
            label_1=LABEL_1,
            label_2=LABEL_2,
            columns=1
        )
        plt.tight_layout()
        filename = os.path.join(path, f"chart " + (",").join(CHARTIDS[i * 3:(i + 1) * 3]) + ".png")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        print(f"\t\tSaving plots to {filename}...")
        plt.savefig(filename)
        print("\t\tPlots saved successfully!")
        # plt.show()
    plt.close(fig=fig)
    fig.clf()
    gc.collect()

for parameter in PARAMETERS_LIST:
    print(f"Extracting {PARAMETERS_LIST[parameter]} from CSVs")
    (group_1, parsed_group_1) = by_user(csvs[GROUP_1_ANSWER], CHARTIDS, column_to_extract=parameter)
    (unsures, parsed_unsure) = by_user(csvs["unsure"], CHARTIDS, column_to_extract=parameter)
    (group_2, parsed_group_2) = by_user(csvs[GROUP_2_ANSWER], CHARTIDS, column_to_extract=parameter)

    path = os.path.join(os.path.join(saved_data_path, "by_user"), parameter)

    parsed_group_1 = {**parsed_group_1, **parsed_unsure}

    fig = plt.figure(dpi=300, figsize=(8.27, 11.69))
    for i in range(0, 6):
        print("\tPlotting charts " + (",").join(CHARTIDS[i * 3:(i + 1) * 3]) + "...")
        fig, plt = plot_charts(
            dict_1=parsed_group_1,
            dict_2=parsed_group_2,
            column_keys=CHARTIDS,
            sup_title=PARAMETERS_LIST[parameter],
            fig=fig,
            truncate=6,
            use_columns=CHARTIDS[i * 3:(i + 1) * 3],
            dpi=300,
            sort=True,
            label_1=LABEL_1,
            label_2=LABEL_2,
            columns=2
        )
        plt.tight_layout()
        filename = os.path.join(path, f"charts " + (",").join(CHARTIDS[i * 3:(i + 1) * 3]) + ".png")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        print(f"\t\tSaving plots to {filename}...")
        plt.savefig(filename)
        print("\t\tPlots saved successfully!")
        # plt.show()
    plt.close(fig=fig)
    fig.clf()
    gc.collect()

fig = plt.figure(dpi=300, figsize=(8.27, 11.69))
path = os.path.join(saved_data_path, "by_chart")
for parameter in PARAMETERS_LIST:
    print(f"Extracting {PARAMETERS_LIST[parameter]} from CSVs")
    parsed_group_1 = by_chart(csvs[GROUP_1_ANSWER], CHARTIDS, column_to_extract=parameter)
    parsed_unsure = by_chart(csvs["unsure"], CHARTIDS, column_to_extract=parameter)
    parsed_group_2 = by_chart(csvs[GROUP_2_ANSWER], CHARTIDS, column_to_extract=parameter)
    parsed_group_1 = merge_data(parsed_group_1, parsed_unsure)

    plt = plotter_1(
        data_1=parsed_group_1,
        label_1=LABEL_1,
        data_2=parsed_group_2,
        label_2=LABEL_2,
        x_labels=CHARTIDS,
        fig=fig,
        sup_title=PARAMETERS_LIST[parameter]
    )
    plt.tight_layout()
    filename = os.path.join(path, f"{parameter}.png")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    print(f"\t\tSaving plots to {filename}...")
    plt.savefig(filename)
    print("\t\tPlots saved successfully!")
    # plt.show()
plt.close(fig=fig)
fig.clf()
gc.collect()

picked_lab_group_1 = get_picked_lab(csvs[GROUP_1_ANSWER], CHARTIDS)
picked_lab_unsure = get_picked_lab(csvs["unsure"], CHARTIDS)
picked_lab_group_2 = get_picked_lab(csvs[GROUP_2_ANSWER], CHARTIDS)
picked_lab_group_1 = merge_data(picked_lab_group_1, picked_lab_unsure)
path = os.path.join(saved_data_path, "ab_scatter_plots")
fig = plt.figure(dpi=300, figsize=(8.27, 11.69))
for i in range(0, 6):
    print("Plotting ab scatter plots for charts " + (",").join(CHARTIDS[i * 3:(i + 1) * 3]))
    plt = plot_ab(
        data_1=picked_lab_group_1,
        label_1=LABEL_1,
        data_2=picked_lab_group_2,
        label_2=LABEL_2,
        fig=fig,
        charts_to_plot=CHARTIDS[i * 3:(i + 1) * 3],
        sup_title="a*b* scatter (sRGB, D65)"
    )
    filename = os.path.join(path, f"charts " + (",").join(CHARTIDS[i * 3:(i + 1) * 3]) + ".png")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    print(f"\t\tSaving plots to {filename}...")
    plt.savefig(filename)
    print("\t\tPlots saved successfully!")
plt.close(fig=fig)
fig.clf()
gc.collect()
