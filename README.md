# Simultaneous contrast plotter
This repo contains some Python (>= Python 3.7) scripts to organize,
parse and plot data generated by the simultaneous contrast perception
test available
<a href="https://github.com/imwaffe/simultaneous-contrast">here on GitHub</a>.
## Usage
### Organize data
To group test results in different directories based on the answers
in the <b>user_details.txt</b> file, simply execute <b><u>Organizer.py</u></b>.<br>
The script will ask for the path of the directory containing all
test results and the path where to copy the sorted data, then it will
ask to organize data by <i>"user_is_colorblind"</i>, <i>"user_gender"</i> or
<i>"user_works_with_colors"</i>.<br><br>
### Parse data
Executing <b><u>CSVParser.py</u></b> will create a single CSV file
containing the chosen parameter (for example "<i>hsl_dist</i>")
values for each user and each chart.<br>
Resulting data is organized like a table, with chart_ids as rows and
user_ids as columns.<br>
### Plot data
Executing <b><u>CSVPlotter.py</u></b> will create a lot of different plots
grouped by user, chart, and specific parameters.<br>
The usage is similar to <b>Organizer.py</b> and <b>CSVParser.py</b>
scripts.<br>
- In folder <i>ab_scatter_plots</i> will be created a scatter plot
for each chart in (a*,b*) space based on the color chosen by the user.<br>
- In folder <i>by_chart</i> will be created a figure for each parameter,
each figure contains two box-plots, one displaying and another not
displaying outliers, and two plots with the median value and
coefficient of variation.
- In folders <i>by_user</i> and <i>by_user_grouped</i> will be created
plots with the with the distance between the actual color and the
color picked by the user for each parameter and for each chart.

In the generated plots data is grouped in <i>"colorblinds"</i> and
<i>"non colorblinds"</i> based on the <i>"user_is_colorblind"</i>
value in <b>user_details.txt</b>, but note that this field contains
the answer the user gave to the question <i>"Have you ever had
issues with colours vision?"</i>, so there is no certainty that
a user answering "yes" is actually colorblind or vice versa.<br>
Please note also that both the users who answered "yes" and
the ones who answered "unsure" are put together in the
"colorblinds" group.

The usage is similar to that of <b>Organizer.py</b> script.