from flask import Flask
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import joblib
import sys
import json

from layout.main_layout import get_layout

# -----------------------------------------------------------------------------
'''
    Block for test and fake data
'''
import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(stream=sys.stderr))
logger.setLevel(logging.DEBUG)

INIT_DATA =  { 'house_id' : 0, 
            'prediction' : 0,
            'variables' : {
                'names' : ['var1', 'var2', 'var3', 'var4', 'var5'],
                'values': [0, 0 , 0 , 0 , 0],
                'percentage': [20, 20, 20, 20, 20]
                }
    }

FAKE_DATA = { 'house_id' : 0, 
            'prediction' : 30,
            'variables' : {
                'names' : ['var1', 'var2', 'var3', 'var4', 'var5'],
                'values': [10, 20 , 30 , -10 , -20],
                'percentage': [15, 30, 40, 10, 5]
                }
    }

FAKE_DATA2 = { 'house_id' : 0, 
            'prediction' : 35,
            'variables' : {
                'names' : ['var1', 'var2', 'var3', 'var4', 'var5'],
                'values': [-10, -20 , 30 , 50 , 20],
                'percentage': [5, 10, 30, 25, 25]
                }
    }

def get_fake_data(house_id):
    data = FAKE_DATA
    if house_id == 99:
        data = FAKE_DATA2
    data['house_id'] = house_id
    return data

# -----------------------------------------------------------------------------
'''
    Server initialization

    and layout load
'''
server = Flask(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(name='Dash_docker_app',
                server=server,
                external_stylesheets=external_stylesheets)

app.layout = get_layout()

model = None

# -----------------------------------------------------------------------------
'''
    Prediction
    and data result json preparation
'''
def predict(house_id):
    try:
        if model is not None:
            result = model.predict(house_id)
            # TODO threat result
            return INIT_DATA
        else:    
            data = get_fake_data(house_id)
            return data
    except:
        app.server.logger.info('test {} {}'.format(house_id, model))
        return INIT_DATA      

# -----------------------------------------------------------------------------
'''
    Dash Callbacks

    https://dash.plotly.com/basic-callbacks (Chained Callbacks)
'''
@app.callback(
    Output(component_id='intermediate-value', component_property='children'), 
    [Input(component_id='input_house_id', component_property='value')])
def data_entered(value):
    app.server.logger.info('callback called')
    data = predict(value)
    return json.dumps(data)

@app.callback(Output('ind_house_id', 'children'), 
            [Input('intermediate-value', 'children')])
def update_indicator_house(jsonified_cleaned_data):
    data = json.loads(jsonified_cleaned_data)
    house_id = data['house_id'] if data['house_id'] else 0
    return house_id

@app.callback(Output('ind_days_to_rent', 'children'), 
            [Input('intermediate-value', 'children')])
def update_indicator_days_to_rent(jsonified_cleaned_data):
    data = json.loads(jsonified_cleaned_data)
    days = data['prediction'] if data['prediction'] else 0
    return days

@app.callback(Output('features_percentage', 'figure'), 
            [Input('intermediate-value', 'children')])
def update_graph_pie(jsonified_cleaned_data):
    data = json.loads(jsonified_cleaned_data)

    labels = data['variables']['names']
    values = data['variables']['percentage']

    trace = go.Pie(
        labels=labels,
        values=values,
    )
    layout = dict(margin=dict(l=15, r=10, t=0, b=65), 
                legend=dict(orientation="h"))

    return dict(data=[trace], layout=layout)

@app.callback(Output('features_importance', 'figure'), 
            [Input('intermediate-value', 'children')])
def update_graph_bar(jsonified_cleaned_data):
    data = json.loads(jsonified_cleaned_data)

    labels = data['variables']['names']
    values = data['variables']['values']

    trace = go.Bar(
        y=labels,
        x=values,
        orientation='h',
    )
    layout = dict(margin=dict(l=40, r=10, t=0, b=30), 
                    legend=dict(orientation="h"),
                    yaxis=dict(automargin=True)
    )

    return dict(data=[trace], layout=layout)

'''
    Main block
'''
if __name__ == '__main__':
    try:
        model = joblib.load("./data/model.pkl")
    except Exception as ex:
        app.server.logger.error('loading model')

    app.run_server(host='0.0.0.0', debug=True)