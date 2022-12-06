# test dash dashboard
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])


# ! LOAD (numeric) DATA ! #
df = pd.read_csv('data/numeric_data.csv', parse_dates=['Date'],
                         infer_datetime_format=True, index_col='Date',
                         thousands=',')

print(df.head())

# create minutes column
df['Time_m'] = df['Time_s'] / 60.

# ! GENERATE DATA ! #
# create the fig1 (distance)
fig1 = px.line(data_frame=df, y='Distance',
               title='Runs by Distance...')
fig1.update_yaxes(title_text='')
fig1.update_xaxes(title_text='')

# create the fig2 (cumulative distance)
fig2 = px.bar(data_frame=df['Distance'].cumsum(), y='Distance',
              color_discrete_sequence=['#656EF2']*len(df),
              title='Cumulative Miles Ran...')
fig2.update_yaxes(title_text='')
fig2.update_xaxes(title_text='')

# create the fig3 (rolling weekly mileage)
fig3 = px.line(data_frame=df['Distance'].rolling(7).sum(), y='Distance',
               title='Rolling Weekly Mileage...')
fig3.update_yaxes(title_text='')
fig3.update_xaxes(title_text='')

# create the fig4 (rolling 30 day mileage)
fig4 = px.line(data_frame=df['Distance'].rolling(30).sum(), y='Distance',
               title='Rolling Monthly Mileage...')
fig4.update_yaxes(title_text='')
fig4.update_xaxes(title_text='')

total_ran = int(df['Distance'].sum())
total_runs = int(df[df['Distance'] > 0].shape[0])
total_hours = df['Time_m'].sum() / 60.


# ! LAYOUT ! #
app.layout = html.Div(children=[
    
    html.H1(children='Run100Miles',
            style={
                'textAlign': 'center'
            }),

    html.H3(children='Choose a daterange to update training stats:',
            style={
                'textAlign': 'center'
            }),

    html.Div(children=[
    dcc.DatePickerRange(id='date_filter',
                        start_date=df.index.min(),
                        end_date=df.index.max(),
                        min_date_allowed=df.index.min(),
                        max_date_allowed=df.index.max(),
                        style={
                        'width': '100%',
                        'display': 'flex',
                        'align-items': 'center',
                        'justify-content': 'center'
                        })]),
    
    # SUMMARY STATS
    html.H3(id='total_distance', 
             children='Miles Ran: {}'.format(total_ran)),
    html.H3(id='total_runs', 
             children='Number of Runs: {}'.format(total_runs)),
    html.H3(id='total_hours', 
             children=f'Hours Spent Running: {total_hours:,.0f}'),

    # DATE PICKER
    html.Div(id='output-container-date-picker-range'),
    
    # GRAPHS
    dcc.Graph(id='graph1',
              figure=fig1),

    dcc.Graph(id='graph2',
              figure=fig2),

    dcc.Graph(id='graph3',
              figure=fig3),

    dcc.Graph(id='graph4',
              figure=fig4),
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
        return 'Miles Ran: {}'.format(int(df[start_date:end_date]['Distance'].sum()))

# Total Runs
@app.callback(
    Output('total_runs', 'children'),
    Input('date_filter', 'start_date'),
    Input('date_filter', 'end_date'))
def updateTotalRuns(start_date, end_date):
    if not start_date or not end_date:
        raise dash.exceptions.PreventUpdate
    else:
        return 'Number of Runs: {}'.format(int(df[start_date:end_date][df['Distance'] > 0].shape[0]))

# Total Hours
@app.callback(
    Output('total_hours', 'children'),
    Input('date_filter', 'start_date'),
    Input('date_filter', 'end_date'))
def updateTotalHours(start_date, end_date):
    if not start_date or not end_date:
        raise dash.exceptions.PreventUpdate
    else:
        total_hours = int(df[start_date:end_date]['Time_m'].sum() / 60.)
        return f'Hours Spent Running: {total_hours:,.0f}'

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
        fig1 = px.line(data_frame=df_alldays, y='Distance',
                       title='Runs by Distance...')
        fig1.update_yaxes(title_text='')
        fig1.update_xaxes(title_text='')
        return fig1

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
        fig2 = px.bar(data_frame=df_alldays['Distance'].cumsum(), y='Distance',
                      color_discrete_sequence=['#656EF2']*len(df_alldays),
                      title='Cumulative Miles Ran...')
        fig2.update_yaxes(title_text='')
        fig2.update_xaxes(title_text='')
        return fig2

# Rolling Weekly Mileage
@app.callback(
    Output('graph3', 'figure'),
    Input('date_filter', 'start_date'),
    Input('date_filter', 'end_date'))
def updateRollingWeeklyMileageGraph(start_date, end_date):
    if not start_date or not end_date:
        raise dash.exceptions.PreventUpdate
    else:
        # define date range
        idx = pd.date_range(start_date, end_date)
        # reindex
        df_alldays = df.reindex(idx, fill_value=0).copy(deep=True)
        fig3 = px.line(data_frame=df_alldays['Distance'].rolling(7).sum(), 
                       y='Distance', title='Rolling Weekly Mileage...')
        fig3.update_yaxes(title_text='')
        fig3.update_xaxes(title_text='')
        return fig3

# Rolling Monthly Mileage
@app.callback(
    Output('graph4', 'figure'),
    Input('date_filter', 'start_date'),
    Input('date_filter', 'end_date'))
def updateRollingMonthlyMileageGraph(start_date, end_date):
    if not start_date or not end_date:
        raise dash.exceptions.PreventUpdate
    else:
        # define date range
        idx = pd.date_range(start_date, end_date)
        # reindex
        df_alldays = df.reindex(idx, fill_value=0).copy(deep=True)
        fig4 = px.line(data_frame=df_alldays['Distance'].rolling(40).sum(),
                       y='Distance', title='Rolling Monthly Mileage...')
        fig4.update_yaxes(title_text='')
        fig4.update_xaxes(title_text='')
        return fig4


# ! MAIN ! #
if __name__ == '__main__':
    app.run_server(debug=True)
