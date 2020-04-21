import dash_core_components as dcc
import dash_html_components as html

def get_layout():
    layout = html.Div(children=[
        # header
        html.Div([

            html.Span("Days to Rent Predictor", className='app-title'),
            
            html.Div(
                html.Img(src='./assets/quinto_andar_logo.png',height="100%")
                ,style={"float":"right","height":"100%"})
            ],
            className="row header"
            ),

    # input row div
        html.Div(
            [
                html.Div(
                    [ 
                        dcc.Input(
                            id="input_house_id",
                            type="number",
                            placeholder="Enter House ID ...",
                            n_submit=1,
                            debounce=True,
                            autoFocus=True
                        ),
                        html.Div(id='result')
                    ], 
                    style = {'textAlign': 'center', 'verticalAlign':'middle'},
                    className = "eight columns indicator",
                    
                ),
            ],
            className="row",
        ),

        # indicators row div
        html.Div(
            [
                html.Div(
                    [ 
                        html.P(
                            "House ID",
                            className="twelve columns indicator_text"
                        ),
                        html.P(
                            id = 'ind_house_id',
                            className="indicator_value"
                        ),
                    ],
                    className="four columns indicator",
                    
                ),
                html.Div(
                    [  
                        html.P(
                            "Days to Rent",
                            className="twelve columns indicator_text"
                        ),
                        html.P(
                            id = 'ind_days_to_rent',
                            className="indicator_value"
                        ),
                    ],
                    className="four columns indicator",
                    
                )
            ],
            className="row",
        ),

        # charts row div
        html.Div(
            [
                html.Div(
                    [
                        html.P("Features Percentage"),
                        dcc.Graph(
                            id="features_percentage",
                            style={"height": "90%", "width": "98%"},
                            config=dict(displayModeBar=False),
                        ),
                    ],
                    className="four columns chart_div"
                ),

                html.Div(
                    [
                        html.P("Features importance"),
                        dcc.Graph(
                            id="features_importance",
                            style={"height": "90%", "width": "98%"},
                            config=dict(displayModeBar=False),
                        ),
                    ],
                    className="four columns chart_div"
                ),
            ],
            className="row",
            style={"marginTop": "5"},
        ),

        # callback for all output data
        html.Div(id='intermediate-value', style={'display': 'none'}),

        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Roboto", rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet")
    ],
        className="row",
        style={"margin": "0%"},
    )
    return layout