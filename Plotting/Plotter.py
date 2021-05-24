import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from Plotting import Plots as plotter


def plot_style_1(data_1, data_2, label_1, label_2, x_labels, fig, sup_title=None, ylabel=None, xlabel='chart_id', dpi=72, figsize=(8.27, 11.69)):
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
        title="median" if ylabel is None else "median "+ylabel,
        xlabel=xlabel,
        group_each=3
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
        group_each=3
    )
    ax4.grid(True)
    ax4.grid(color="#eeeeee", linestyle='-', linewidth=0.5)

    fig.add_subplot(ax1)
    fig.add_subplot(ax2)
    fig.add_subplot(ax3)
    fig.add_subplot(ax4)

    plt.tight_layout()

    return plt


def plot_style_2(data, x_labels, sup_title=None, ylabel=None, xlabel='chart_id', dpi=72, figsize=(8.27, 11.69), group_each=0):
    fig = plt.figure(figsize=figsize, dpi=dpi)
    gs = GridSpec(5, 2, figure=fig)

    fig.suptitle(sup_title, fontweight="bold", fontsize=18)

    ax1 = plotter.simple_boxplot(
        ax=plt.subplot(gs[:2, :]),
        parsed_data=data,
        ticks=x_labels,
        ylabel=ylabel,
        showfliers=True
    )
    ax1.grid(True)
    ax1.grid(color="#eeeeee", linestyle='-', linewidth=0.5)

    ax2 = plotter.simple_boxplot(
        ax=plt.subplot(gs[2, :]),
        parsed_data=data,
        ticks=x_labels,
        ylabel=ylabel,
        showfliers=False
    )
    ax2.grid(True)
    ax2.grid(color="#eeeeee", linestyle='-', linewidth=0.5)

    ax3 = plotter.simple_plot(
        ax=plt.subplot(gs[-2:, 0]),
        data=plotter.get_median(data, chart_ids=x_labels),
        ticks=x_labels,
        title="median" if ylabel is None else "median "+ylabel,
        xlabel=xlabel,
        group_each=group_each
    )
    ax3.grid(True)
    ax3.grid(color="#eeeeee", linestyle='-', linewidth=0.5)

    ax4 = plotter.simple_plot(
        ax=plt.subplot(gs[-2:, -1]),
        data=plotter.get_var_coeff(data, chart_ids=x_labels),
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