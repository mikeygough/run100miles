# imports
from datetime import datetime, timedelta, date
from dash import Dash, html, dcc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

# use stylesheet
external_stylesheets = [dbc.themes.LITERA]
# create app
app = Dash(__name__, external_stylesheets=external_stylesheets)
# ! LOAD (numeric) DATA ! #
df = pd.read_csv('data/numeric_data.csv', 
                 parse_dates=['Date'], infer_datetime_format=True, 
                 index_col='Date', thousands=',')

# create minutes column
df['Time_m'] = df['Time_s'] / 60.
# create 7 and 30 day rolling sums
df['7d'] = df['Distance'].rolling(7).sum()
df['30d'] = df['Distance'].rolling(30).sum()


# ! GENERATE PLOTS AND FIGS ! #
# fig1 (distance)
fig1 = px.area(data_frame=df, y='Distance', height=400)
fig1.update_traces(line_color='#1c9099')
fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)',
                   font_family='Times New Roman',
                   margin=dict(l=10, r=10, t=10, b=10))
fig1.update_yaxes(title_text='')
fig1.update_xaxes(title_text='')


# fig2 (cumulative distance)
fig2 = px.bar(data_frame=df['Distance'].cumsum(), y='Distance',
              height=400,
              color_discrete_sequence=['#016c59']*len(df))
fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)',
                   font_family='Times New Roman',
                   margin=dict(l=10, r=10, t=10, b=10))
fig2.update_yaxes(title_text='')
fig2.update_xaxes(title_text='')


# fig3 (rolling weekly and monthly mileage)
# uses graph_object 'go'
fig3 = make_subplots(specs=[
                            [{'secondary_y': True}]
                           ]
                    )
# add traces
# 7d
fig3.add_trace(
    go.Line(x=df.index, 
            y=df['7d'],
            line_color='#67a9cf',
            name='Weekly Mileage'),
    secondary_y=False)
#30d
fig3.add_trace(
    go.Line(x=df.index,
            y=df['30d'],
            line_color='#014636',
            name='Monthly Mileage'),
    secondary_y=True)
fig3.update_layout(height=400,
                   paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)',
                   font_family='Times New Roman',
                   margin=dict(l=10, r=10, t=10, b=10),
                   legend=dict(orientation="h",
                               yanchor="top", y=1.1,
                               xanchor="left",x=0.01))
fig3.update_yaxes(title_text='')
fig3.update_xaxes(title_text='')

# fig4 (distance distribution)
fig4 = px.histogram(data_frame=df, y='Distance',
              height=400,
              color_discrete_sequence=['#016c59']*len(df))
fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)',
                   font_family='Times New Roman',
                   margin=dict(l=10, r=10, t=10, b=10))
fig4.update_yaxes(title_text='')
fig4.update_xaxes(title_text='')



# descriptive statistics
total_ran = int(df['Distance'].sum())
total_runs = int(df[df['Distance'] > 0].shape[0])
total_hours = df['Time_m'].sum() / 60.
total_calories = df['Calories'].sum()

start_date = df.index.min()
end_date = df.index.max()


# ! LAYOUT ! #
app.layout = dbc.Container(
    html.Div(children=[
    
        # top section
        html.H1(children='Run100Miles',
                style={
                    'textAlign': 'center'
                }),
        html.H5(children='Choose a daterange to update training stats:',
                style={
                    'textAlign': 'center'
                }),
        html.Br(),

        # summary stats & runs plot
        html.Div(dbc.Row(
                [
                dbc.Col([
                        dbc.CardBody(
                            [
                                html.H6('Mile Count...', 
                                        className='card-title'),
                                html.P('{}'.format(total_ran),
                                       className='card-text',
                                       id='total_distance')
                            ], className='card bg-light mb-3'),
                        dbc.CardBody(
                            [
                                html.H6('Run Count...',
                                        className='card-title'),
                                html.P('{}'.format(total_runs),
                                        className='card-text',
                                        id='total_runs')
                            ], className='card bg-light mb-3'),
                        dbc.CardBody(
                            [
                                html.H6('Hour Count...',
                                        className='card-title'),
                                html.P('{}'.format(total_hours),
                                        className='card-text',
                                        id='total_hours')
                            ], className='card bg-light mb-3'),
                        dbc.CardBody(
                            [
                                html.H6('Calorie Count...',
                                        className='card-title'),
                                html.P('{}'.format(total_calories),
                                        className='card-text',
                                        id='total_calories')
                            ], className='card bg-light mb-3'),
                        ], width=2),
                dbc.Col([
                        dbc.Card([
                            # html.H6('Runs by Distance',
                            #         className='graph-card-title'),
                            dbc.Row(
                                dbc.Col(
                                    dbc.CardBody(
                                        dmc.DateRangePicker(
                                            id='date_filter',
                                            value=[start_date, end_date],
                                            minDate=df.index.min(),
                                            maxDate=df.index.max(),
                                            icon=[DashIconify(icon='clarity:date-line')],
                                            size='lg'),
                                        className='card border-dark mb-3 my-date-range-picker-card'),
                                    width=4),
                                justify='left', align='left'),
                            dcc.Graph(id='graph1', figure=fig1)
                            ], className='graph-card')
                        ], width=10)
                ], align='center'),
        style={'border-radius': '20px', 'padding': '10px'}),

        # rolling sum and cumulative distance plots
        html.Div(dbc.Row(
            [
            dbc.Col([
                dbc.Card([
                    html.H6('Rolling Weekly and Monthly Sum',
                            className='graph-card-title'),
                    dcc.Graph(id='graph3', figure=fig3)
                    ], className='graph-card')
                ], width=6),
            dbc.Col([
                dbc.Card([
                    html.H6('Cumulative Distance',
                            className='graph-card-title'),
                    dcc.Graph(id='graph2', figure=fig2)
                    ], className='graph-card')
                ], width=6)
            ], align='center'),
        style={'border-radius': '0px', 'padding': '10px'}),
        html.Br(),

        # histogram of run distance
        html.Div(dbc.Row(
            [
            dbc.Col([
                dbc.Card([
                    html.H6('Distance Distribution',
                            className='graph-card-title'),
                    dcc.Graph(id='graph4', figure=fig4)
                    ], className='graph-card')
                ], width=5),
            ], align='center'),
        style={'border-radius': '0px', 'padding': '10px'})

    ]), fluid=True)


