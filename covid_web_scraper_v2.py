import plotly.graph_objects as go
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import country_converter as coco
import csv
import requests
from bs4 import BeautifulSoup

app = dash.Dash()

app.layout = html.Div([
    # Div to hold the two dropdown menus
    html.Div([
        # Dropdown to select the scope of the heatmap
        html.Label(["Select scope", dcc.Dropdown(
            id = 'scope_menu',
            options=[
                {
                    "label": "Global",
                    "value": "orthographic",
                },
                {
                    "label": "United States",
                    "value": "USA-states",
                },
            ],
            value='orthographic',
            clearable=False),
        ]),
        # Dropdown to select the metric to view for the heatmap
        html.Label(["Select metric", dcc.Dropdown(
            id = 'metric_menu',
            options=[
                {
                    "label": "Total Cases",
                    "value": "Total Cases"
                },
                {
                    "label": "New Cases Today",
                    "value": "New Cases"
                },
                {
                    "label": "Total Deaths",
                    "value": "Total Deaths"
                },
                {
                    "label": "New Deaths Today",
                    "value": "New Deaths"
                },
                {
                    "label": "Active Cases",
                    "value": "Active Cases"
                }
            ],
            value='Active Cases',
            clearable=False),
        ]),
    ]),
    # Heatmap to display
    dcc.Graph(id = "heatmap"),
    # Interval component to update data every 10 seconds
    dcc.Interval(
        id = 'interval-component',
        interval = 10000,
        n_intervals = 0
    )
])

# Callback to update heatmap every 10 seconds and after every metric/scope change
@app.callback(
    Output('heatmap', 'figure'),
    [
        Input('metric_menu', 'value'),
        Input('scope_menu', 'value'),
        Input('interval-component', 'n_intervals')
    ]
)
# Function to update heatmap from callback
def update_figure(metric, scope, n):
    if scope == "USA-states":
        scrape_state_data()
    else:
        scrape_country_data()
        
    if metric == "Total Cases":
        return drawMap("Total Cases", "Total Confirmed COVID-19 Cases", scope)
    elif metric == "Active Cases":
        return drawMap("Active Cases", "Total Active COVID-19 Cases", scope)
    elif metric == "Total Deaths":
        return drawMap(metric, "Total Deaths Attributed to COVID-19", scope)
    elif metric == "New Deaths":
        return drawMap(metric, "Total Deaths Attributed to COVID-19 Today", scope)
    else: 
        return drawMap("New Cases", "Total New COVID-19 Cases Today", scope)


# Function to get abbreviated state code of a US state
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
        csvwriter.writerow(['Code', 'Name', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Active Cases'])
        
        # For each state, extract data, create a new State object and add it to data
        for state in states:
            numbers = state.find_all('td')
            new_data = [get_abbr(numbers[0].text.strip('\n')),
                      numbers[0].text.strip('\n'),
                      numbers[1].text.strip('\n').replace(',', ''),
                      numbers[2].text.strip('\n').replace(',', ''),
                      numbers[3].text.strip('\n').replace(',', ''),
                      numbers[4].text.strip('\n').replace(',', ''),
                      numbers[5].text.strip('\n').replace(',', '')]
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
    # Remove Data from non-countries (global total, continents, ships)
    for i in range(8):
        countries.pop(0)
    
    # Open a file for writing as a .csv
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write .csv headers 
        csvwriter.writerow(['Code', 'Name', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Active Cases'])
        # For each country, extract data and write it to the .csv
        for country in countries:
            numbers = country.find_all('td')
            name = numbers[1].text.strip('\n')
            # Ignore ships in countries list
            if name == 'Diamond Princess' or name == 'MS Zaandam' or name == 'Channel Islands':
                continue
            #Special conversions for countries with improperly formatted names
            if name == 'UK':
                name = 'United Kingdom'
            elif name == 'UAE':
                name = 'United Arab Emirates'
            elif name == 'DRC':
                name = 'Democratic Republic of the Congo'
            elif name == 'CAR':
                name = 'Central African Republic'
            # Convert country name to ISO-3 country code for mapping
            code = cc.convert(names = name, to = 'ISO3')
            # Add country data to a list as list of strings
            new_data = [code, cc.convert(names = code, to = 'name_short'),
                      numbers[2].text.strip('\n').replace(',', ''),
                      numbers[3].text.strip('\n').replace(',', ''),
                      numbers[4].text.strip('\n').replace(',', ''),
                      numbers[5].text.strip('\n').replace(',', ''),
                      numbers[8].text.strip('\n').replace(',', '')]
            data.append(new_data)
        # Write all country data to .csv
        csvwriter.writerows(data)


# Function to create a plotly choropleth map
def drawMap(metric, title_text, scope):
    # Format for scope (US/Global)
    if scope == 'USA-states':
        df = pd.read_csv('state_data.csv')
        title_ending = ' by US State'
    else:
        df = pd.read_csv('country_data.csv')
        title_ending = ' by Country'
    
    # Create figure
    fig = go.Figure(data=go.Choropleth(
        locations=df['Code'],
        hovertemplate = '%{text}<br>%{z:,}<br><br><extra></extra>',
        text = df['Name'],
        z = df[metric],
        locationmode = scope if scope == 'USA-states' else 'ISO-3',
        colorscale = 'Reds',
        colorbar_title = metric,
        marker_line_color = 'gray',
        marker_line_width = .5
    ))
    # Give figure style
    fig.update_layout(
        title_text = '<b>' + title_text + title_ending,
        geo=dict(
            resolution = 50,
            scope = 'usa' if scope == 'USA-states' else 'world',
            showframe=False,
            showcoastlines=False,
            projection_type = scope if scope == 'orthographic' else 'albers usa'
        ),
        autosize = True,
        width = 1600,
        height = 900
    )
    
    return fig
  
  
if __name__ == '__main__':
  scrape_state_data()
  scrape_country_data()
  drawMap("Active Cases", "Total Active COVID-19 Cases", "orthographic")
  app.run_server(debug=True)
  