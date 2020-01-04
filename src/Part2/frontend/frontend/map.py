import json
from textwrap import dedent as d
from django_plotly_dash import DjangoDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from Color_Console import *
import dash_table

from db.db_utils import get_all_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('map', external_stylesheets=external_stylesheets)

df = get_all_data()
print(df.head())
hotels = df.drop_duplicates('Hotel_Address')
hotels.reset_index(drop=True, inplace=True)


fig = px.scatter_mapbox(hotels, lat="Lat", lon="Lng", hover_name="Hotel_Name", hover_data=["Average_Score", "Total_Number_of_Reviews"],
                        zoom=3, height=1000, size="Total_Number_of_Reviews", color="Average_Score", opacity=1, color_continuous_scale="rdylgn")
fig.update_layout(mapbox_style="dark", mapbox_accesstoken="pk.eyJ1IjoicWxhbmdlZGlqayIsImEiOiJjanRzbnduNTgwcW52M3lsODlvcW5qODduIn0.YWIrTNQehZylJfjo8KfwGA")
fig.update_layout(
    autosize=True,
    margin={"r": 0, "t": 0, "l": 0, "b": 0})

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure=fig
    ),

    html.Div(className='row', children=[
        html.Div(id="click_table"),
])
    ])

@app.callback(
    Output('click_table', 'children'),
    [Input('basic-interactions', 'clickData')])
def display_click(clickData):
    ctext(clickData, "red")
    if clickData:
        hdf = df.loc[df['Hotel_Name'] == clickData['points'][0]['hovertext']]
        hdf = hdf.rename(columns={'Review': 'Review_long'})
        hdf['Review'] = hdf['Review_long'].astype(str).str[0:50]
        hdf = hdf.drop(columns=['Hotel_Address', 'Hotel_Name', 'Lat', 'Lng', 'Average_Score', 'Total_Number_of_Reviews', 'Additional_Number_of_Scoring', 'Review_long'])
        ctext(hdf, "red")
        #reorder
        hdf = hdf[['Review', 'Sentiment', 'Reviewer_Score', 'Review_Date', 'Review_Word_Counts', 'Reviewer_Nationality', 'Total_Number_of_Reviews_Reviewer_Has_Given', 'Tags']]

        ctext(hdf.head(), "red")
        columns = [{"name": i, "id": i} for i in hdf.columns]

        return dash_table.DataTable(
            columns=columns,
            data=hdf.to_dict('records'),
            style_cell={'textAlign': 'left'},
            style_as_list_view=True
        )


if __name__ == '__main__':
    app.run_server(debug=True)