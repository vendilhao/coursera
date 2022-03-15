# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_geo.csv")
cols =['Flight','Number','Date,Time (UTC)','Booster_Version',
       'Launch_Site','Payload','PAYLOAD_MASS__KG_','Orbit',
       'Customer','Mission Outcome','Landing Outcome','class','Lat','Long']
spacex_df.columns=cols
max_payload = spacex_df['PAYLOAD_MASS__KG_'].max()
min_payload = spacex_df['PAYLOAD_MASS__KG_'].min()

# Create a dash application
app = dash.Dash(__name__)

launchsites = spacex_df['Launch_Site'].unique().tolist()
ls_sites = []
ls_sites.append({'label': 'All_L_Sites', 'value': 'All_L_Sites'})
for LS in launchsites:
    ls_sites.append({'label': LS , 'value': LS })

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site_dropdown',options=ls_sites,placeholder='Launch_Site', searchable = True , value = 'All_L_Sites'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                
                                html.P("PAYLOAD_MASS__KG_:"),

                                dcc.RangeSlider(id='payload_slider',min=0,max=10000,step=1000,marks = {
                                            0: '0kg',
                                            1000: '1000kg',
                                            2000: '2000kg',
                                            3000: '3000kg',
                                            4000: '4000kg',
                                            5000: '5000kg',
                                            6000: '6000kg',
                                            7000: '7000kg',
                                            8000: '8000kg',
                                            9000: '9000kg',
                                            10000: '10000kg'
                                    },

                                    value=[min_payload,max_payload]
                                ),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
     Output(component_id='success-pie-chart',component_property='figure'),
     [Input(component_id='site_dropdown',component_property='value')]
)

def update_graph(site_dropdown):
    if (site_dropdown == 'All_L_Sites'):
        df  = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(df, names = 'Launch_Site',hole=.3,title = 'Total Success Launches By all sites')
    else:
        df  = spacex_df.loc[spacex_df['Launch_Site'] == site_dropdown]
        fig = px.pie(df, names = 'class',hole=.3,title = 'Total Success Launches for site ' + site_dropdown)
    return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
     Output(component_id='success-payload-scatter-chart',component_property='figure'),
     [Input(component_id='site_dropdown',component_property='value'),Input(component_id="payload_slider", component_property="value")]
)
def update_scattergraph(site_dropdown,payload_slider):
    if site_dropdown == 'All_L_Sites':
        low, high = payload_slider
        df  = spacex_df
        mask = (df['PAYLOAD_MASS__KG_'] > low) & (df['PAYLOAD_MASS__KG_'] < high)
        fig = px.scatter(
            df[mask], x="PAYLOAD_MASS__KG_", y="class",
            color="Booster_Version",
            size='PAYLOAD_MASS__KG_',
            hover_data=['PAYLOAD_MASS__KG_'])
    else:
        low, high = payload_slider
        df  = spacex_df.loc[spacex_df['Launch_Site'] == site_dropdown]
        mask = (df['PAYLOAD_MASS__KG_'] > low) & (df['PAYLOAD_MASS__KG_'] < high)
        fig = px.scatter(
            df[mask], x="PAYLOAD_MASS__KG_", y="class",
            color="Booster_Version",
            size='PAYLOAD_MASS__KG_',
            hover_data=['PAYLOAD_MASS__KG_'])
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
