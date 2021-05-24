import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D

from Plotting import Plots as plotter


def truncate_string(string, max, placeholder):
    return string[:max] + (string[max:] and placeholder)


def sort_dictionary(dictionary, column_keys, truncate=0, sort=True):
    data = {}
    sorted_data = []
    sorted_ticks = []

    for tick in dictionary:
        data[tick] = []
        data[tick].append(dictionary[tick][column_keys])

    sorting_array = dictionary
    if sort:
        sorting_array = sorted(data, key=data.get)

    for tick in sorting_array:
        display_tick = tick
        if truncate > 0:
            display_tick = truncate_string(tick, truncate, "..")
        sorted_ticks.append(display_tick)
        sorted_data.append(data[tick])

    return sorted_ticks, sorted_data


def draw_plot(data, ticks, title, grid_spec, color):
    ax = plotter.simple_plot(
        ax=plt.subplot(grid_spec),
        data=data,
        ticks=ticks,
        title=title,
        group_each=1,
        color=color
    )
    ax.axhline(y=np.quantile(data, 0.75), color=color, ls='dotted',
               label=f'3rd quartile = {np.quantile(data, 0.75)}')
    ax.axhline(y=np.median(data), color=color, label=f'median = {np.median(data)}')
    ax.axhline(y=np.quantile(data, 0.25), color=color, ls='--',
               label=f'1st quartile = {np.quantile(data, 0.25)}')
    ax.legend()
    return ax


def merge_series(dict_1, dict_2, column_keys, sort=True, truncate=0):
    merged = {**dict_1, **dict_2}
    return sort_dictionary(
        dictionary=merged,
        column_keys=column_keys,
        truncate=truncate,
        sort=sort
    )


def draw_merged_plot(data, ticks, ticks_1, ticks_2, title, grid_spec, color_1, color_2):
    ax = plt.subplot(grid_spec)
    ax = plotter.grouped_vertical_plot(
        ax=ax,
        data=data,
        ticks=ticks,
        ticks_1=ticks_1,
        ticks_2=ticks_2,
        title=title
    )

    return ax


def plots_group(dict_1, dict_2, column_keys, use_columns, fig, label_1=None, label_2=None, sup_title=None, dpi=72,
                truncate=0,
                color_1="#2C7BB6", color_2="#ebba34", show_grid=True, sort=True, columns=2):
    assert len(use_columns) == 3, "chart_ids array length should be 3"

    gs = GridSpec(3, columns, figure=fig)
    fig.suptitle(sup_title, fontweight="bold", fontsize=18)
    axes = []
    max_y = 0
    plot_index = 0

    if gs.get_geometry()[1] == 2:
        for column in use_columns:
            sorted_ticks, sorted_data = sort_dictionary(dict_1, column_keys.index(column), truncate, sort=sort)
            ax = draw_plot(
                data=sorted_data,
                ticks=sorted_ticks,
                title="chart " + column,
                grid_spec=gs[plot_index % 3, 0],
                color=color_1
            )
            max_y = np.maximum(max_y, max(sorted_data))
            axes.append(ax)
            sorted_ticks, sorted_data = sort_dictionary(dict_2, column_keys.index(column), truncate, sort=sort)
            ax = draw_plot(
                data=sorted_data,
                ticks=sorted_ticks,
                title="chart " + column,
                grid_spec=gs[plot_index % 3, 1],
                color=color_2
            )
            max_y = np.maximum(max_y, max(sorted_data))
            axes.append(ax)
            plot_index += 1

    elif gs.get_geometry()[1] == 1:
        for column in use_columns:
            sorted_ticks, sorted_data = merge_series(dict_1, dict_2, column_keys.index(column), sort=sort)
            ax = draw_merged_plot(
                data=sorted_data,
                ticks=sorted_ticks,
                ticks_1=dict_1,
                ticks_2=dict_2,
                title="chart " + column,
                grid_spec=gs[plot_index % 3, 0],
                color_1=color_1,
                color_2=color_2
            )
            max_y = np.maximum(max_y, max(sorted_data))
            axes.append(ax)
            plot_index += 1
            if label_1 is not None or label_2 is not None:
                legend_elements = [
                    Line2D([0], [0], marker='o', color=color_1, label=label_1, lw=0),
                    Line2D([0], [0], marker='o', color=color_2, label=label_2, lw=0),
                ]
                ax.legend(handles=legend_elements)

    else:
        raise Exception("Must have 1 or 2 columns")

    for ax in axes:
        ax.set_ylim([0, max_y + 5])
        for label in ax.get_xticklabels():
            label.set_fontsize(6)
        if show_grid:
            ax.grid(True)
            ax.grid(color="#eeeeee", linestyle='-', linewidth=0.5)
        fig.add_subplot(ax)

    return fig, plt
