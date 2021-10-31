import plotly.express as px
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def extract(path):
    df = pd.read_csv(path, header=None)
    list = []
    for j in range(24):
        length = 3600
        list.append(df[j*length:(j+1)*length].mean(axis=0).loc[0])
    return list


path = os.getcwd() + '/04'
files = os.listdir(path)
# print(files)         # ['01', '02', '03', '04', '05', '06', '07', '08']
allaverage = []     # size of 8*864
for file in files:
    path2 = path + '/' + file
    files2 = os.listdir(path2)
    daylist = []
    for file2 in files2:
        daylist.append(extract(path2+'/'+file2))
    daylist = np.array(daylist)
    allaverage.append(daylist.mean(axis=0))
print(len(allaverage))
print(len(allaverage[0]))
fig = px.imshow(allaverage, labels=dict(x='Time in Day(hr)', y='Appliance',
                color='Consumption(Watt)'), x=[str(i) for i in range(24)],
                y=['Fridge', 'Kitchen appliances', 'Lamp', 'Stereo and laptop',
                'Freezer', 'Tablet', 'Entertainment', 'Microwave'])
fig.update_layout(title_text="Average Power Appliances Consumption Per Hour",
                  title_x=0.5)
fig.update_xaxes(title_text="Time in Day(hr) <br> Data from 4th household of ECO dataset")
fig.write_html("plotly.html")
