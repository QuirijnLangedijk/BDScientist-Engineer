import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
from classify.classify import classify_lr
import utils.utils as utils
import pandas as pd
import dash_table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('classify', external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    dcc.Input(id='input'),

    html.Button('Classify', id='button'),

    html.Div(className='row', children=[
        html.Div(id="click_table"),
    ])
])

@app.callback(
    Output('click_table', 'children'),
    [Input('button', 'n_clicks')],
    [State('input', 'value')])
def display_click(n_clicks, value):
    if value:
        data = [['Logistic Regression Spark', classify_spark_lr(value)], ['Logistic Regression', classify_normal_lr(value)], ['Naive Bayes', classify_nb(value)],
                ['Support Vector Machine', classify_svm(value)]]
        columns = ['Model', 'Resultaat']
        df = pd.DataFrame(data=data, columns=columns)
        columns = [{"name": i, "id": i} for i in df.columns]
        print('displayclick')
        print(df.head())

        table = dash_table.DataTable(
            columns=columns,
            data=list(df.to_dict("index").values()),
            style_cell={'textAlign': 'left'},
            style_as_list_view=True
        )

        print(table)

        return table



'''
app.layout = html.Div([

    html.Label('Input sentence'),
    dcc.Input(id='input-1'),

    html.Button('Classify', id='button-2'),

    html.Div(className='row', children=[
        html.Div(id="output"),
    ]),


    html.Div(dcc.Input(id='input-box', type='text')),
    html.Button('Submit', id='button'),
    html.Div(id='output-container-button',
             children='Enter a value and press submit'),
    html.Div(id="click_table"),
])


@app.callback(
    Output('output-container-button', 'children'),
    [Input('button', 'n_clicks')],
    [State('input-box', 'value')])
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )


@app.callback(
    Output(component_id='click_table', component_property='children'),
    [Input(component_id='input-box', component_property='value')],
    [State('input-box', 'value')])
def classify_all(sentence, value):
    data = [['Logistic Regression', classify_normal_lr(sentence)], ['Naive Bayes', classify_nb(sentence)], ['Support Vector Machine', classify_svm(sentence)]]
    columns = ['Model', 'Resultaat']
    df = pd.DataFrame(data=data, columns=columns)

    print(df.head())

    return dash_table.DataTable(
        columns=columns,
        data=df.to_dict('records'),
        style_cell={'textAlign': 'left'},
        style_as_list_view=True
    )

@app.callback(
    Output('output', 'children'),
    [Input('button-2', 'n_clicks')],
    state=[State('input-1', 'value')])
def compute(input1, sentence):
    data = [['Logistic Regression', classify_normal_lr(sentence)], ['Naive Bayes', classify_nb(sentence)], ['Support Vector Machine', classify_svm(sentence)]]
    columns = ['Model', 'Resultaat']
    df = pd.DataFrame(data=data, columns=columns)

    print(df.head())

    table = dash_table.DataTable(
        columns=columns,
        data=df.to_dict('records'),
        style_cell={'textAlign': 'left'},
        style_as_list_view=True
    )

    print('Sentence: ', sentence, 'Logistic Regression: ', classify_normal_lr(sentence), ' Naive Bayes: ', classify_nb(sentence), ' Support Vector Machine: ', classify_svm(sentence))
    return 'Sentence: ', sentence, 'Logistic Regression: ', classify_normal_lr(sentence), ' Naive Bayes: ', classify_nb(sentence), ' Support Vector Machine: ', classify_svm(sentence)
'''

def classify_spark_lr(sentence):
    return classify_lr(sentence)


def classify_normal_lr(sentence):
    vectorizer = utils.load_model('../../Part1/models/trained_models/logistic_regression/vectorizer100k')
    classifier = utils.load_model('../../Part1/models/trained_models/logistic_regression/classifier100k')

    review_vector = vectorizer.transform([sentence])
    return classifier.predict(review_vector)[0]


def classify_nb(sentence):
    utils.get_punkt()
    classifier = utils.load_model('../../Part1/models/trained_models/naive_bayes/NaiveBayes')

    return classifier.classify(utils.format_sentence(sentence))


def classify_svm(sentence):
    vectorizer = utils.load_model('../../Part1/models/trained_models/svm/vectorizer300k')
    classifier = utils.load_model('../../Part1/models/trained_models/svm/classifier300k')

    review_vector = vectorizer.transform([sentence])
    return classifier.predict(review_vector)[0]




if __name__ == '__main__':
    app.run_server(debug=True)