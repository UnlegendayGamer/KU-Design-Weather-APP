import matplotlib.pyplot as plt
import numpy as np
from readfile import getDict

WANTED_DATA = 'temperature_min'

data = {}
datadict = getDict("weatherdata.txt")
datalist = datadict.get(WANTED_DATA + ":")

for i, val in enumerate(datalist):
    data[i+1] = float(val)

namedict = {"date":"Date","weather_code":"Weather Code","temperature_max":"Max Temperature","temperature_min":"Min Temperature"}

categories = list(data.keys())
values = list(data.values())

# Create the histogram
plt.bar(categories, values, color='g', alpha=0.7)


# Add labels and title

plt.xlabel('Days')
plt.ylabel(namedict.get(WANTED_DATA))
plt.title(namedict.get(WANTED_DATA) + ' for Each Day')

# Show the plot
plt.savefig('my_plot.png')