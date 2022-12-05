# test dash dashboard
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)


# ! LOAD (numeric) DATA ! #
df = pd.read_csv('data/numeric_data.csv', parse_dates=['Date'],
                         infer_datetime_format=True, index_col='Date',
                         thousands=',')


# ! GENERATE DATA ! #
# create the fig1 (distance)
fig1 = px.line(data_frame=df, y='Distance')

# create the fig2 (cumulative distance)
fig2 = px.bar(data_frame=df['Distance'].cumsum(), y='Distance',
               color_discrete_sequence=['#656EF2']*len(df))

# create the fig3 (rolling weekly mileage)
fig3 = px.line(data_frame=df['Distance'].rolling(7).sum(), y='Distance')

total_ran = int(df['Distance'].sum())
total_runs = int(df[df['Distance'] > 0].shape[0])


# ! LAYOUT ! #
app.layout = html.Div(children=[
    
    html.H1(children='Run100Miles'),

    html.H3(children='Pick a date range & see your running stats update automagically!'),

    dcc.DatePickerRange(id='date_filter',
                        start_date=df.index.min(),
                        end_date=df.index.max(),
                        min_date_allowed=df.index.min(),
                        max_date_allowed=df.index.max()),
    
    html.H3(id='total_distance', 
             children='{} Miles Ran'.format(total_ran)),

    html.H3(id='total_runs', 
             children='{} Runs'.format(total_runs)),

    html.Div(id='output-container-date-picker-range'),
    
    html.H3(children='Runs by Distance...'),

    dcc.Graph(id='graph1',
              figure=fig1),

    html.H3(children='Cumulative Distance...'),

    dcc.Graph(id='graph2',
              figure=fig2),

    html.H3(children='Rolling Weekly Mileage...'),

    dcc.Graph(id='graph3',
              figure=fig3),
    ])


# ! CALLBACKS ! #
# Total Distance
@app.callback(
    Output('total_distance', 'children'),
    Input('date_filter', 'start_date'),
    Input('date_filter', 'end_date'))
def updateTotalDistance(start_date, end_date):
    if not start_date or not end_date:
        raise dash.exceptions.PreventUpdate
    else:
        return '{} Miles Ran'.format(int(df[start_date:end_date]['Distance'].sum()))

# Total Runs
@app.callback(
    Output('total_runs', 'children'),
    Input('date_filter', 'start_date'),
    Input('date_filter', 'end_date'))
def updateTotalRuns(start_date, end_date):
    if not start_date or not end_date:
        raise dash.exceptions.PreventUpdate
    else:
        return '{} Runs'.format(int(df[start_date:end_date][df['Distance'] > 0].shape[0]))

# Distance Plot
@app.callback(
    Output('graph1', 'figure'),
    Input('date_filter', 'start_date'),
    Input('date_filter', 'end_date'))
def updateDistanceGraph(start_date, end_date):
    if not start_date or not end_date:
        raise dash.exceptions.PreventUpdate
    else:
        # define date range
        idx = pd.date_range(start_date, end_date)
        # reindex
        df_alldays = df.reindex(idx, fill_value=0).copy(deep=True)
        return px.line(data_frame=df_alldays, y='Distance')

# Cumulative Distance Plot
@app.callback(
    Output('graph2', 'figure'),
    Input('date_filter', 'start_date'),
    Input('date_filter', 'end_date'))
def updateCumulativeDistanceGraph(start_date, end_date):
    if not start_date or not end_date:
        raise dash.exceptions.PreventUpdate
    else:
        # define date range
        idx = pd.date_range(start_date, end_date)
        # reindex
        df_alldays = df.reindex(idx, fill_value=0).copy(deep=True)
        return px.bar(data_frame=df_alldays['Distance'].cumsum(), y='Distance',
            color_discrete_sequence=['#656EF2']*len(df_alldays))

# Rolling Weekly Mileage
@app.callback(
    Output('graph3', 'figure'),
    Input('date_filter', 'start_date'),
    Input('date_filter', 'end_date'))
def updateRollingMileageGraph(start_date, end_date):
    if not start_date or not end_date:
        raise dash.exceptions.PreventUpdate
    else:
        # define date range
        idx = pd.date_range(start_date, end_date)
        # reindex
        df_alldays = df.reindex(idx, fill_value=0).copy(deep=True)
        return px.line(data_frame=df_alldays['Distance'].rolling(7).sum(), y='Distance')


# ! MAIN ! #
if __name__ == '__main__':
    app.run_server(debug=True)