# ! CALLBACKS ! #
# total distance
@app.callback(
    Output('total_distance', 'children'),
    Input('date_filter', 'value'))
def updateTotalDistance(value):
    if not value:
        raise dash.exceptions.PreventUpdate
    else:
        total_ran = int(df[value[0]:value[1]]['Distance'].sum())
        return f'{total_ran:,.0f}'

# total runs
@app.callback(
    Output('total_runs', 'children'),
    Input('date_filter', 'value'))
def updateTotalRuns(value):
    if not value:
        raise dash.exceptions.PreventUpdate
    else:
        total_runs = int(df[value[0]:value[1]][df['Distance'] > 0].shape[0])
        return f'{total_runs:,.0f}'

# total hours
@app.callback(
    Output('total_hours', 'children'),
    Input('date_filter', 'value'))
def updateTotalHours(value):
    if not value:
        raise dash.exceptions.PreventUpdate
    else:
        total_hours = int(df[value[0]:value[1]]['Time_m'].sum() / 60.)
        return f'{total_hours:,.0f}'

# total calories
@app.callback(
    Output('total_calories', 'children'),
    Input('date_filter', 'value'))
def updateTotalCalories(value):
    if not value:
        raise dash.exceptions.PreventUpdate
    else:
        total_calories = int(df[value[0]:value[1]]['Calories'].sum())
        return f'{total_calories:,.0f}'

# distance plot
@app.callback(
    Output('graph1', 'figure'),
    Input('date_filter', 'value'))
def updateDistanceGraph(value):
    if not value:
        raise dash.exceptions.PreventUpdate
    else:
        # define date range
        idx = pd.date_range(value[0], value[1])
        # reindex
        df_alldays = df.reindex(idx, fill_value=0).copy(deep=True)
        fig1 = px.area(data_frame=df_alldays, y='Distance', height=400)
        fig1.update_traces(line_color='#1c9099')
        fig1.update_layout(paper_bgcolor = 'rgba(0,0,0,0)',
                           plot_bgcolor = 'rgba(0,0,0,0)',
                           font_family='Times New Roman',
                           margin=dict(l=10, r=10, t=10, b=10))
        fig1.update_yaxes(title_text='')
        fig1.update_xaxes(title_text='')
        return fig1

# cumulative distance plot
@app.callback(
    Output('graph2', 'figure'),
    Input('date_filter', 'value'))
def updateCumulativeDistanceGraph(value):
    if not value:
        raise dash.exceptions.PreventUpdate
    else:
        # define date range
        idx = pd.date_range(value[0], value[1])
        # reindex
        df_alldays = df.reindex(idx, fill_value=0).copy(deep=True)
        fig2 = px.bar(data_frame=df_alldays['Distance'].cumsum(), y='Distance',
                      height=400,
                      color_discrete_sequence=['#016c59']*len(df_alldays))
        fig2.update_layout(paper_bgcolor = 'rgba(0,0,0,0)',
                           plot_bgcolor = 'rgba(0,0,0,0)',
                           font_family='Times New Roman',
                           margin=dict(l=10, r=10, t=10, b=10))
        fig2.update_yaxes(title_text='')
        fig2.update_xaxes(title_text='')
        return fig2

# rolling sums
@app.callback(
    Output('graph3', 'figure'),
    Input('date_filter', 'value'))
def updateRollingWeeklyMileageGraph(value):
    if not value:
        raise dash.exceptions.PreventUpdate
    else:
        # define date range
        idx = pd.date_range(value[0], value[1])
        # reindex
        df_alldays = df.reindex(idx, fill_value=0).copy(deep=True)

        df_alldays['7d'] = df_alldays['Distance'].rolling(7).sum()
        df_alldays['30d'] = df_alldays['Distance'].rolling(30).sum()

        fig3 = make_subplots(specs=[[{'secondary_y': True}]])

        # Add traces
        fig3.add_trace(
            go.Line(x=df_alldays.index,
                    y=df_alldays['7d'],
                    line_color='#67a9cf',
                    name='Weekly Mileage'),
            secondary_y=False)

        fig3.add_trace(
            go.Line(x=df_alldays.index, 
                    y=df_alldays['30d'],
                    line_color='#014636',
                    name='Monthly Mileage'),
            secondary_y=True)

        fig3.update_layout(height=400,
                           paper_bgcolor = 'rgba(0,0,0,0)',
                           plot_bgcolor = 'rgba(0,0,0,0)',
                           font_family='Times New Roman',
                           margin=dict(l=10, r=10, t=10, b=10),
                           legend=dict(orientation="h",
                                       yanchor="top", y=1.1,
                                       xanchor="left",x=0.01))
        fig3.update_yaxes(title_text='')
        fig3.update_xaxes(title_text='')
        return fig3


# ! MAIN ! #
if __name__ == '__main__':
    app.run_server(debug=True)
