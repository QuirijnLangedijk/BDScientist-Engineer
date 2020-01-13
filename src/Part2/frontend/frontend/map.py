from django_plotly_dash import DjangoDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from Color_Console import *
import dash_table
import pandas as pd

import db.db_utils as db

external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']
app = DjangoDash('map', external_stylesheets=external_stylesheets)

df = None


def make_map(min_score=8, max_score=10):
    global df
    df = None
    df = db.execute_query('all_data',     [
        {
            "$match": {
                "$and": [
                    {
                        "Average_Score": {
                            "$gte": min_score
                        }
                    },
                    {
                        "Average_Score": {
                            "$lte": max_score
                        }
                    }
                ]
            }
        },
        {
            "$group": {
                "_id": {
                    "Lng": "$Lng",
                    "Total_Number_of_Reviews": "$Total_Number_of_Reviews",
                    "Lat": "$Lat",
                    "Average_Score": "$Average_Score",
                    "Hotel_Name": "$Hotel_Name"
                }
            }
        },
        {
            "$project": {
                "Hotel_Name": "$_id.Hotel_Name",
                "Lat": "$_id.Lat",
                "Lng": "$_id.Lng",
                "Total_Number_of_Reviews": "$_id.Total_Number_of_Reviews",
                "Average_Score": "$_id.Average_Score",
                "_id": 0
            }
        }
    ]
    )

    zero_hotel = [['TestHotel', 0, 0, 1, 0], ['TestHotel2', 0, 0, 1, 10]]
    zero_hotel_df = pd.DataFrame(data=zero_hotel, columns=['Hotel_Name', 'Lat', 'Lng', 'Total_Number_of_Reviews', 'Average_Score'])
    df = df.append(zero_hotel_df)

    print(df)

    fig = px.scatter_mapbox(df, lat="Lat", lon="Lng", hover_name="Hotel_Name", hover_data=["Average_Score", "Total_Number_of_Reviews"],
                            zoom=3, height=1000, size="Total_Number_of_Reviews", color="Average_Score", opacity=1, color_continuous_scale="rdylgn")
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken="pk.eyJ1IjoicWxhbmdlZGlqayIsImEiOiJjanRzbnduNTgwcW52M3lsODlvcW5qODduIn0.YWIrTNQehZylJfjo8KfwGA")
    fig.update_layout(
        autosize=True,
        margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


app.layout = html.Div(
    html.Div([
        # Selectors
        html.Div(
            [
                html.Div(
                    [
                        html.P('Rating:'),
                        dcc.RangeSlider(
                            id='rating_range',
                            min=0,
                            max=10,
                            step=0.1,
                            marks={
                                0: '0',
                                1: '1',
                                2: '2',
                                3: '3',
                                4: '4',
                                5: '5',
                                6: '6',
                                7: '7',
                                8: '8',
                                9: '9',
                                10: '10'
                            },
                            value=[8, 10]
                        )
                    ],
                    className='six columns',
                    style={'marginTop': 30, 'marginBottom': 30}
                )
            ],
            className='row'
        ),

        # Map + table + Histogram
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id='map',
                            figure=make_map()
                        ),
                    ], className = "six columns"
                ),
                html.Div([
                    ], className= 'twelve columns'),
                html.Div(className='row', children=[
                    html.Div(id="click_table"),
                ])
            ], className="row"
        ),

        html.Div(
            [
                html.Div(id="click_table"),
            ],
            className="six columns",
        )
    ], className='ten columns offset-by-one'))


@app.callback(
    Output('map', 'figure'),
    [Input('rating_range', 'value')])
def update_map(value):
    return make_map(value[0], value[1])


@app.callback(
    Output('click_table', 'children'),
    [Input('map', 'clickData')])
def display_click(data):
    ctext(data, "blue")
    if data:
        hdf = db.execute_query('all_data', [{"$match": {'Hotel_Name': data['points'][0]['hovertext']}}])
        hdf = hdf.rename(columns={'Review': 'Review_long'})
        hdf['Review'] = hdf['Review_long'].astype(str).str[0:50]
        hdf = hdf.drop(columns=['Hotel_Address', 'Hotel_Name', 'Lat', 'Lng', 'Average_Score', 'Total_Number_of_Reviews', 'Additional_Number_of_Scoring', 'Review_long'])
        ctext(hdf, "red")
        # reorder
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