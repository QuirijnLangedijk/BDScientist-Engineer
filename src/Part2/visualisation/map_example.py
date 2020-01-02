import chart_studio
import plotly.graph_objs as go
import pandas as pd
from src.Part2.db.db_utils import get_all_data
import chart_studio.plotly as py
import plotly.io as pio


chart_studio.tools.set_credentials_file(username='QLangedijk', api_key='teCWrnePUrMOyVY141xW')

df = get_all_data()
df = df.drop_duplicates('Hotel_Address')
df.reset_index(drop=True, inplace=True)

cities = list(['London', 'Amsterdam', 'Paris', 'Barcelona', 'Milan', 'Vienna'])
print(cities)

data = []
for city in cities:
    print(df.loc[df['Hotel_Address'].str.contains(city), 'Hotel_Name'])
    print(df.loc[df['Hotel_Address'].str.contains(city), 'Lat'])
    df[['Hotel_Name']] = df[['Hotel_Name']].astype(str)
    event_data = dict(
        lat=df.loc[df['Hotel_Address'].str.contains(city), 'Lat'],
        lon=df.loc[df['Hotel_Address'].str.contains(city), 'Lng'],
        name=city,
        marker=dict(size=8, opacity=0.5),
        type='scattermapbox'
    )
    data.append(event_data)

mapbox_access_token = 'pk.eyJ1IjoicWxhbmdlZGlqayIsImEiOiJjanRzbnduNTgwcW52M3lsODlvcW5qODduIn0.YWIrTNQehZylJfjo8KfwGA'

layout = dict(
    height=1000,
    margin=dict(t=0, b=0, l=0, r=0),
    font=dict(color='#FFFFFF', size=11),
    paper_bgcolor='#000000',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=48,
            lon=2
        ),
        pitch=0,
        zoom=3,
        style='dark'
    ),
)

updatemenus = list([
    dict(
        buttons=list([
            dict(
                args=['mapbox.style', 'dark'],
                label='Dark',
                method='relayout'
            ),
            dict(
                args=['mapbox.style', 'light'],
                label='Light',
                method='relayout'
            ),
            dict(
                args=['mapbox.style', 'outdoors'],
                label='Outdoors',
                method='relayout'
            ),
            dict(
                args=['mapbox.style', 'satellite-streets'],
                label='Satellite with Streets',
                method='relayout'
            )
        ]),
        direction='up',
        x=0.75,
        xanchor='left',
        y=0.05,
        yanchor='bottom',
        bgcolor='#000000',
        bordercolor='#000000',
        font=dict(size=11)
    ),

    dict(
        buttons=list([
            dict(label='All Cities',
                 method='update',
                 args=[{'visible': [True, True, True, True, True, True]}]),
            dict(label='London',
                 method='update',
                 args=[{'visible': [True, False, False, False, False, False]}]),
            dict(label='Amsterdam',
                 method='update',
                 args=[{'visible': [False, True, False, False, False, False]}]),
            dict(label='Paris',
                 method='update',
                 args=[{'visible': [False, False, True, False, False, False]}]),
            dict(label='Barcelona',
                 method='update',
                 args=[{'visible': [False, False, False, True, False, False]}]),
            dict(label='Milan',
                 method='update',
                 args=[{'visible': [False, False, False, False, True, False]}]),
            dict(label='Vienna',
                 method='update',
                 args=[{'visible': [False, False, False, False, False, True]}])

        ]),
        direction='down',
        x=0.5,
        xanchor='left',
        y=0.99,
        yanchor='bottom',
        bgcolor='#000000',
        bordercolor='#FFFFFF',
        font=dict(size=11)
    )
])


layout['title'] = 'Hotels'
layout['updatemenus'] = updatemenus

figure = dict(data=data, layout=layout)
py.iplot(figure, filename='hotels')

pio.write_html(figure, file='hotels.html', auto_open=True)
