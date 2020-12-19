
#parsing data from the website

import requests 
from bs4 import BeautifulSoup

#url of the website from where the data to be scraped
url = "https://www.estesparkweather.net/archive_reports.php?date=202011"

response = requests.get(url)
print(response)

soup = BeautifulSoup(response.content, 'html.parser')

print(soup)

table_data = soup.find_all('table')
print(table_data)

#getting the data in usable format

import re
from datetime import datetime


outer_table_data = []
for i in range(30):
    value = list(filter(lambda x: x if x!=None else '', table_data[i].text.splitlines()))
    outer_table_data.append(value)

print(outer_table_data[0])


#creating a 2D list of all the features

final_list = []
for x in outer_table_data:
    numerical = []
    for y in x[1:]: 
        numerical.append(".".join(re.findall('\d+', str(y.split()[:5]))))
    final_list.append(numerical)
    
print(final_list[0])

# creating a dataframe of this 2D list

import pandas as pd

columns = ['Avg_temp', 'Avg_humidity', 'Avg_dewpoint', 'Avg_barometer', 'Avg_windspeed',
           'Avg_gustspeed', 'Avg_direction', 'Rainfall_for_month', 'Rainfall_for_year', 
           'max_rain_per_min', 'max_temp', 'min_temp', 'max_humidity', 'min_humidity', 
           'max_pressure', 'min_pressure', 'max_windspeed', 'max_gustspeed', 'max_heat_index']

weather_data = pd.DataFrame(final_list, columns=columns)
weather_data['Date'] = pd.date_range('2020-11-01', '2020-11-30')
weather_data[columns] = weather_data[columns].apply(pd.to_numeric)

# sending the file data to a csv file
weather_data.to_csv('weather_data(nov2020).csv', index = False)
