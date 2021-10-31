import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
import altair as alt


def extract(path):
    df = pd.read_csv(path, header=None)
    return df.mean(axis=0).loc[0]


df = pd.DataFrame()
path = os.getcwd() + '/04'
files = os.listdir(path)
for file in files:
    path2 = path + '/' + file
    files2 = os.listdir(path2)
    daylist = []
    power = []
    for file2 in files2:
        daylist.append(file2[0:10])
        power.append(extract(path2+'/'+file2))
    this = pd.DataFrame([power], columns=daylist)
    df = pd.concat([df, this], axis=0, ignore_index=True)

cols = df.columns.tolist()
cols.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))

df = df[cols]
df = df.dropna(axis=1)
df = df.set_axis(['Fridge', 'Kitchen appliances', 'Lamp', 'Stereo and laptop',
                  'Freezer', 'Tablet', 'Entertainment', 'Microwave'], axis='index')
df = df.T
df.index.name = 'Date'
df = df.reset_index().melt('Date', var_name='Appliance', value_name='Power(Watt)')
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['Date'], empty='none')

# The basic line
line = alt.Chart(df).mark_line(interpolate='basis').encode(
    alt.X('Date:T', axis=alt.Axis(grid=False)),
    y='Power(Watt):Q',
    color='Appliance:N'
).properties(
    title={
      "text": ['Power Consumed of Appliances By Date'],
      "subtitle": ["Data from 4th household of ECO dataset"]
    }
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
).add_selection(
    nearest
)

# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'Power(Watt):Q', alt.value(' '))
)

# Draw a rule at the location of the selection
rules = alt.Chart(df).mark_rule(color='gray').encode(
    x='Date:T',
).transform_filter(
    nearest
)

# Put the five layers into a chart and bind the data
chart = alt.layer(
    line, points, rules, text
).properties(
    width=800, height=300
).configure_view(
    strokeWidth=0
)
chart.save('altair.html')
