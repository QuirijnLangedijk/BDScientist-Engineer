import pandas as pd
import plotly.express as px
from src.Part2.db.db_utils import get_all_data

df = get_all_data()
pd.set_option('display.max_columns', None)
print(df.head())
# hotels = pd.DataFrame(columns=['Hotel_Address', 'Hotel_Name', 'Lat', 'Lng', 'Average_Score', 'Total_Number_of_Reviews', 'Additional_Number_of_Scoring'])

'''
for i in range(df.shape[0]):
    print(str(i),  ' - ', df.iloc[i].Hotel_Address in hotels.Hotel_Address.values)
    if df.iloc[i].Hotel_Address not in hotels.Hotel_Address.values:
        row = df.iloc[i]
        hotels.loc[i] = [row.Hotel_Address, row.Hotel_Name, row.Lat, row.Lng, row.Average_Score, row.Total_Number_of_Reviews, row.Additional_Number_of_Scoring]
'''

hotels = df.drop_duplicates('Hotel_Address')
hotels.reset_index(drop=True, inplace=True)

print(hotels)
fig = px.scatter_mapbox(hotels, lat="Lat", lon="Lng", hover_name="Hotel_Name", hover_data=["Average_Score", "Total_Number_of_Reviews"],
                        zoom=3, height=1000, size="Total_Number_of_Reviews", color="Average_Score", opacity=1, color_continuous_scale="rdylgn")
fig.update_layout(mapbox_style="dark", mapbox_accesstoken="pk.eyJ1IjoicWxhbmdlZGlqayIsImEiOiJjanRzbnduNTgwcW52M3lsODlvcW5qODduIn0.YWIrTNQehZylJfjo8KfwGA")
fig.update_layout(
    autosize=True,
    margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()
