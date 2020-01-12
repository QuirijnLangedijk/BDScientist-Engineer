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

        return table


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