from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
from numpy import array
from scipy.stats import variation
from scipy.stats import iqr


def get_median(data, chart_ids):
    avgs = []
    for chart_id in chart_ids:
        avgs.append(np.median(data[chart_id]))
    return avgs


def get_var_coeff(data, chart_ids):
    elements = []
    for chart_id in chart_ids:
        elements.append(variation(data[chart_id]))
    return elements


def get_iqr(data, chart_ids):
    elements = []
    for chart_id in chart_ids:
        elements.append(iqr(data[chart_id]))
    return elements

def get_elements(data, chart_ids):
    elements = []
    for chart_id in chart_ids:
        elements.append(data[chart_id])
    return elements

#
#
#
#   GROUPED BOX PLOT DRAWING
#
def grouped_boxplot(ax, parsed_data_1, parsed_data_2, label_1, label_2, ticks, color_1="#2C7BB6", color_2="#ebba34",
                    ylabel=None, xlabel=None, title=None, showfliers=False):
    data_1 = []
    data_2 = []
    for chart_id in ticks:
        data_1.append(parsed_data_1[chart_id])
        data_2.append(parsed_data_2[chart_id])

    def set_box_color(bp, color):
        plt.setp(bp['boxes'], color=color)
        plt.setp(bp['whiskers'], color=color)
        plt.setp(bp['caps'], color=color)
        plt.setp(bp['medians'], color=color)
        if showfliers:
            plt.setp(bp['fliers'], markeredgecolor=color, marker='+')
    bpl = ax.boxplot(data_1, positions=np.array(range(len(data_1))) * 2.0 - 0.4, widths=0.6, showfliers=showfliers)
    bpr = ax.boxplot(data_2, positions=np.array(range(len(data_2))) * 2.0 + 0.4, widths=0.6, showfliers=showfliers)
    set_box_color(bpl, color_1)
    set_box_color(bpr, color_2)

    # draw temporary red and blue lines and use them to create a legend
    ax.plot([], c=color_1, label=label_1)
    ax.plot([], c=color_2, label=label_2)
    ax.legend()

    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)

    ax.set_xticks(range(0, len(ticks) * 2, 2))
    ax.set_xticklabels(ticks, fontsize=8, rotation=45, ha='right', rotation_mode='anchor')
    ax.set_xlim(-2, len(ticks) * 2)

    return ax


#
#
#
#   SIMPLE BOX PLOT DRAWING
#
def simple_boxplot(ax, parsed_data, ticks, color="#2C7BB6", ylabel=None, xlabel=None, title=None, showfliers=False):
    data = []
    for chart_id in ticks:
        data.append(parsed_data[chart_id])

    def set_box_color(bp, color):
        plt.setp(bp['boxes'], color=color)
        plt.setp(bp['whiskers'], color=color)
        plt.setp(bp['caps'], color=color)
        plt.setp(bp['medians'], color=color)
        if showfliers:
            plt.setp(bp['fliers'], markeredgecolor=color, marker='+')

    bpl = ax.boxplot(data, positions=np.array(range(len(data))) * 2.0 - 0.4, widths=0.6, showfliers=showfliers)
    set_box_color(bpl, color)

    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)

    ax.set_xticks(range(0, len(ticks) * 2, 2))
    ax.set_xticklabels(ticks, fontsize=8, rotation=45)
    ax.set_xlim(-2, len(ticks) * 2)

    return ax


#
#
#
#   GROUPED GRAPH BAR DRAWING
#
def grouped_plot_style2(ax, data_1, label_1, ticks, data_2=None, data_3=None, label_2=None, label_3=None,
                        color_1="#2C7BB6", color_2="#EBBA34", color_3="#000000",
                        ylabel=None, xlabel=None, title=None, group_each=3, inner_group_spacing=0.8):
    width = 0.20
    # x = np.arange(len(ticks))  # the label locations
    # x = array([0, 0.7, 1.4, 3, 3.7, 4.4, 6, 6.7, 7.4, 9, 9.7, 10.4, 12, 12.7, 13.4, 15, 15.7, 16.4])
    x = []
    for groups in range(int(len(ticks)/group_each)):
        for i in range(group_each):
            x.append(groups*group_each+i*inner_group_spacing)
    x = array(x)

    ax.bar(x-width, data_1, width, color=color_1, label=label_1)
    if data_2 is not None:
        ax.bar(x, data_2, width, color=color_2, label=label_2)
    if data_3 is not None:
        ax.bar(x+width, data_3, width, color=color_3, label=label_3)

    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(ticks, rotation=45, ha='right', rotation_mode='anchor')
    ax.legend()

    return ax


