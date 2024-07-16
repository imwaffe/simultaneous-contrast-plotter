import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D


def plot_scatter_two_groups(data_1, data_2, ax, data_indexes, target_color, max_coord=[128, 128], min_coord=[-128, -128],
                            color_1="#2C7BB6", color_2="#ebba34", ylabel=None, xlabel=None, title=None):
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    if min_coord[1] == 0:
        ax.xaxis.set_label_coords(1.03, 0.03)
        ax.yaxis.set_label_coords(.53, 0.95)
    else:
        ax.xaxis.set_label_coords(0.97, .53)
        ax.yaxis.set_label_coords(.53, -0.01)
    ax.spines['left'].set_position(('data', 0.0))
    ax.spines['bottom'].set_position(('data', 0.0))

    for vector in data_1:
        ax.scatter(vector[data_indexes[0]]-target_color[data_indexes[0]], vector[data_indexes[1]]-target_color[data_indexes[1]], c=color_1, s=15, alpha=1)
        # max_coord[0] = max(max_coord[0], vector[data_indexes[0]])
        # max_coord[1] = max(max_coord[1], vector[data_indexes[1]])
        # min_coord[0] = min(min_coord[0], vector[data_indexes[0]])
        # min_coord[1] = min(min_coord[1], vector[data_indexes[1]])
    for vector in data_2:
        ax.scatter(vector[data_indexes[0]]-target_color[data_indexes[0]], vector[data_indexes[1]]-target_color[data_indexes[1]], c=color_2, s=15, alpha=1)
        # max_coord[0] = max(max_coord[0], vector[data_indexes[0]])
        # max_coord[1] = max(max_coord[1], vector[data_indexes[1]])
        # min_coord[0] = min(min_coord[0], vector[data_indexes[0]])
        # min_coord[1] = min(min_coord[1], vector[data_indexes[1]])
    max_coord = [val + val * 0.1 for val in max_coord]
    min_coord = [val + val * 0.1 for val in min_coord]
    if xlabel is not None:
        ax.set_xlabel(xlabel, fontweight="bold", fontsize="x-large")
    if ylabel is not None:
        ax.set_ylabel(ylabel, rotation=90, fontweight="bold", fontsize="x-large")
    if title is not None:
        ax.set_title(title)
    return ax, max_coord, min_coord


def plot_three_charts(data_1, data_2, fig, axes, label_1, label_2, charts_to_plot, target_color,
                      data_indexes=[0, 1], max_coordinates=[128, 128], min_coordinates=[-128, -128],
                      sup_title=None, color_1="#2C7BB6", color_2="#ebba34"):
    legend_elements = [
        Line2D([0], [0], marker='o', color=color_1, label=label_1, lw=0),
        Line2D([0], [0], marker='o', color=color_2, label=label_2, lw=0),
        Line2D([0], [0], marker='s', color='#000000', label=label_1+' mean', lw=0),
        Line2D([0], [0], marker='v', color='#000000', label=label_2+' mean', lw=0),
        Line2D([0], [0], marker='o', color='#000000', label='target color', lw=0),
        Line2D([0], [0], marker='x', color='#000000', label='starting color', lw=0),
    ]
    fig.suptitle(sup_title, fontweight="bold", fontsize=18)
    # fig.legend(handles=legend_elements)

    row = 0
    for chart_id in charts_to_plot:
        ax, max_coord, min_coord = plot_scatter_two_groups(data_1[chart_id], data_2[chart_id], target_color=target_color[chart_id],
                                                           max_coord=max_coordinates, min_coord=min_coordinates,
                                                           data_indexes=data_indexes, ax=axes[row],
                                                           #title=f"chart {chart_id}"
                                                           )
        # max_coordinates[0] = max(max_coord[0], max_coordinates[0])
        # max_coordinates[1] = max(max_coord[1], max_coordinates[1])
        # min_coordinates[0] = min(min_coord[0], min_coordinates[0])
        # min_coordinates[1] = min(min_coord[1], min_coordinates[1])
        row += 1

    for ax in axes:
        ax.set_xlim([min_coordinates[0], max_coordinates[0]])
        ax.set_ylim([min_coordinates[1], max_coordinates[1]])

    plt.subplots_adjust(top=2)
    plt.tight_layout()
