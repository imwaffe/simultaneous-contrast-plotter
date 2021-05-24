import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D


def plot_ab(data_1, data_2, grid_spec, color_1="#2C7BB6", color_2="#ebba34", ylabel="b*", xlabel="a*", title=None):
    ax = plt.subplot(grid_spec)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_label_coords(1.03, .53)
    ax.yaxis.set_label_coords(.5, -.1)

    max_x = 0
    max_y = 0
    for Lab in data_1:
        ax.scatter(Lab[1], Lab[2], c=color_1, s=15, alpha=0.25)
        max_x = max(max_x, abs(Lab[1]))
        max_y = max(max_y, abs(Lab[2]))
    for Lab in data_2:
        ax.scatter(Lab[1], Lab[2], c=color_2, s=15, alpha=0.25)
        max_x = max(max_x, abs(Lab[1]))
        max_y = max(max_y, abs(Lab[2]))
    max_x += 10
    max_y += 10
    ax.set_xlim([-max_x, max_x])
    ax.set_ylim([-max_y, max_y])
    if xlabel is not None:
        ax.set_xlabel(xlabel, fontweight="bold", fontsize="x-large")
    if ylabel is not None:
        ax.set_ylabel(ylabel, rotation=0, fontweight="bold", fontsize="x-large")
    if title is not None:
        ax.set_title(title)
    return ax


def plot_three_charts(data_1, data_2, fig, label_1, label_2, charts_to_plot, sup_title=None, color_1="#2C7BB6",
                      color_2="#ebba34"):
    assert len(charts_to_plot) is 3, "charts_to_plot should be of length 3"

    legend_elements = [
        Line2D([0], [0], marker='o', color=color_1, label=label_1, lw=0),
        Line2D([0], [0], marker='o', color=color_2, label=label_2, lw=0),
    ]
    fig.suptitle(sup_title, fontweight="bold", fontsize=18)
    fig.legend(handles=legend_elements)
    gs = GridSpec(3, 1, figure=fig)

    row = 0
    for chart_id in charts_to_plot:
        ax = plot_ab(data_1[chart_id], data_2[chart_id], gs[row, 0],
                     title=f"chart {chart_id}")
        row += 1

    plt.subplots_adjust(top=2)
    plt.tight_layout()
    return plt
