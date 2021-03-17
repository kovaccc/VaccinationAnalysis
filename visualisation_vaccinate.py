# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


# Visualization Imports
import pandas as pd
import pandas_profiling as pp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns
color = sns.color_palette()
sns.set_context('talk')
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.express as px

# read csv
vaccination_df = pd.read_csv("C:\RProjects\country_vaccinations.csv")

# return only rows for Croatia 
countries = ["Croatia"]
vaccination_croatia_df = vaccination_df.query("country==@countries")

# first 5 rows
print(vaccination_croatia_df.head())

# statics about missing variables, certain values for rows, number of rows etc.
report = pp.ProfileReport(vaccination_croatia_df)
report.to_file("report_before_clean.html")
    

# first example - daily vaccination (processed not raw)

# get data for certain columns
vaccination_croatia_daily_df = vaccination_croatia_df[['date', 'daily_vaccinations']]
print(vaccination_croatia_daily_df)

# statics about missing variables, certain values for rows, number of rows etc.
report_for_daily_vacc = pp.ProfileReport(vaccination_croatia_daily_df)
report_for_daily_vacc.to_file("report_for_daily_vacc.html")

# we won't use median, mode, mean to replace empty columns since for
# this data is important to be correct (it represents daily vaccinate we should not make up some random value)
# instead we are going to delete rows with empty cells 

#drop rows with missing cells
cleaned_vaccination_croatia_daily_df = vaccination_croatia_daily_df.dropna()
print(cleaned_vaccination_croatia_daily_df)


#visualize daily vaccination
plt.figure(figsize=(40,10)) #change size of plot
plt.scatter(cleaned_vaccination_croatia_daily_df['date'], 
            cleaned_vaccination_croatia_daily_df['daily_vaccinations'])
plt.title('Daily Vaccinations in Croatia')
plt.xlabel("date")
plt.ylabel("daily_vaccinations")
plt.gcf().autofmt_xdate()

# count number of rows in dataset
count_row = cleaned_vaccination_croatia_daily_df.shape[0]

# we will show every second date so x axis won't became too densely
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(2))

# show plot
plt.show()





# second example - comparing total_vaccinations, 
# people_vaccinated, people_fully_vaccinated

# get data for certain columns
vaccination_croatia_total_df = vaccination_croatia_df[['date', 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated']]
print(vaccination_croatia_total_df)

# statics about missing variables, certain values for rows, number of rows etc.
report_for_total_vacc = pp.ProfileReport(vaccination_croatia_total_df)
report_for_total_vacc.to_file("report_for_total_vacc.html")


# we won't use median, mode, mean to replace empty columns since for
# this data is important to be correct (it represents total vaccinate we should not make up some random value)
# instead we are going to delete rows with empty cells 

#drop rows with missing cells
cleaned_vaccination_croatia_total_df = vaccination_croatia_total_df.dropna()
print(cleaned_vaccination_croatia_total_df)



# Create a grouped bar chart, with date as the x-axis

# size
fig, ax = plt.subplots(figsize=(50, 10))

# Our x-axis. We basically just want a list
x = np.arange(len(cleaned_vaccination_croatia_total_df['date']))

# Define bar width. We need this to offset the second and third bar.
bar_width = 0.4

b1 = ax.bar(x, cleaned_vaccination_croatia_total_df['total_vaccinations'],
            width=bar_width/2, label='total_vaccinations')
# Same thing, but offset the x.
b2 = ax.bar(x + bar_width/2, cleaned_vaccination_croatia_total_df['people_vaccinated'],
            width=bar_width/2, label='people_vaccinated')


b3 = ax.bar(x + bar_width, cleaned_vaccination_croatia_total_df['people_fully_vaccinated'],
            width=bar_width/2, label='people_fully_vaccinated')


# Fix the x-axes.
ax.set_xticks(x + bar_width/2)
ax.set_xticklabels(cleaned_vaccination_croatia_total_df['date'])

# Add legend.
ax.legend()

# Axis styling.
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#DDDDDD')
ax.tick_params(bottom=False, left=False)
ax.set_axisbelow(True)
ax.yaxis.grid(True, color='#EEEEEE')
ax.xaxis.grid(False)

# Add axis and chart labels.
ax.set_xlabel('date', labelpad=15)
ax.set_ylabel('vaccinations', labelpad=15)
ax.set_title('Daily vaccination comparing', pad=15)

# For each bar in the chart, add a text label.
for bar in ax.patches:
  # The text annotation for each bar should be its height.
  bar_value = bar.get_height()
  # Format the text with commas to separate thousands. You can do
  # any type of formatting here though.
  text = f'{bar_value:,}'
  # This will give the middle of each bar on the x-axis.
  text_x = bar.get_x() + bar.get_width() / 2
  # get_y() is where the bar starts so we add the height to it.
  text_y = bar.get_y() + bar_value
  # If we want the text to be the same color as the bar, we can
  # get the color like so:
  bar_color = bar.get_facecolor()
  # If you want a consistent color, you can just set it as a constant, e.g. #222222
  ax.text(text_x, text_y, text, ha='center', va='bottom', color=bar_color,
          size=10)


fig.tight_layout()




