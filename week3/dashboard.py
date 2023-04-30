# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash import callback
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
success_df = spacex_df[spacex_df['Landing Outcome'] == 1].groupby(['Launch Site']).size().reset_index(name='Counts')

# Create a dash application
app = dash.Dash(__name__)
fig = px.pie(success_df, values='Counts', names='Launch Site', title="Total Successful Launches by Site")
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': site, 'value': site} for site in
                                                      ['ALL'] + list(spacex_df['Launch Site'].unique())],
                                             value='ALL',
                                             placeholder="place holder here",
                                             searchable=True
                                             ),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the
                                # site

                                html.Div(dcc.Graph(id='success-pie-chart', figure=fig)),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=min_payload,
                                                max=max_payload,
                                                step=1000,
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_graph(value):
    if value == 'ALL':
        title = "Total Successful Launches by Site"
        dff = success_df
        fig = px.pie(dff, values='Counts', names='Launch Site', title=title)
    else:
        title = f"Success vs. Failed for {value}"
        dff = spacex_df[spacex_df['Launch Site'] == value]['Landing Outcome'].value_counts().reset_index(name='counts')
        fig = px.pie(dff, values='counts', names='Landing Outcome', title=title)
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
)
def update_scatter_chart(site, payload):
    if site == "ALL":
        df = spacex_df
    else:
        df = spacex_df[spacex_df['Launch Site'] == site]

    filtered_df = df[(df['Payload Mass (kg)'] >= payload[0]) & (df['Payload Mass (kg)'] <= payload[1])]
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Landing Outcome')

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
