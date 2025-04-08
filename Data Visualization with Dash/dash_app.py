#!/usr/bin/env python
# coding: utf-8

import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# TASK 2.1: Create Dash application with meaningful title
app.title = "Automobile Sales Statistics Dashboard"

# Create dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
year_list = [i for i in range(1980, 2024, 1)]

# TASK 2.2: Create layout with dropdowns
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a report type'
        )
    ], style={'width': '50%', 'display': 'inline-block'}),
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=1980,
            placeholder='Select a year'
        )
    ], style={'width': '50%', 'display': 'inline-block'}),
    # TASK 2.3: Add division for output
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flex-wrap': 'wrap'})
])

# TASK 2.4: Create callbacks
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# Main callback for plotting
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        # TASK 1.1 & 2.5: Line chart for sales fluctuation
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales Fluctuation over Recession Periods"))

        # TASK 1.2: Different lines for vehicle types
        vehicle_rec = recession_data.groupby(['Year', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.line(vehicle_rec,
                x='Year',
                y='Automobile_Sales',
                color='Vehicle_Type',
                title="Sales Trends by Vehicle Type During Recession"))

        # TASK 1.8: Pie chart for advertising expenditure by vehicle type
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Advertising Expenditure Share by Vehicle Type During Recession"))

        # TASK 1.9: Line plot for unemployment effect
        unemp_data = recession_data.groupby(['Year', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.line(unemp_data,
                x='Year',
                y='Automobile_Sales',
                color='Vehicle_Type',
                title='Effect of Unemployment Rate on Vehicle Sales'))

        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[R_chart3, R_chart4], style={'display': 'flex'})
        ]

    elif selected_statistics == 'Yearly Statistics' and input_year:
        yearly_data = data[data['Year'] == input_year]
        
        # TASK 1.1 & 2.6: Yearly sales line chart
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas,
                x='Year',
                y='Automobile_Sales',
                title='Yearly Automobile Sales'))

        # TASK 1.5: Bubble plot for seasonality
        monthly_data = data.groupby(['Month', 'Year'])['Automobile_Sales'].mean().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.scatter(monthly_data,
                x='Month',
                y='Automobile_Sales',
                size='Automobile_Sales',
                color='Year',
                title='Seasonality Impact on Automobile Sales'))

        # TASK 1.3: Seaborn-style comparison (using Plotly equivalent)
        vehicle_data = data.groupby(['Vehicle_Type', 'Recession'])['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(vehicle_data,
                x='Vehicle_Type',
                y='Automobile_Sales',
                color='Recession',
                barmode='group',
                title='Sales Trend: Recession vs Non-Recession'))

        # TASK 1.7: Pie chart for advertising expenditure
        exp_data = data.groupby('Recession')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data,
                values='Advertising_Expenditure',
                names='Recession',
                title='Advertising Expenditure: Recession vs Non-Recession'))

        return [
            html.Div(className='chart-item', children=[Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[Y_chart3, Y_chart4], style={'display': 'flex'})
        ]
    else:
        return None

# Additional standalone plots using Matplotlib
# TASK 1.4: GDP subplots
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(data[data['Recession'] == 1]['Year'], data[data['Recession'] == 1]['GDP'])
plt.title('GDP During Recession')
plt.subplot(1, 2, 2)
plt.plot(data[data['Recession'] == 0]['Year'], data[data['Recession'] == 0]['GDP'])
plt.title('GDP During Non-Recession')
plt.tight_layout()
plt.savefig('gdp_comparison.png')

# TASK 1.6: Scatter plot for price vs sales correlation
plt.figure(figsize=(10, 6))
plt.scatter(data[data['Recession'] == 1]['Price'], data[data['Recession'] == 1]['Automobile_Sales'])
plt.xlabel('Average Vehicle Price')
plt.ylabel('Automobile Sales')
plt.title('Price vs Sales Correlation During Recession')
plt.savefig('price_sales_correlation.png')

if __name__ == '__main__':
    app.run(debug=True)