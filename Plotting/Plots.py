import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import variation


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
    ax.set_xticklabels(ticks, fontsize=8, rotation=45)
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
def grouped_bargraph(ax, data_1, data_2, label_1, label_2, ticks, color_1="#2C7BB6", color_2="#ebba34", ylabel=None,
                     xlabel=None, title=None):
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()

    x = np.arange(len(ticks))  # the label locations
    rects1 = ax.bar(x - width / 2, data_1, width, label=label_1, color=color_1)
    rects2 = ax.bar(x + width / 2, data_2, width, label=label_2, color=color_2)

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

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    return plt


#
#
#
#   GROUPED PLOT DRAWING
#
def grouped_plot(ax, data_1, data_2, label_1, label_2, ticks, color_1="#2C7BB6", color_2="#ebba34", ylabel=None,
                 xlabel=None, title=None, group_each=0):
    x = np.arange(len(ticks))  # the label locations

    if group_each > 0:
        groups = len(ticks) / group_each
        assert groups % group_each == 0, "Number of fields must be a multiple of 'group_each'"
        groups = int(groups)
        ax.plot(ticks[0:group_each], data_1[0:group_each], label=label_1, color=color_1)
        ax.plot(ticks[0:group_each], data_2[0:group_each], label=label_2, color=color_2)
        for i in range(groups):
            ax.plot(ticks[i * group_each:i * group_each + group_each],
                    data_1[i * group_each:i * group_each + group_each], color=color_1)
            ax.plot(ticks[i * group_each:i * group_each + group_each],
                    data_2[i * group_each:i * group_each + group_each], color=color_2)
    else:
        ax.plot(ticks, data_1, label=label_1, color=color_1)
        ax.plot(ticks, data_2, label=label_2, color=color_2)

    ax.plot(ticks, data_1, 'o', color=color_1)
    ax.plot(ticks, data_2, 'o', color=color_2)

    vlines = np.maximum(data_1, data_2)
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
    ax.set_xticklabels(ticks, fontsize=8, rotation=60)

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