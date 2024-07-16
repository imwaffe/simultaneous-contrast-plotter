import csv
import os
from pprint import pprint

import numpy as np
# from colour import models
# from colour import plotting as xy

import gc
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from ColorUtils.RGB2HSL import RGB2HSL
from ColorUtils import RGB2Lab, ciede2000
from ColorUtils.ciede2000 import CIEDE2000
from Parsing.OrganizeTests import GETCSVs
from Parsing.ParseTests import get_derived, by_user, by_chart
from Plotting import Plots
from Plotting.PlotLab import plot_three_charts as plot_scatter
from Plotting.PlotCharts import plots_group as plot_charts
from Plotting.PlotVectors import plot_three_charts as plot_vect
from Plotting.Plotter import plot_style_1_PAPER as plotter_1
from Plotting.Plotter import plot_style_2 as plotter_2
from scipy.spatial import distance
from PIL import Image, ImageDraw

from Draws.DrawBox import DrawBox
from Draws.DrawGrid import DrawGrid

COLOR_1 = "#2C7BB6"
COLOR_2 = "#ebba34"

PARAMETERS_LIST = {
    "delta_e": "ΔE* (sRGB, D65)",
    "hsl_dist": "HSL euclidean distance",
    "rgb_dist": "RGB euclidean distance",
    "hue_dist": "Hue distance",
    "saturation_dist": "Saturation distance",
    "luma_dist": "Lightness distance"
}
START_TO_PICKED = {
    "h": "HUE |picked-start|",
    "s": "SATURATION |picked-start|",
    "l": "LIGHTNESS |picked-start|"
}
# CHARTIDS = ["b_wn", "bm", "by", "c_wn", "cg", "cr", "g_wn", "gc", "gm", "m_wn", "mb", "mg", "r_wn", "ry", "rc",
#            "y_wn", "yr", "yb"]

CHARTIDS = ["bm", "by", "cg", "cr", "gc", "gm", "mb", "mg", "ry", "rc", "yr", "yb"]
CHARTIDS_BY_BG = ["by", "yb", "gm", "mg", "ry", "yr", "bm", "mb", "rc", "cr", "gc", "cg"]

# CHARTIDS = ["mg-m", "gm-wn_m", "gm-g_wn", "mg-wn_g"]

# CHARTIDS = ["gm-g_wn", "mg-wn_g", "gm_big", "mg-m_wn", "mg_small", "gm_small", "gm-wn_m", "mg_big"]
# CHARTIDS_BY_BG = ["gm-g_wn", "mg-wn_g", "mg-m_wn", "gm-wn_m", "gm_big", "mg_big", "mg_small", "gm_small"]

GROUP_EACH_STD = 2
GROUP_EACH_PAIRS = 1

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

target_colors = {}
start_colors = {}
context_colors = {}

