import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

from Plotting import Plots as plotter
from Plotting.PlotCharts import sort_dictionary
import numpy as np


def plot_style_1(data_1, data_2, label_1, label_2, x_labels, fig, sup_title=None, ylabel=None, xlabel='chart_id',
                 group_each=3):
    gs = GridSpec(5, 2, figure=fig)

    fig.suptitle(sup_title, fontweight="bold", fontsize=18)

    ax1 = plotter.grouped_boxplot(
        ax=plt.subplot(gs[:2, :]),
        parsed_data_1=data_1,
        parsed_data_2=data_2,
        label_1=label_1,
        label_2=label_2,
        ticks=x_labels,
        ylabel=ylabel,
        showfliers=True
    )
    ax1.grid(True)
    ax1.grid(color="#eeeeee", linestyle='-', linewidth=0.5)

    ax2 = plotter.grouped_boxplot(
        ax=plt.subplot(gs[2, :]),
        parsed_data_1=data_1,
        parsed_data_2=data_2,
        label_1=label_1,
        label_2=label_2,
        ticks=x_labels,
        ylabel=ylabel,
        showfliers=False
    )
    ax2.grid(True)
    ax2.grid(color="#eeeeee", linestyle='-', linewidth=0.5)

    ax3 = plotter.grouped_plot(
        ax=plt.subplot(gs[-2:, 0]),
        data_1=plotter.get_median(data_1, chart_ids=x_labels),
        data_2=plotter.get_median(data_2, chart_ids=x_labels),
        label_1=label_1,
        label_2=label_2,
        ticks=x_labels,
        title="median" if ylabel is None else "median " + ylabel,
        xlabel=xlabel,
        group_each=group_each
    )
    ax3.grid(True)
    ax3.grid(color="#eeeeee", linestyle='-', linewidth=0.5)

    ax4 = plotter.grouped_plot(
        ax=plt.subplot(gs[-2:, -1]),
        data_1=plotter.get_var_coeff(data_1, chart_ids=x_labels),
        data_2=plotter.get_var_coeff(data_2, chart_ids=x_labels),
        label_1=label_1,
        label_2=label_2,
        ticks=x_labels,
        title="coefficient of variation",
        xlabel=xlabel,
        group_each=group_each
    )
    ax4.grid(True)
    ax4.grid(color="#eeeeee", linestyle='-', linewidth=0.5)

    fig.add_subplot(ax1)
    fig.add_subplot(ax2)
    fig.add_subplot(ax3)
    fig.add_subplot(ax4)

    plt.tight_layout()

    return plt


def plot_style_1_PAPER(data_1, label_1, x_labels, fig, data_2=None, hlines=None, label_2=None, label_3=None,
                       sup_title=None, ylabel1=None, ylabel2=None, xlabel='chart_id', group_each=3,
                       color_1="#2C7BB6", color_2="#EBBA34", color_3="#000000"):
    gs = GridSpec(2, 1, figure=fig)

    fig.suptitle(sup_title, fontweight="bold", fontsize=18)

    ax1 = plotter.grouped_boxplot(
        ax=plt.subplot(gs[0, 0]),
        parsed_data_1=data_1,
        parsed_data_2=data_2,
        label_1=label_1,
        label_2=label_2,
        ticks=x_labels,
        xlabel=xlabel,
        ylabel=ylabel1,
        showfliers=True
    )
    ax1.grid(True)
    ax1.grid(color="#eeeeee", linestyle='-', linewidth=0.5)

    ax2 = plotter.grouped_plot_style2(
        ax=plt.subplot(gs[1, 0]),
        data_1=plotter.get_median(data_1, chart_ids=x_labels),
        data_2=plotter.get_median(data_2, chart_ids=x_labels),
        # data_3=plotter.get_median(data_3, chart_ids=x_labels),
        label_1=label_1,
        label_2=label_2,
        # label_3=label_3,
        ticks=x_labels,
        title="",
        xlabel=xlabel,
        ylabel=ylabel2,
        group_each=group_each
    )
    x = []
    for groups in range(int(len(hlines))):
        x.append(groups * group_each)
    x = np.array(x)
    ax2.hlines(hlines, x - 0.5, x + 2, linestyles="dashdot", colors=["#000000"])

    patches = [mpatches.Patch(color=c) for c in [color_1, color_2]]
    patches.append(Line2D([0], [0], color=color_3, linewidth=3, linestyle='--'))
    labels = [label_1, label_2, label_3]
    ax2.legend(patches, labels)

    ax2.grid(True)
    ax2.grid(color="#eeeeee", linestyle='-', linewidth=0.5)

    fig.add_subplot(ax1)
    fig.add_subplot(ax2)

    plt.tight_layout()

    return plt


def plot_style_2(data, x_labels, fig, sup_title=None, ylabel=None, xlabel='chart_id', group_each=0, color="#2C7BB6"):
    gs = GridSpec(5, 2, figure=fig)

    fig.suptitle(sup_title, fontweight="bold", fontsize=18)

    ax1 = plotter.simple_boxplot(
        ax=plt.subplot(gs[:2, :]),
        parsed_data=data,
        ticks=x_labels,
        ylabel=ylabel,
        showfliers=True,
        color=color
    )
    ax1.grid(True)
    ax1.grid(color="#eeeeee", linestyle='-', linewidth=0.5)

    ax2 = plotter.simple_boxplot(
        ax=plt.subplot(gs[2, :]),
        parsed_data=data,
        ticks=x_labels,
        ylabel=ylabel,
        showfliers=False,
        color=color
    )
    ax2.grid(True)
    ax2.grid(color="#eeeeee", linestyle='-', linewidth=0.5)

    ax3 = plotter.simple_plot(
        ax=plt.subplot(gs[-2:, 0]),
        data=plotter.get_median(data, chart_ids=x_labels),
        ticks=x_labels,
        title="median" if ylabel is None else "median " + ylabel,
        xlabel=xlabel,
        group_each=group_each,
        color=color
    )
    ax3.grid(True)
    ax3.grid(color="#eeeeee", linestyle='-', linewidth=0.5)

    ax4 = plotter.simple_plot(
        ax=plt.subplot(gs[-2:, -1]),
        data=plotter.get_iqr(data, chart_ids=x_labels),
        ticks=x_labels,
        title="interquartile range",
        xlabel=xlabel,
        group_each=group_each,
        color=color
    )
    ax4.grid(True)
    ax4.grid(color="#eeeeee", linestyle='-', linewidth=0.5)

    fig.add_subplot(ax1)
    fig.add_subplot(ax2)
    fig.add_subplot(ax3)
    fig.add_subplot(ax4)

    plt.tight_layout()

    return plt
