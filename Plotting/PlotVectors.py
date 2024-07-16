import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D


def draw_vector(a, b, ax, color="#2C7BB6", head_length=6, head_width=4):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    vec_ab_magnitude = np.sqrt(dx ** 2 + dy ** 2)
    dx = dx / vec_ab_magnitude
    dy = dy / vec_ab_magnitude
    # vec_ab_magnitude = vec_ab_magnitude - head_length
    vec_ab_magnitude = vec_ab_magnitude * 5
    ax.arrow(
        a[0],
        a[1],
        vec_ab_magnitude * dx, vec_ab_magnitude * dy,
        head_width=head_width, head_length=head_length,
        fc=color, ec=color)
    return ax


def plot_vect(data_0, data_1, data_2, starting_point, ax, firstValIndex=1, secondValIndex=2, color_2="#2C7BB6",
              color_3="#ebba34", color_1="#000000", ylabel=None, xlabel=None, title=None):
    settings = {
        'axes': ax,
        'uniform': False,
        'aspect': 'auto',
        'font.size': 7,
        'transparent_background': False
    }
    # xy.plot_chromaticity_diagram_CIE1931(standalone=False, cmfs='CIE 1931 2 Degree Standard Observer', show_diagram_colours=True, show_spectral_locus=True, **settings)
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    # ax.spines['left'].set_position(('data', 0.0))
    # ax.spines['bottom'].set_position(('data', 0.0))
    point_1 = [0, 0]
    for vector in data_1:
        point_1[0] += vector[firstValIndex]
        point_1[1] += vector[secondValIndex]
    point_1 = [val / len(data_1) for val in point_1]
    point_1 = [point_1[0] - data_0[firstValIndex], point_1[1] - data_0[secondValIndex]]
    point_2 = [0, 0]
    for vector in data_2:
        point_2[0] += vector[firstValIndex]
        point_2[1] += vector[secondValIndex]
    point_2 = [val / len(data_2) for val in point_2]
    point_2 = [point_2[0] - data_0[firstValIndex], point_2[1] - data_0[secondValIndex]]
    starting_point[firstValIndex] -= data_0[firstValIndex]
    starting_point[secondValIndex] -= data_0[secondValIndex]
    data_0[firstValIndex] = 0
    data_0[secondValIndex] = 0
    V = np.subtract([[starting_point[firstValIndex], starting_point[secondValIndex]], point_1, point_2],
                    [data_0[firstValIndex], data_0[secondValIndex]])
    origin = [[data_0[firstValIndex], data_0[firstValIndex], data_0[firstValIndex]],
              [data_0[secondValIndex], data_0[secondValIndex], data_0[secondValIndex]]]
    ax.quiver(*origin, V[:, 0], V[:, 1], color=[color_1, color_2, color_3], angles='xy', scale_units='xy', scale=1, width=0.01)
    ax.scatter(point_1[0], point_1[1], c="#000000", marker="s", s=120, alpha=1)
    ax.scatter(point_2[0], point_2[1], c="#000000", marker="v", s=120, alpha=1)
    ax.scatter(starting_point[firstValIndex], starting_point[secondValIndex], c="#000000", marker="x", s=120, alpha=1)
    ax.scatter(data_0[firstValIndex], data_0[secondValIndex], c="#000000", s=120, alpha=1)
    # return ax
    # draw_vector(
    #     a=[data_0[firstValIndex], data_0[secondValIndex]],
    #     b=[point_1[0], point_1[1]],
    #     ax=ax,
    #     color=color_1
    # )
    # draw_vector(
    #     a=[data_0[firstValIndex], data_0[secondValIndex]],
    #     b=[point_2[0], point_2[1]],
    #     ax=ax,
    #     color=color_2
    # )
    # ax.set_xlim([-128, 127])
    # ax.set_ylim([-128, 127])
    ax.tick_params(axis='both', labelsize=20)
    if xlabel is not None:
        ax.set_xlabel(xlabel, fontweight="bold", fontsize=20, position=(0, 0))
    if ylabel is not None:
        ax.set_ylabel(ylabel, rotation=0, fontweight="bold", fontsize=20, position=(0, 0))
    if title is not None:
        ax.set_title(title)
    return ax


def plot_three_charts(data_0, data_1, data_2, starting_point, fig, axes, label_0, label_1, label_2, charts_to_plot,
                      data_indexes=[0, 1], ylabel=None, xlabel=None,
                      sup_title=None, color_1="#2C7BB6", color_2="#ebba34"):
    legend_elements = [
        Line2D([0], [0], marker='o', color=color_1, label=label_1, lw=0),
        Line2D([0], [0], marker='o', color=color_2, label=label_2, lw=0),
        Line2D([0], [0], marker='s', color='#000000', label=label_1+' mean', lw=0),
        Line2D([0], [0], marker='v', color='#000000', label=label_2+' mean', lw=0),
        Line2D([0], [0], marker='o', color='#000000', label='target color', lw=0),
        Line2D([0], [0], marker='x', color='#000000', label='starting color', lw=0),
    ]

    row = 0
    for chart_id in charts_to_plot:
        plot_vect(
            data_0=data_0[chart_id],
            data_1=data_1[chart_id],
            data_2=data_2[chart_id],
            starting_point=starting_point[chart_id],
            firstValIndex=data_indexes[0],
            secondValIndex=data_indexes[1],
            ax=axes[row],
            # title=f"chart {chart_id}",
            # ylabel=ylabel,
            # xlabel=xlabel
        )
        row += 1
    fig.suptitle(sup_title, fontweight="bold", fontsize=18)
    fig.legend(handles=legend_elements)
    # plt.subplots_adjust(top=2)
    plt.tight_layout()
