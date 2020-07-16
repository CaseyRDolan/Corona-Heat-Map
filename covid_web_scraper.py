# -*- coding: utf-8 -*-
"""CoronaWebScraper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ec0V_9HDSDcn5Tk20ztta8HclhC5wzQR
"""

!pip install country_converter
import country_converter as coco
import csv
import requests
from bs4 import BeautifulSoup

# Object to hold info for individual states/countries/counties (name, total
# cases, new cases, total deaths, new deaths and active cases)
class State:
  def __init__(self, name, total_cases, new_cases, total_deaths, new_deaths, active_cases):
    self.name = name
    self.total_cases = total_cases if total_cases != "" else '0'
    self.new_cases = new_cases if new_cases != "" else '0'
    self.total_deaths = total_deaths if total_deaths != "" else '0'
    self.new_deaths = new_deaths if new_deaths != "" else '0'
    self.active_cases = active_cases if active_cases != "" else '0'

  def __str__(self):
    return f'{self.name}\nTotal Cases: {self.total_cases}\nNew Cases Today: {self.new_cases}\nTotal Deaths: {self.total_deaths}\nDeaths Today: {self.new_deaths}\nActive Cases: {self.active_cases}'

def get_abbr(state):
  us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District Of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
  } 
  return us_state_abbrev[state.rstrip()]
# Function to scrape COVID-19 data from the Worldometers website for each state
def scrape_state_data():

  data = []
  filename = 'state_data.csv'
  URL = 'https://www.worldometers.info/coronavirus/country/us/'
  page = requests.get(URL) # Visit Worldometers site and download HTML
  soup = BeautifulSoup(page.content, 'html.parser') # Parse HTML content

  # List of HTML data for each state
  states = soup.find(id='usa_table_countries_today').find('tbody').find_all('tr')
  states.pop(0) # Remove first entry (USA Total)

  # Write to .csv file
  with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Name', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Active Cases'])
    # For each state, extract data, create a new State object and add it to data
    for state in states:
      numbers = state.find_all('td')
      new_data = [get_abbr(numbers[0].text.strip('\n')), numbers[1].text.strip('\n').replace(',', ''),\
                       numbers[2].text.strip('\n'), numbers[3].text.strip('\n'),\
                       numbers[4].text.strip('\n'), numbers[5].text.strip('\n')]
      data.append(new_data)

    csvwriter.writerows(data)


# Function to scrape COVID-19 data from worldometers website for each Country
def scrape_country_data():
  cc = coco.CountryConverter()
  data = []
  filename = 'country_data.csv'
  URL = 'https://www.worldometers.info/coronavirus/#countries'
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, 'html.parser') # Parse HTML content

  # List of HTML data for each country
  countries = soup.find(id='main_table_countries_today').find('tbody').find_all('tr')
  # Remove Data from non-countries (ships)
  for i in range(8):
    countries.pop(0)

  with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Name', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Active Cases'])
    # For each country, extract data, create a new State object and add it to data
    for country in countries:
      numbers = country.find_all('td')
      new_data = [cc.convert(names = numbers[1].text.strip('\n'), to = 'ISO3'), numbers[2].text.strip('\n').replace(',', ''),\
                      numbers[3].text.strip('\n'), numbers[4].text.strip('\n'),\
                      numbers[5].text.strip('\n'), numbers[6].text.strip('\n')]
      data.append(new_data)

    csvwriter.writerows(data)

scrape_state_data()
scrape_country_data()

import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('state_data.csv')

fig = go.Figure(data=go.Choropleth(
    locations=df['Name'],
    z = df['Total Cases'],
    locationmode = 'USA-states',
    colorscale = 'Reds',
    colorbar_title = "Total Cases"
))

fig.update_layout(
    title_text = 'Total Confirmed COVID-19 Cases by State',
    geo_scope = 'usa'
)

fig.show()

df = pd.read_csv('country_data.csv')
fig = go.Figure(data=go.Choropleth(
    locations = df['Name'],
    z = df['Total Cases'],
    locationmode = 'ISO-3',
    colorscale = 'Reds',
    colorbar_title = "Total Cases"
))

fig.update_layout(
    title_text = 'Total Confirmed COVID-19 Cases by Country'
)

fig.show()