#
#
#
#   GROUPED PLOT DRAWING
#
def grouped_plot(ax, data_1, label_1, ticks, label_2=None, data_2=None, label_3=None, data_3=None, color_1="#2C7BB6", color_2="#ebba34", color_3="#2a2a2a", ylabel=None,
                 xlabel=None, title=None, group_each=0) -> object:
    x = np.arange(len(ticks))  # the label locations

    if group_each > 0:
        groups = len(ticks) / group_each
        assert groups % group_each == 0, "Number of fields must be a multiple of 'group_each'"
        groups = int(groups)
        ax.plot(ticks[0:group_each], data_1[0:group_each], label=label_1, color=color_1)
        if data_2 is not None:
            ax.plot(ticks[0:group_each], data_2[0:group_each], label=label_2, color=color_2)
        if data_3 is not None:
            ax.plot(ticks[0:group_each], data_3[0:group_each], label=label_3, color=color_3)
        for i in range(groups):
            ax.plot(ticks[i * group_each:i * group_each + group_each],
                    data_1[i * group_each:i * group_each + group_each], color=color_1)
            if data_2 is not None:
                ax.plot(ticks[i * group_each:i * group_each + group_each],
                    data_2[i * group_each:i * group_each + group_each], color=color_2)
            if data_3 is not None:
                ax.plot(ticks[i * group_each:i * group_each + group_each],
                        data_3[i * group_each:i * group_each + group_each], color=color_3)
    else:
        ax.plot(ticks, data_1, label=label_1, color=color_1)
        if data_2 is not None:
            ax.plot(ticks, data_2, label=label_2, color=color_2)
        if data_3 is not None:
            ax.plot(ticks, data_3, label=label_3, color=color_3)

    ax.plot(ticks, data_1, 'o', color=color_1)
    if data_2 is not None:
        ax.plot(ticks, data_2, 'o', color=color_2)
    if data_3 is not None:
        ax.plot(ticks, data_3, 'o', color=color_3)

    vlines = data_1
    if data_2 is not None:
        vlines = np.maximum(vlines, data_2)
    if data_3 is not None:
        vlines = np.maximum(vlines, data_3)
    ax.vlines(ticks, [0], vlines, color="#dddddd")

    # Add some text for labels, title and custom x-axis tick labels, etc.
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(ticks, fontsize=8, rotation=45)
    ax.legend()

    return ax


#
#
#
#   SIMPLE PLOT DRAWING
#
def simple_plot(ax, data, ticks, color="#2C7BB6", ylabel=None, xlabel=None, title=None, group_each=0):
    x = np.arange(len(ticks))  # the label locations

    if group_each > 0:
        groups = len(ticks) / group_each
        assert groups % group_each == 0, "Number of fields must be a multiple of 'group_each'"
        groups = int(groups)
        ax.plot(ticks[0:group_each], data[0:group_each], color=color)
        for i in range(groups):
            ax.plot(ticks[i * group_each:i * group_each + group_each], data[i * group_each:i * group_each + group_each],
                    color=color)
    else:
        ax.plot(ticks, data, color=color)

    ax.plot(ticks, data, 'o', color=color)

    ax.vlines(ticks, [0], data, color="#dddddd")

    # Add some text for labels, title and custom x-axis tick labels, etc.
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(ticks, rotation=60)

    return ax


#
#
#
#   GROUPED VERTICAL PLOT
#
def grouped_vertical_plot(ax, data, ticks, ticks_1, ticks_2, color_1="#2C7BB6", color_2="#ebba34", ylabel=None, xlabel=None, title=None):
    x = np.arange(len(ticks))  # the label locations

    for i in range(0, len(ticks)):
        tick_color="#000000"
        if ticks[i] in ticks_1:
            tick_color=color_1
        elif ticks[i] in ticks_2:
            tick_color=color_2
        ax.plot(ticks[i], data[i], 'o', color=tick_color)

    ax.vlines(ticks, [0], data, color="#dddddd")

    # Add some text for labels, title and custom x-axis tick labels, etc.
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(ticks, fontsize=8, rotation=90)

    return ax