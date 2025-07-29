# Import libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load your data
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Create the app
app = dash.Dash(__name__)

# Get min and max payload for slider
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# App layout
app.layout = html.Div([
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            *[{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]
        ],
        value='ALL',
        placeholder="Select a Launch Site",
        searchable=True
    ),

    html.Br(),

    dcc.Graph(id='success-pie-chart'),

    html.Br(),

    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={int(i): str(int(i)) for i in range(int(min_payload), int(max_payload)+1, 2500)},
        value=[min_payload, max_payload]
    ),
])

# Callback for pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site',
                     title='Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class',
                     title=f'Total Success vs. Failure for site {entered_site}')
    return fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