with open(os.path.join(test_results_path, "colors.csv"), mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if 'second_background' in row:
            if row['second_background'] == 'wn':
                target_colors[row['chart_id']] = row['first_foreground']
                start_colors[row['chart_id']] = row['second_foreground']
                context_colors[row['chart_id']] = row['background_color']
            elif row['second_foreground'] == 'wn':
                target_colors[row['chart_id']] = row['background_color']
                start_colors[row['chart_id']] = row['second_background']
                context_colors[row['chart_id']] = row['first_foreground']
        else:
            target_colors[row['chart_id']] = row['first_foreground']
            start_colors[row['chart_id']] = row['second_foreground']
            context_colors[row['chart_id']] = row['background_color']


def by_user_stats(parameter, chart_ids, csvs):
    sort = True
    global plt
    print(f"Extracting {PARAMETERS_LIST[parameter]} from CSVs")
    (group_1, parsed_group_1) = by_user(csvs[GROUP_1_ANSWER], chart_ids, column_to_extract=parameter)
    if "unsure" in csvs:
        (unsures, parsed_unsure) = by_user(csvs["unsure"], chart_ids, column_to_extract=parameter)
    (group_2, parsed_group_2) = by_user(csvs[GROUP_2_ANSWER], chart_ids, column_to_extract=parameter)

    data_dir_name = "by_user_grouped"
    if not sort:
        data_dir_name += "_UNSORTED"
    path = os.path.join(os.path.join(saved_data_path, data_dir_name), parameter)

    if "unsure" in csvs:
        parsed_group_1 = {**parsed_group_1, **parsed_unsure}

    dict_1_fake_usernames = {}
    dict_2_fake_usernames = {}
    i = 1
    for user in parsed_group_1:
        dict_1_fake_usernames[f"cdo#{i}"] = parsed_group_1[user]
        i += 1
    i = 1
    for user in parsed_group_2:
        dict_2_fake_usernames[f"nco#{i}"] = parsed_group_2[user]
        i += 1
    for i in range(0, int(len(chart_ids) / 3)):
        print("\tPlotting charts " + (",").join(chart_ids[i * 3:(i + 1) * 3]) + "...")
        fig = plt.figure(dpi=300, figsize=(8.27, 11.69))
        fig, plt = plot_charts(
            dict_1=dict_1_fake_usernames,
            dict_2=dict_2_fake_usernames,
            column_keys=chart_ids,
            sup_title=PARAMETERS_LIST[parameter],
            fig=fig,
            truncate=6,
            use_columns=chart_ids[i * 3:(i + 1) * 3],
            dpi=300,
            sort=sort,
            label_1=LABEL_1,
            label_2=LABEL_2,
            columns=2,
            max_y_user=30
        )
        plt.tight_layout()
        # plt.pause(0.3)
        # plt.show(block=False)
        filename = os.path.join(path, f"chart " + (",").join(CHARTIDS[i * 3:(i + 1) * 3]) + ".pdf")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        print(f"\t\tSaving plots to {filename}...")
        plt.savefig(filename)
        print("\t\tPlots saved successfully!")
    # plt.show()
    # plt.close(fig=fig)
    # fig.clf()
    gc.collect()


#
# for parameter in PARAMETERS_LIST:
#     print(f"Extracting {PARAMETERS_LIST[parameter]} from CSVs")
#     (group_1, parsed_group_1) = by_user(csvs[GROUP_1_ANSWER], CHARTIDS, column_to_extract=parameter)
#     if "unsure" in csvs:
#         (unsures, parsed_unsure) = by_user(csvs["unsure"], CHARTIDS, column_to_extract=parameter)
#     (group_2, parsed_group_2) = by_user(csvs[GROUP_2_ANSWER], CHARTIDS, column_to_extract=parameter)
#
#     path = os.path.join(os.path.join(saved_data_path, "by_user"), parameter)
#
#     if "unsure" in csvs:
#         parsed_group_1 = {**parsed_group_1, **parsed_unsure}
#
#     fig = plt.figure(dpi=300, figsize=(8.27, 11.69))
#     for i in range(0, 6):
#         print("\tPlotting charts " + (",").join(CHARTIDS[i * 3:(i + 1) * 3]) + "...")
#         fig, plt = plot_charts(
#             dict_1=parsed_group_1,
#             dict_2=parsed_group_2,
#             column_keys=CHARTIDS,
#             sup_title=PARAMETERS_LIST[parameter],
#             fig=fig,
#             truncate=6,
#             use_columns=CHARTIDS[i * 3:(i + 1) * 3],
#             dpi=300,
#             sort=True,
#             label_1=LABEL_1,
#             label_2=LABEL_2,
#             columns=2
#         )
#         plt.tight_layout()
#         filename = os.path.join(path, f"charts " + (",").join(CHARTIDS[i * 3:(i + 1) * 3]) + ".pdf")
#         os.makedirs(os.path.dirname(filename), exist_ok=True)
#         print(f"\t\tSaving plots to {filename}...")
#         plt.savefig(filename)
#         print("\t\tPlots saved successfully!")
#         # plt.show()
#     plt.close(fig=fig)
#     fig.clf()
#     gc.collect()
#
def global_stats(parameter, chart_ids, csvs):
    global plt, target_colors
    fig = plt.figure(dpi=72, figsize=(6, 9))
    path = os.path.join(saved_data_path, "by_chart")
    print(f"Extracting {PARAMETERS_LIST[parameter]} from CSVs")
    parsed_group_1 = by_chart(csvs[GROUP_1_ANSWER], chart_ids, column_to_extract=parameter)
    if "unsure" in csvs:
        parsed_unsure = by_chart(csvs["unsure"], chart_ids, column_to_extract=parameter)
    parsed_group_2 = by_chart(csvs[GROUP_2_ANSWER], chart_ids, column_to_extract=parameter)
    if "unsure" in csvs:
        parsed_group_1 = merge_data(parsed_group_1, parsed_unsure)

    target_lab = {}
    start_lab = {}
    for chart_id in chart_ids:
        target_lab[chart_id] = RGB2Lab.rgb2lab(target_colors[chart_id])
        start_lab[chart_id] = RGB2Lab.rgb2lab(start_colors[chart_id])
    delta_e_start = []
    single_patches = []
    for chart_id in chart_ids:
        if chart_id[0] not in single_patches:
            single_patches.append(chart_id[0])
            delta_e_start.append(CIEDE2000(target_lab[chart_id], start_lab[chart_id]))

    plt = plotter_1(
        data_1=parsed_group_1,
        label_1=LABEL_1,
        data_2=parsed_group_2,
        label_2=LABEL_2,
        hlines=delta_e_start,
        label_3="starting color",
        x_labels=chart_ids,
        xlabel="chart ids",
        ylabel1="ΔE*",
        ylabel2="median ΔE*",
        fig=fig,
        sup_title=PARAMETERS_LIST[parameter],
        group_each=GROUP_EACH_STD
    )
    plt.tight_layout()
    filename = os.path.join(path, f"{parameter}.pdf")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    print(f"\t\tSaving plots to {filename}...")
    plt.savefig(filename)
    print("\t\tPlots saved successfully!")
    plt.pause(0.1)
    plt.show(block=False)
    # plt.close(fig=fig)
    # fig.clf()
    gc.collect()


def start_vs_picked(parameter, chart_ids, csvs):
    global plt
    print(f"Extracting {START_TO_PICKED[parameter]} from CSVs")
    (group_1, rgb_group_1) = by_user(csvs[GROUP_1_ANSWER], chart_ids, column_to_extract="picked_color")
    (group_unsure, rgb_group_unsure) = by_user(csvs[GROUP_1_ANSWER], chart_ids, column_to_extract="picked_color")
    (group_2, rgb_group_2) = by_user(csvs[GROUP_2_ANSWER], chart_ids, column_to_extract="picked_color")
    rgb_group_1 = {**rgb_group_1, **rgb_group_unsure}
    parsed_group_1 = {}
    parsed_group_2 = {}

    for user in rgb_group_1:
        parsed_group_1[user] = []
        for i in range(0, len(chart_ids)):
            hsl_start = RGB2HSL(target_colors[chart_ids[i]])
            hsl_picked = RGB2HSL(rgb_group_1[user][i])
            parsed_group_1[user].append(abs(hsl_start[parameter] - hsl_picked[parameter]))
    for user in rgb_group_2:
        parsed_group_2[user] = []
        for i in range(0, len(chart_ids)):
            hsl_start = RGB2HSL(target_colors[chart_ids[i]])
            hsl_picked = RGB2HSL(rgb_group_2[user][i])
            parsed_group_2[user].append(abs(hsl_start[parameter] - hsl_picked[parameter]))

    path = os.path.join(os.path.join(saved_data_path, "picked_vs_starting_color"), parameter)

    for i in range(0, 6):
        print("\tPlotting charts " + (",").join(chart_ids[i * 3:(i + 1) * 3]) + "...")
        fig = plt.figure(dpi=72, figsize=(8.27, 11.69))
        fig, plt = plot_charts(
            dict_1=parsed_group_1,
            dict_2=parsed_group_2,
            column_keys=chart_ids,
            sup_title=START_TO_PICKED[parameter],
            fig=fig,
            truncate=6,
            use_columns=chart_ids[i * 3:(i + 1) * 3],
            dpi=300,
            sort=True,
            label_1=LABEL_1,
            label_2=LABEL_2,
            columns=1
        )
        plt.tight_layout()
        # filename = os.path.join(path, f"chart " + (",").join(chart_ids[i * 3:(i + 1) * 3]) + ".pdf")
        # os.makedirs(os.path.dirname(filename), exist_ok=True)
        # print(f"\t\tSaving plots to {filename}...")
        # plt.savefig(filename)
        # print("\t\tPlots saved successfully!")
        plt.pause(0.3)
        plt.show(block=False)
    # plt.close(fig=fig)
    # fig.clf()
    gc.collect()


def plot_iqr(parameter, chart_ids, csvs):
    global plt
    fig = plt.figure(dpi=72, figsize=(8.27, 11.69))
    path = os.path.join(saved_data_path, "iqr")
    print(f"Extracting {PARAMETERS_LIST[parameter]} from CSVs")
    parsed_group_1 = by_chart(csvs[GROUP_1_ANSWER], chart_ids, column_to_extract=parameter)
    if "unsure" in csvs:
        parsed_unsure = by_chart(csvs["unsure"], chart_ids, column_to_extract=parameter)
    parsed_group_2 = by_chart(csvs[GROUP_2_ANSWER], chart_ids, column_to_extract=parameter)
    if "unsure" in csvs:
        merged_data = merge_data(merge_data(parsed_group_1, parsed_unsure), parsed_group_2)

    plt = plotter_2(
        data=parsed_group_2,
        x_labels=chart_ids,
        fig=fig,
        sup_title="non colorblinds: " + PARAMETERS_LIST[parameter],
        group_each=1,
        color="#ebba34"
    )
    plt.tight_layout()
    plt.pause(0.1)
    plt.show(block=False)
    # filename = os.path.join(path, f"{parameter}.pdf")
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    # print(f"\t\tSaving plots to {filename}...")
    # plt.savefig(filename)
    # print("\t\tPlots saved successfully!")
    # plt.close(fig=fig)
    # fig.clf()
    gc.collect()


#
#
# CONVERSION_FUNCTION = RGB2Lab.rgb2lab
# picked_lab_group_1 = get_derived(csvs[GROUP_1_ANSWER], CHARTIDS, "picked_color", func=CONVERSION_FUNCTION)
# if "unsure" in csvs:
#     picked_lab_unsure = get_derived(csvs["unsure"], CHARTIDS, "picked_color", func=CONVERSION_FUNCTION)
# picked_lab_group_2 = get_derived(csvs[GROUP_2_ANSWER], CHARTIDS, "picked_color", func=CONVERSION_FUNCTION)
# if "unsure" in csvs:
#     picked_lab_group_1 = merge_data(picked_lab_group_1, picked_lab_unsure)
# path = os.path.join(saved_data_path, "ab_vectors")
# fig = plt.figure(dpi=300, figsize=(8, 25))
# target_xyz = {}
# for chartid in target_colors:
#     target_xyz[chartid] = CONVERSION_FUNCTION(target_colors[chartid])
# for i in range(0, 6):
#     gs = GridSpec(3, 1, figure=fig)
#     axes = []
#     for row in range(0, 3):
#         axes.append(plt.subplot(gs[row, 0]))
#     print("Plotting xy error for charts " + (",").join(CHARTIDS[i * 3:(i + 1) * 3]))
#     plot_vect(
#         data_1=picked_lab_group_1,
#         label_1=LABEL_1,
#         data_2=picked_lab_group_2,
#         label_2=LABEL_2,
#         data_0=target_xyz,
#         ylabel='b*',
#         xlabel='a*',
#         label_0="target color",
#         fig=fig,
#         axes=axes,
#         charts_to_plot=CHARTIDS[i * 3:(i + 1) * 3],
#     )
#     plot_ab(
#         data_1=picked_lab_group_1,
#         label_1=LABEL_1,
#         data_2=picked_lab_group_2,
#         label_2=LABEL_2,
#         fig=fig,
#         axes=axes,
#         charts_to_plot=CHARTIDS[i * 3:(i + 1) * 3],
#         sup_title="a*b* scatter (sRGB, D65)"
#     )
#     filename = os.path.join(path, f"charts " + (",").join(CHARTIDS[i * 3:(i + 1) * 3]) + ".pdf")
#     os.makedirs(os.path.dirname(filename), exist_ok=True)
#     print(f"\t\tSaving plots to {filename}...")
#     plt.savefig(filename)
#     print("\t\tPlots saved successfully!")
# plt.close(fig=fig)
# fig.clf()
# gc.collect()


def by_chart_compl(parameter, chart_ids, csvs):
    global plt
    fig = plt.figure(dpi=72, figsize=(8.27, 11.69))
    path = os.path.join(saved_data_path, "by_chart_compl")
    print(f"Extracting {PARAMETERS_LIST[parameter]} from CSVs")
    parsed_group_1 = by_chart(csvs[GROUP_1_ANSWER], chart_ids, column_to_extract=parameter)
    if "unsure" in csvs:
        parsed_unsure = by_chart(csvs["unsure"], chart_ids, column_to_extract=parameter)
    parsed_group_2 = by_chart(csvs[GROUP_2_ANSWER], chart_ids, column_to_extract=parameter)
    if "unsure" in csvs:
        parsed_group_1 = merge_data(parsed_group_1, parsed_unsure)

    plt = plotter_1(
        data_1=parsed_group_1,
        label_1=LABEL_1,
        data_2=parsed_group_2,
        label_2=LABEL_2,
        x_labels=chart_ids,
        fig=fig,
        sup_title=PARAMETERS_LIST[parameter],
        group_each=GROUP_EACH_PAIRS
    )
    plt.tight_layout()
    # filename = os.path.join(path, f"{parameter}.pdf")
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    # print(f"\t\tSaving plots to {filename}...")
    # plt.savefig(filename)
    # print("\t\tPlots saved successfully!")
    plt.pause(0.1)
    plt.show(block=False)
    # plt.close(fig=fig)
    # fig.clf()
    gc.collect()


def scatter_plots(csvs, chart_ids, conversion_function=RGB2Lab.rgb2lab):
    global GROUP_1_ANSWER, GROUP_2_ANSWER, LABEL_1, LABEL_2
    picked_lab_group_1 = get_derived(csvs[GROUP_1_ANSWER], chart_ids, "picked_color", func=conversion_function)
    if "unsure" in csvs:
        picked_lab_unsure = get_derived(csvs["unsure"], chart_ids, "picked_color", func=conversion_function)
    picked_lab_group_2 = get_derived(csvs[GROUP_2_ANSWER], chart_ids, "picked_color", func=conversion_function)
    if "unsure" in csvs:
        picked_lab_group_1 = merge_data(picked_lab_group_1, picked_lab_unsure)
    path = os.path.join(saved_data_path, "ab_scatter_compl")
    target_color = {}
    start_col = {}
    for chartid in chart_ids:
        target_color[chartid] = conversion_function(target_colors[chartid])
        start_col[chartid] = conversion_function(start_colors[chartid])

    data_indexes = [1, 2, [15, 15], [-15, -15]]
    axis_labels = ["Δa*", "Δb*"]

    # plt.ion()
    # plt.pause(0.01)
    for i in range(0, len(chart_ids)):
        fig = plt.figure(dpi=300, figsize=(9, 9))
        gs = GridSpec(1, 1, figure=fig)
        axes = []
        axes.append(plt.subplot(gs[0, 0]))
        print("Plotting a*b* error for charts " + (",").join(chart_ids[i:i + 1]))
        plot_scatter(
            data_1=picked_lab_group_1,
            label_1=LABEL_1,
            data_2=picked_lab_group_2,
            label_2=LABEL_2,
            data_indexes=data_indexes[0:2],
            target_color=target_color,
            max_coordinates=data_indexes[2],
            min_coordinates=data_indexes[3],
            fig=fig,
            axes=axes,
            charts_to_plot=chart_ids[i:i + 1]
        )
        plot_vect(
            data_1=picked_lab_group_1,
            label_1=LABEL_1,
            data_2=picked_lab_group_2,
            label_2=LABEL_2,
            data_0=target_color,
            starting_point=start_col,
            data_indexes=data_indexes[0:2],
            ylabel=axis_labels[1],
            xlabel=axis_labels[0],
            label_0="target color",
            fig=fig,
            axes=axes,
            charts_to_plot=chart_ids[i:i + 1],
            sup_title="a*b* error from target"
        )
        plt.tight_layout(w_pad=10, h_pad=5)
        #plt.pause(0.1)
        #plt.show(block=False)
        filename = os.path.join(path, f"charts " + (",").join(chart_ids[i:i+1]) + ".pdf")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        print(f"\t\tSaving plots to {filename}...")
        plt.savefig(filename)
        print("\t\tPlots saved successfully!")
        plt.close(fig=fig)
        fig.clf()
        gc.collect()


def chart_hsl_compl(csvs, chart_ids):
    global plt
    path = os.path.join(saved_data_path, "chart_hsl_compl")
    fig = plt.figure(dpi=72, figsize=(10, 10))
    gs = GridSpec(1, 1, fig)
    delta_start = {}
    for chart_id in chart_ids:
        start = RGB2HSL(start_colors[chart_id])
        target = RGB2HSL(target_colors[chart_id])
        hue_dist = np.min([np.abs(start['h'] - target['h']), 360 - np.abs(start['h'] - target['h'])])
        delta_start[chart_id] = np.sqrt(
            np.power(hue_dist, 2) +
            np.power((start['s'] - target['s']), 2) +
            np.power((start['l'] - target['l']), 2)
        )
    picked_group_1 = by_chart(csvs[GROUP_1_ANSWER], chart_ids, "hsl_dist")
    if "unsure" in csvs:
        picked_unsure = by_chart(csvs["unsure"], chart_ids, "hsl_dist")
    picked_group_2 = by_chart(csvs[GROUP_2_ANSWER], chart_ids, "hsl_dist")
    if "unsure" in csvs:
        picked_group_1 = merge_data(picked_group_1, picked_unsure)

    Plots.grouped_plot(
        ax=plt.subplot(gs[0, 0]),
        data_3=Plots.get_elements(delta_start, chart_ids),
        data_1=Plots.get_median(picked_group_1, chart_ids),
        data_2=Plots.get_median(picked_group_2, chart_ids),
        label_1=LABEL_1,
        label_2=LABEL_2,
        label_3='start color',
        ticks=chart_ids,
        xlabel='chart id',
        title='HSL euclidean distance start vs picked',
        group_each=GROUP_EACH_PAIRS
    )
    plt.tight_layout()
    plt.pause(0.1)
    plt.show(block=False)
    # filename = os.path.join(path, "hsl.pdf")
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    # print(f"\t\tSaving plots to {filename}...")
    # plt.savefig(filename)
    # print("\t\tPlots saved successfully!")
    # plt.close(fig=fig)
    # fig.clf()
    gc.collect()


def compl_delta_e(csvs, chart_ids, conversion_function=RGB2Lab.rgb2lab):
    fig = plt.figure(dpi=72, figsize=(8.27, 11.69))
    gs = GridSpec(2, 1, fig)

    picked_lab_group_1 = get_derived(csvs[GROUP_1_ANSWER], chart_ids, "picked_color", func=conversion_function)
    if "unsure" in csvs:
        picked_lab_unsure = get_derived(csvs["unsure"], chart_ids, "picked_color", func=conversion_function)
    picked_lab_group_2 = get_derived(csvs[GROUP_2_ANSWER], chart_ids, "picked_color", func=conversion_function)
    if "unsure" in csvs:
        picked_lab_group_1 = merge_data(picked_lab_group_1, picked_lab_unsure)
    target_lab = {}
    start_lab = {}
    for chart_id in chart_ids:
        target_lab[chart_id] = conversion_function(target_colors[chart_id])
        start_lab[chart_id] = conversion_function(start_colors[chart_id])

    # path = os.path.join(saved_data_path, "delta_e_compl_with_starting_color")

    delta_e_group_1 = {}
    delta_e_group_2 = {}
    delta_e_start = {}
    for chart_id in CHARTIDS_BY_BG:
        point_1 = [0, 0, 0]
        for vector in picked_lab_group_1[chart_id]:
            point_1[0] += vector[0]
            point_1[1] += vector[1]
            point_1[2] += vector[2]
        point_1 = [val / len(picked_lab_group_1[chart_id]) for val in point_1]
        point_2 = [0, 0, 0]
        for vector in picked_lab_group_2[chart_id]:
            point_2[0] += vector[0]
            point_2[1] += vector[1]
            point_2[2] += vector[2]
        point_2 = [val / len(picked_lab_group_2[chart_id]) for val in point_2]
        delta_e_group_1[chart_id] = CIEDE2000(target_lab[chart_id], point_1)
        delta_e_group_2[chart_id] = CIEDE2000(target_lab[chart_id], point_2)
        delta_e_start[chart_id] = CIEDE2000(target_lab[chart_id], start_lab[chart_id])

    Plots.grouped_plot(
        ax=plt.subplot(gs[0, 0]),
        data_1=Plots.get_elements(delta_e_group_1, chart_ids),
        data_2=Plots.get_elements(delta_e_group_2, chart_ids),
        data_3=Plots.get_elements(delta_e_start, chart_ids),
        label_1=LABEL_1,
        label_2=LABEL_2,
        label_3='start color',
        ticks=chart_ids,
        ylabel='CIEDE2000',
        xlabel='chart id',
        title='DeltaE between target and point of mass',
        group_each=GROUP_EACH_PAIRS
    )

    parameter = 'delta_e'
    parsed_group_1 = by_chart(csvs[GROUP_1_ANSWER], chart_ids, column_to_extract=parameter)
    if "unsure" in csvs:
        parsed_unsure = by_chart(csvs["unsure"], chart_ids, column_to_extract=parameter)
    parsed_group_2 = by_chart(csvs[GROUP_2_ANSWER], chart_ids, column_to_extract=parameter)
    if "unsure" in csvs:
        parsed_group_1 = merge_data(parsed_group_1, parsed_unsure)

    Plots.grouped_plot(
        ax=plt.subplot(gs[1, 0]),
        data_1=Plots.get_median(parsed_group_1, chart_ids),
        data_2=Plots.get_median(parsed_group_2, chart_ids),
        data_3=Plots.get_elements(delta_e_start, chart_ids),
        label_1=LABEL_1,
        label_2=LABEL_2,
        label_3='start color',
        ticks=chart_ids,
        ylabel='CIEDE2000',
        xlabel='chart id',
        title='Median DeltaE',
        group_each=GROUP_EACH_PAIRS
    )
    plt.tight_layout()
    plt.pause(0.1)
    plt.show(block=False)
    # filename = os.path.join(path, f"{parameter}.pdf")
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    # print(f"\t\tSaving plots to {filename}...")
    # plt.savefig(filename)
    # print("\t\tPlots saved successfully!")
    # plt.close(fig=fig)
    # fig.clf()
    gc.collect()


def get_mean_delta(val1, val2, conversionFunction):
    deltas = []
    for val in val2:
        deltas.append(CIEDE2000(conversionFunction(val1), conversionFunction(val)))
    return np.mean(deltas)


def get_distances(csvs, chart_ids):
    parameter = 'picked_color'
    parsed_group_1 = by_chart(csvs[GROUP_1_ANSWER], chart_ids, column_to_extract=parameter)
    if "unsure" in csvs:
        parsed_unsure = by_chart(csvs["unsure"], chart_ids, column_to_extract=parameter)
    parsed_group_2 = by_chart(csvs[GROUP_2_ANSWER], chart_ids, column_to_extract=parameter)
    if "unsure" in csvs:
        parsed_group_1 = merge_data(parsed_group_1, parsed_unsure)

    d1 = {}
    d2_group_1 = {}
    d2_group_2 = {}
    d3_group_1 = {}
    d3_group_2 = {}
    d1d3_group_1 = {}
    d1d3_group_2 = {}

    for chart_id in chart_ids:
        target_lab = RGB2Lab.rgb2lab(target_colors[chart_id])
        start_lab = RGB2Lab.rgb2lab(start_colors[chart_id])
        d1[chart_id] = CIEDE2000(target_lab, start_lab)
        d2_group_1[chart_id] = get_mean_delta(target_colors[chart_id], parsed_group_1[chart_id], RGB2Lab.rgb2lab)
        d2_group_2[chart_id] = get_mean_delta(target_colors[chart_id], parsed_group_2[chart_id], RGB2Lab.rgb2lab)
        d3_group_1[chart_id] = get_mean_delta(start_colors[chart_id], parsed_group_1[chart_id], RGB2Lab.rgb2lab)
        d3_group_2[chart_id] = get_mean_delta(start_colors[chart_id], parsed_group_2[chart_id], RGB2Lab.rgb2lab)
        d1d3_group_1[chart_id] = np.abs(d1[chart_id] - d3_group_1[chart_id])
        d1d3_group_2[chart_id] = np.abs(d1[chart_id] - d3_group_2[chart_id])

    fig = plt.figure(dpi=72, figsize=(8.27, 11.69))
    gs = GridSpec(2, 1, fig)

    Plots.grouped_plot(
        ax=plt.subplot(gs[0, 0]),
        data_1=Plots.get_elements(d1d3_group_1, chart_ids),
        data_2=Plots.get_elements(d2_group_1, chart_ids),
        label_1="D1-D3",
        label_2="D2",
        color_1=COLOR_1,
        color_2="#000000",
        title=LABEL_1,
        ticks=chart_ids,
        group_each=GROUP_EACH_STD
    )
    Plots.grouped_plot(
        ax=plt.subplot(gs[1, 0]),
        data_1=Plots.get_elements(d1d3_group_2, chart_ids),
        data_2=Plots.get_elements(d2_group_2, chart_ids),
        label_1="D1-D3",
        label_2="D2",
        color_1=COLOR_2,
        color_2="#000000",
        title=LABEL_2,
        ticks=chart_ids,
        group_each=GROUP_EACH_STD
    )

    plt.tight_layout()
    plt.pause(0.1)
    plt.show(block=False)


def lab_variance(csvs, chart_ids, conversion_function=RGB2Lab.rgb2lab):
    parameter = 'picked_color'

    picked_lab_group_1 = get_derived(csvs[GROUP_1_ANSWER], CHARTIDS, parameter, func=conversion_function)
    if "unsure" in csvs:
        picked_lab_unsure = get_derived(csvs["unsure"], CHARTIDS, parameter, func=conversion_function)
    picked_lab_group_2 = get_derived(csvs[GROUP_2_ANSWER], CHARTIDS, parameter, func=conversion_function)
    if "unsure" in csvs:
        picked_lab_group_1 = merge_data(picked_lab_group_1, picked_lab_unsure)
    path = os.path.join(saved_data_path, "ab_variance")
    fig = plt.figure(dpi=72, figsize=(8, 12))
    gs = GridSpec(3, 1, fig)

    group_1_var = {}
    group_2_var = {}

    for chart_id in chart_ids:
        group_1_mean = np.mean(picked_lab_group_1[chart_id], axis=0)
        group_1_distances = []
        group_2_mean = np.mean(picked_lab_group_2[chart_id], axis=0)
        group_2_distances = []
        for val in picked_lab_group_1[chart_id]:
            group_1_distances.append(np.power(distance.euclidean(group_1_mean, [val[0], val[1], val[2]]), 2))
        for val in picked_lab_group_2[chart_id]:
            group_2_distances.append(np.power(distance.euclidean(group_2_mean, [val[0], val[1], val[2]]), 2))
        group_1_var[chart_id] = np.sqrt(np.sum(group_1_distances) / len(group_1_distances))
        group_2_var[chart_id] = np.sqrt(np.sum(group_2_distances) / len(group_2_distances))

    Plots.grouped_plot(
        ax=plt.subplot(gs[0, 0]),
        data_1=Plots.get_elements(group_1_var, chart_ids),
        data_2=Plots.get_elements(group_2_var, chart_ids),
        label_1=LABEL_1,
        label_2=LABEL_2,
        ticks=chart_ids,
        group_each=GROUP_EACH_STD,
        title="L*a*b* variance"
    )

    for chart_id in chart_ids:
        group_1_mean = [np.mean(list(zip(*picked_lab_group_1[chart_id]))[1]),
                        np.mean(list(zip(*picked_lab_group_1[chart_id]))[2])]
        group_1_distances = []
        group_2_mean = [np.mean(list(zip(*picked_lab_group_2[chart_id]))[1]),
                        np.mean(list(zip(*picked_lab_group_2[chart_id]))[2])]
        group_2_distances = []
        for val in picked_lab_group_1[chart_id]:
            group_1_distances.append(np.power(distance.euclidean(group_1_mean, [val[1], val[2]]), 2))
        for val in picked_lab_group_2[chart_id]:
            group_2_distances.append(np.power(distance.euclidean(group_2_mean, [val[1], val[2]]), 2))
        group_1_var[chart_id] = np.sqrt(np.sum(group_1_distances) / len(group_1_distances))
        group_2_var[chart_id] = np.sqrt(np.sum(group_2_distances) / len(group_2_distances))

    Plots.grouped_plot(
        ax=plt.subplot(gs[1, 0]),
        data_1=Plots.get_elements(group_1_var, chart_ids),
        data_2=Plots.get_elements(group_2_var, chart_ids),
        label_1=LABEL_1,
        label_2=LABEL_2,
        ticks=chart_ids,
        group_each=GROUP_EACH_STD,
        title="a*b* variance"
    )

    for chart_id in chart_ids:
        group_1_mean = [np.mean(list(zip(*picked_lab_group_1[chart_id]))[0])]
        group_1_distances = []
        group_2_mean = [np.mean(list(zip(*picked_lab_group_2[chart_id]))[0])]
        group_2_distances = []
        for val in picked_lab_group_1[chart_id]:
            group_1_distances.append(np.power(val[0] - group_1_mean, 2))
        for val in picked_lab_group_2[chart_id]:
            group_2_distances.append(np.power(val[0] - group_2_mean, 2))
        group_1_var[chart_id] = np.sqrt(np.sum(group_1_distances) / len(group_1_distances))
        group_2_var[chart_id] = np.sqrt(np.sum(group_2_distances) / len(group_2_distances))

    Plots.grouped_plot(
        ax=plt.subplot(gs[2, 0]),
        data_1=Plots.get_elements(group_1_var, chart_ids),
        data_2=Plots.get_elements(group_2_var, chart_ids),
        label_1=LABEL_1,
        label_2=LABEL_2,
        ticks=chart_ids,
        group_each=GROUP_EACH_STD,
        title="L* variance"
    )
    plt.tight_layout()
    plt.pause(0.1)
    plt.show(block=False)


def show_charts(csvs, chart_ids):
    global GROUP_1_ANSWER, GROUP_2_ANSWER, LABEL_1, LABEL_2
    picked_lab_group_1 = get_derived(csvs[GROUP_1_ANSWER], chart_ids, "picked_color", func=RGB2Lab.rgb2lab)
    if "unsure" in csvs:
        picked_lab_unsure = get_derived(csvs["unsure"], chart_ids, "picked_color", func=RGB2Lab.rgb2lab)
    picked_lab_group_2 = get_derived(csvs[GROUP_2_ANSWER], chart_ids, "picked_color", func=RGB2Lab.rgb2lab)
    if "unsure" in csvs:
        picked_lab_group_1 = merge_data(picked_lab_group_1, picked_lab_unsure)

    path = os.path.join(saved_data_path, "charts_simulation")

    img = Image.new(mode="RGB", size=(1400, 1400))
    drawgrid = DrawGrid(350, 75, img, [len(chart_ids), 3])
    drawgrid.initBoxes()
    drawgrid.setColor([1, 1], "#ff0000", "#ffff00")
    i = 0

    bgImg = Image.open(os.path.join(test_results_path, "whitenoise.pdf"))

    for chart_id in chart_ids:
        group_1_mean_lab = np.mean(picked_lab_group_1[chart_id], axis=0)
        group_2_mean_lab = np.mean(picked_lab_group_2[chart_id], axis=0)
        if context_colors[chart_id] != "wn":
            drawgrid.setColor([i, 0],
                              target_colors[chart_id], context_colors[chart_id],
                              chart_id + ", target")
            drawgrid.setColor([i, 1],
                              RGB2Lab.lab2rgb(group_2_mean_lab), context_colors[chart_id],
                              chart_id + ", " + LABEL_2)
            drawgrid.setColor([i, 2],
                              RGB2Lab.lab2rgb(group_1_mean_lab), context_colors[chart_id],
                              chart_id + ", " + LABEL_1)
        else:
            drawgrid.setBgImage([i, 0], target_colors[chart_id], bgImg, chart_id + ", target")
            drawgrid.setBgImage([i, 1], RGB2Lab.lab2rgb(group_2_mean_lab), bgImg, chart_id + ", " + LABEL_2)
            drawgrid.setBgImage([i, 2], RGB2Lab.lab2rgb(group_1_mean_lab), bgImg, chart_id + ", " + LABEL_1)
        i += 1
    img.show()
    img.save(os.path.join(path, f'{chart_ids}.pdf'))


def default_function():
    print("Please enter a valid value")
    return


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def choose_charts(chart_ids, function, group_each_id=2, csvs=csvs):
    sub_ids = np.array_split(chart_ids, int(len(chart_ids) / group_each_id))
    print("\n")
    for i in range(0, len(sub_ids)):
        print(f"[{i + 1}]\t{sub_ids[i]}")
    print("[0]\tgo back...")
    choice = int(input("Which charts to plot? "))
    if 0 < choice <= int(len(chart_ids) / group_each_id):
        function(csvs=csvs,
                 chart_ids=sub_ids[choice - 1])
        return 1
    elif choice == 0:
        return 0
    else:
        return -1


def choose_parameter(chart_ids, function, csvs=csvs, parameters=PARAMETERS_LIST):
    i = 1
    parameters_key_list = []
    print("\n")
    for param in parameters:
        print(f"[{i}]\t{parameters[param]}")
        parameters_key_list.append(param)
        i += 1
    print("[0]\tgo back...")
    choice = int(input("Which parameter to plot? "))
    if 0 < choice <= int(len(parameters)):
        function(parameter=parameters_key_list[choice - 1],
                 chart_ids=chart_ids,
                 csvs=csvs)
        return 1
    elif choice == 0:
        return 0
    else:
        return -1


# sub_ids = np.array_split(CHARTIDS, int(len(CHARTIDS) / 2))
# scatter_plots(csvs=csvs, chart_ids=sub_ids[0])

while True:
    print("\n")
    print("[l]\tL*a*b* scatter")
    print("[v]\tL*a*b* variance")
    print("[d]\tCheck distances")
    print("[c]\tDelta-e between complementary patches")
    print("[s]\tGlobal stats")
    print("[u]\tGlobal stats showing users")
    print("[p]\tStart vs picked colors")
    print("[o]\tComplementary by chart")
    print("[i]\tIQR and stats (trichromats only)")
    print("[h]\tStart vs picked HSL euclidean distance")
    print("[z]\tShow mean colors")
    print("[q]\tQuit")
    choice = input("Select a plot: ")
    choice = choice.casefold()
    # Scatter plots
    if choice == 'l':
        while True:
            result = choose_charts(CHARTIDS_BY_BG, scatter_plots, group_each_id=2)
            if result == -1:
                print("Please make a valid choice")
            elif result == 0:
                break
    if choice == 'z':
        while True:
            result = choose_charts(CHARTIDS, show_charts, group_each_id=3)
            if result == -1:
                print("Please make a valid choice")
            elif result == 0:
                break
    elif choice == 'v':
        lab_variance(csvs, CHARTIDS)
    elif choice == 'd':
        get_distances(csvs, CHARTIDS)
    elif choice == 'c':
        compl_delta_e(csvs, CHARTIDS_BY_BG)
    elif choice == 'h':
        chart_hsl_compl(csvs, CHARTIDS_BY_BG)
    elif choice == 's':
        while True:
            result = choose_parameter(CHARTIDS, global_stats)
            if result == -1:
                print("Please make a valid choice")
            elif result == 0:
                break
    elif choice == 'u':
        while True:
            result = choose_parameter(CHARTIDS, by_user_stats)
            if result == -1:
                print("Please make a valid choice")
            elif result == 0:
                break
    elif choice == 'p':
        while True:
            result = choose_parameter(CHARTIDS, start_vs_picked, parameters=START_TO_PICKED)
            if result == -1:
                print("Please make a valid choice")
            elif result == 0:
                break
    elif choice == 'o':
        while True:
            result = choose_parameter(CHARTIDS_BY_BG, by_chart_compl)
            if result == -1:
                print("Please make a valid choice")
            elif result == 0:
                break
    elif choice == 'i':
        while True:
            result = choose_parameter(CHARTIDS, plot_iqr)
            if result == -1:
                print("Please make a valid choice")
            elif result == 0:
                break
    elif choice == 'q':
        exit()
    else:
        print("Please make a valid choice")
