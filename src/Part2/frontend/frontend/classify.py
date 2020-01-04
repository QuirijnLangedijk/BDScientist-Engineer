import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from classify.classify import classify_lr

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('classify', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div')
])


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(sentence):
    return 'You\'ve entered "{}"'.format(classify_spark_lr(sentence))


def classify_spark_lr(sentence):
    print(classify_lr(sentence))
    return classify_lr(sentence)

if __name__ == '__main__':
    app.run_server(debug=True)