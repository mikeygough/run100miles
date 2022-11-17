# test dash dashboard
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)


# load in (numeric) data
df = pd.read_csv('data/numeric_data.csv', parse_dates=['Date'],
                         infer_datetime_format=True, index_col='Date',
                         thousands=',')

# create the fig
fig = px.line(data_frame=df, y='Distance')


# create layout
app.layout = html.Div(children=[
    html.H1(children='hello, world'),
    html.Div(children='i like to run'),
    dcc.Graph(id='example-graph',
        figure=fig)
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
