import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import plotly
import numpy as np
import datetime as dt
import dash_table
import os
import sys
from plotly.subplots import make_subplots
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import math
import base64

ROOT_DIR = os.path.abspath(os.curdir)
format1 = '%Y-%m-%d %H:%M:%S'
format2 = '%H:%M:%S'
todayDate = dt.datetime.now().strftime('%Y-%m-%d')
#define what columns have to be shown
dashboard_col = ['code', 'Name', 'Industry', 'time', 'Price',  'Freq', 'Number', 'Star', 'Amp', 'Spread']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colors = {
    'background': '#111111',
    'background2': "rgba(0,0,0,255)",
    'text': "darkgray",
    'text2': "white"
}


def b64_image(image_filename):
    with open(image_filename, 'rb') as f: image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


app = dash.Dash(__name__, external_stylesheets=external_stylesheets, prevent_initial_callbacks=False)
app.layout = html.Div(style={'backgroundColor': '#21252C'}, children=[
    html.H5(children="HK Stock Scanner",
            style={
                'color': colors['text2']
            }),
    dcc.Interval(id="refresh-time", interval=1 * 5000, n_intervals=0),
    html.H6(id='update-time',
            style={
                'color': colors['text']
            }),
    html.Div([
        html.Div([
            dcc.Graph(
                id='chart1',
                figure={'layout': {
                    'plot_bgcolor': colors['background2'],
                    'paper_bgcolor': colors['background2'],
                }}
            ),
        ], className='three columns'),
        html.Div([
            dcc.Graph(
                id='chart2',
                figure={'layout': {
                    'plot_bgcolor': colors['background2'],
                    'paper_bgcolor': colors['background2'],
                }}
            ),
        ], className='three columns'),
        html.Div([
            dcc.Graph(
                id='chart3',
                figure={'layout': {
                    'plot_bgcolor': colors['background2'],
                    'paper_bgcolor': colors['background2'],
                }}
            ),
        ], className='three columns'),
        html.Div([
            dcc.Graph(
                id='chart4',
                figure={'layout': {
                    'plot_bgcolor': colors['background2'],
                    'paper_bgcolor': colors['background2'],
                }}
            ),
        ], className='three columns')
    ], className='row'),
    html.Div([
        html.Div([
            dcc.Graph(
                id='chart5',
                figure={'layout': {
                    'plot_bgcolor': colors['background2'],
                    'paper_bgcolor': colors['background2'],
                }}
            ),
        ], className='three columns'),
        html.Div([
            dcc.Graph(
                id='chart6',
                figure={'layout': {
                    'plot_bgcolor': colors['background2'],
                    'paper_bgcolor': colors['background2'],
                }}
            ),
        ], className='three columns'),
        html.Div([
            dcc.Graph(
                id='chart7',
                figure={'layout': {
                    'plot_bgcolor': colors['background2'],
                    'paper_bgcolor': colors['background2'],
                }}
            ),
        ], className='three columns'),
        html.Div([
            dcc.Graph(
                id='chart8',
                figure={'layout': {
                    'plot_bgcolor': colors['background2'],
                    'paper_bgcolor': colors['background2'],
                }}
            ),
        ], className='three columns')
    ], className='row'),
    html.Div([
        html.Div([
            dcc.Graph(
                id='chart9',
                figure={'layout': {
                    'plot_bgcolor': colors['background2'],
                    'paper_bgcolor': colors['background2'],
                }}
            ),
        ], className='three columns'),
        html.Div([
            dcc.Graph(
                id='chart10',
                figure={'layout': {
                    'plot_bgcolor': colors['background2'],
                    'paper_bgcolor': colors['background2'],
                }}
            ),
        ], className='three columns'),
        html.Div([
            dcc.Graph(
                id='chart11',
                figure={'layout': {
                    'plot_bgcolor': colors['background2'],
                    'paper_bgcolor': colors['background2'],
                }}
            ),
        ], className='three columns'),
        html.Div([
            dcc.Graph(
                id='chart12',
                figure={'layout': {
                    'plot_bgcolor': colors['background2'],
                    'paper_bgcolor': colors['background2'],
                }}
            ),
        ], className='three columns')
    ], className='row')
])


def generatingCharts(market_data, code, dashboard):
    dfstock = market_data[market_data.code == code]
    amp = dashboard.loc[code, 'Amp']
    name = dashboard.loc[code, 'Name']
    chart_title = code + ' ' + name + ' ' + amp
    title_color = 'white'
    if dashboard.loc[code, 'Amp'] >= '1%':
        title_color = '#3D9970'
    elif dashboard.loc[code, 'Amp'] <= '-1%':
        title_color = '#FF4136'
    elif '-1%' < dashboard.loc[code, 'Amp'] < '1%':
        title_color = 'white'
    fig = candlestick_chart(dfstock, chart_title, title_color)
    return fig


def candlestick_chart(dfstock, chart_title, title_color):
    ohlc_stock = dfstock['price'].resample('1Min').ohlc()
    ohlc_stock.reset_index(inplace=True)
    ohlc_stock['time'] = pd.to_datetime(ohlc_stock['DateTime']).dt.strftime('%H:%M:%S')
    ohlc_stock.dropna(inplace=True)
    ohlc_stock.drop('DateTime', axis=1, inplace=True)
    ohlc_stock.set_index('time', inplace=True)
    timelength = len(ohlc_stock.index)
    if timelength >= 40:
        ohlc_stock = ohlc_stock.iloc[timelength - 40:timelength]
    fig = go.Figure(go.Candlestick(
        x=ohlc_stock.index,
        open=ohlc_stock['open'],
        high=ohlc_stock['high'],
        low=ohlc_stock['low'],
        close=ohlc_stock['close']
    ))
    fig.update_layout(
        title=chart_title,
        title_font_color=title_color,
        title_font_size=25,
        autosize=True,
        width=550,
        height=400,
        plot_bgcolor='#21252C',
        paper_bgcolor="#21252C",
        font_color='white',
        showlegend=False,
        xaxis_rangeslider_visible=False,
        hovermode='x unified',
        xaxis={
            "zeroline": True,
            "showgrid": False,
            "showline": False,
            "autorange": True,
            "visible": False,
            "type": "category",
            # "titlefont": {"color": "darkgray"},
        },
        yaxis={
            "showgrid": False,
            "showline": False,
            "zeroline": True,
            "autorange": True,
            "visible": True,
            "showticklabels": True,
            # "titlefont": {"color": "darkgray"},
        },
    )
    return fig


@app.callback(Output('chart1', 'figure'), Output('chart2', 'figure'), Output('chart3', 'figure'),
              Output('chart4', 'figure'), Output('chart5', 'figure'), Output('chart6', 'figure'),
              Output('chart7', 'figure'), Output('chart8', 'figure'), Output('chart9', 'figure'),
              Output('chart10', 'figure'), Output('chart11', 'figure'), Output('chart12', 'figure'),
              Output('update-time', 'children'),
              Input('refresh-time', 'n_intervals'))
def UpdateCharts(n):
    if os.path.isfile('dashboard.csv'):
        dashboard = pd.read_csv('dashboard.csv', encoding='utf_8_sig')
        if not dashboard.empty:
            dashboard.set_index('code', inplace=True)
            if len(dashboard.index) > 12:
                dashboard = dashboard.iloc[:12, :]
            stockslist = dashboard.index
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
                   dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
                   html.Div(children='Last update time: ' + dt.datetime.now().strftime('%H:%M:%S'))
    else:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
               dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
               html.Div(children='Last update time: ' + dt.datetime.now().strftime('%H:%M:%S'))
    market_data = pd.read_csv('market_data.csv')
    market_data = market_data[market_data.ticker_direction != 'NEUTRAL']
    market_data['DateTime'] = pd.to_datetime(todayDate + ' ' + market_data['time'], format=format1)
    market_data.set_index(pd.DatetimeIndex(market_data['DateTime']), inplace=True)

    if len(stockslist) == 12:
        fig1 = generatingCharts(market_data, stockslist[0], dashboard)
        fig2 = generatingCharts(market_data, stockslist[1], dashboard)
        fig3 = generatingCharts(market_data, stockslist[2], dashboard)
        fig4 = generatingCharts(market_data, stockslist[3], dashboard)
        fig5 = generatingCharts(market_data, stockslist[4], dashboard)
        fig6 = generatingCharts(market_data, stockslist[5], dashboard)
        fig7 = generatingCharts(market_data, stockslist[6], dashboard)
        fig8 = generatingCharts(market_data, stockslist[7], dashboard)
        fig9 = generatingCharts(market_data, stockslist[8], dashboard)
        fig10 = generatingCharts(market_data, stockslist[9], dashboard)
        fig11 = generatingCharts(market_data, stockslist[10], dashboard)
        fig12 = generatingCharts(market_data, stockslist[11], dashboard)
        return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, fig12, \
               html.Div(children='Last update time: ' + dt.datetime.now().strftime('%H:%M:%S'))
    elif len(stockslist) == 11:
        fig1 = generatingCharts(market_data, stockslist[0], dashboard)
        fig2 = generatingCharts(market_data, stockslist[1], dashboard)
        fig3 = generatingCharts(market_data, stockslist[2], dashboard)
        fig4 = generatingCharts(market_data, stockslist[3], dashboard)
        fig5 = generatingCharts(market_data, stockslist[4], dashboard)
        fig6 = generatingCharts(market_data, stockslist[5], dashboard)
        fig7 = generatingCharts(market_data, stockslist[6], dashboard)
        fig8 = generatingCharts(market_data, stockslist[7], dashboard)
        fig9 = generatingCharts(market_data, stockslist[8], dashboard)
        fig10 = generatingCharts(market_data, stockslist[9], dashboard)
        fig11 = generatingCharts(market_data, stockslist[10], dashboard)
        return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, dash.no_update, \
               html.Div(children='Last update time: ' + dt.datetime.now().strftime('%H:%M:%S'))
    elif len(stockslist) == 10:
        fig1 = generatingCharts(market_data, stockslist[0], dashboard)
        fig2 = generatingCharts(market_data, stockslist[1], dashboard)
        fig3 = generatingCharts(market_data, stockslist[2], dashboard)
        fig4 = generatingCharts(market_data, stockslist[3], dashboard)
        fig5 = generatingCharts(market_data, stockslist[4], dashboard)
        fig6 = generatingCharts(market_data, stockslist[5], dashboard)
        fig7 = generatingCharts(market_data, stockslist[6], dashboard)
        fig8 = generatingCharts(market_data, stockslist[7], dashboard)
        fig9 = generatingCharts(market_data, stockslist[8], dashboard)
        fig10 = generatingCharts(market_data, stockslist[9], dashboard)
        return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, dash.no_update, dash.no_update, \
               html.Div(children='Last update time: ' + dt.datetime.now().strftime('%H:%M:%S'))
    elif len(stockslist) == 9:
        fig1 = generatingCharts(market_data, stockslist[0], dashboard)
        fig2 = generatingCharts(market_data, stockslist[1], dashboard)
        fig3 = generatingCharts(market_data, stockslist[2], dashboard)
        fig4 = generatingCharts(market_data, stockslist[3], dashboard)
        fig5 = generatingCharts(market_data, stockslist[4], dashboard)
        fig6 = generatingCharts(market_data, stockslist[5], dashboard)
        fig7 = generatingCharts(market_data, stockslist[6], dashboard)
        fig8 = generatingCharts(market_data, stockslist[7], dashboard)
        fig9 = generatingCharts(market_data, stockslist[8], dashboard)
        return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, dash.no_update, dash.no_update, dash.no_update, \
               html.Div(children='Last update time: ' + dt.datetime.now().strftime('%H:%M:%S'))
    elif len(stockslist) == 8:
        fig1 = generatingCharts(market_data, stockslist[0], dashboard)
        fig2 = generatingCharts(market_data, stockslist[1], dashboard)
        fig3 = generatingCharts(market_data, stockslist[2], dashboard)
        fig4 = generatingCharts(market_data, stockslist[3], dashboard)
        fig5 = generatingCharts(market_data, stockslist[4], dashboard)
        fig6 = generatingCharts(market_data, stockslist[5], dashboard)
        fig7 = generatingCharts(market_data, stockslist[6], dashboard)
        fig8 = generatingCharts(market_data, stockslist[7], dashboard)
        return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, dash.no_update, dash.no_update, dash.no_update, \
               dash.no_update, \
               html.Div(children='Last update time: ' + dt.datetime.now().strftime('%H:%M:%S'))
    elif len(stockslist) == 7:
        fig1 = generatingCharts(market_data, stockslist[0], dashboard)
        fig2 = generatingCharts(market_data, stockslist[1], dashboard)
        fig3 = generatingCharts(market_data, stockslist[2], dashboard)
        fig4 = generatingCharts(market_data, stockslist[3], dashboard)
        fig5 = generatingCharts(market_data, stockslist[4], dashboard)
        fig6 = generatingCharts(market_data, stockslist[5], dashboard)
        fig7 = generatingCharts(market_data, stockslist[6], dashboard)
        return fig1, fig2, fig3, fig4, fig5, fig6, fig7, dash.no_update, dash.no_update, dash.no_update, dash.no_update,\
               dash.no_update, \
               html.Div(children='Last update time: ' + dt.datetime.now().strftime('%H:%M:%S'))
    elif len(stockslist) == 6:
        fig1 = generatingCharts(market_data, stockslist[0], dashboard)
        fig2 = generatingCharts(market_data, stockslist[1], dashboard)
        fig3 = generatingCharts(market_data, stockslist[2], dashboard)
        fig4 = generatingCharts(market_data, stockslist[3], dashboard)
        fig5 = generatingCharts(market_data, stockslist[4], dashboard)
        fig6 = generatingCharts(market_data, stockslist[5], dashboard)
        return fig1, fig2, fig3, fig4, fig5, fig6, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
               dash.no_update, dash.no_update, \
               html.Div(children='Last update time: ' + dt.datetime.now().strftime('%H:%M:%S'))
    elif len(stockslist) == 5:
        fig1 = generatingCharts(market_data, stockslist[0], dashboard)
        fig2 = generatingCharts(market_data, stockslist[1], dashboard)
        fig3 = generatingCharts(market_data, stockslist[2], dashboard)
        fig4 = generatingCharts(market_data, stockslist[3], dashboard)
        fig5 = generatingCharts(market_data, stockslist[4], dashboard)
        return fig1, fig2, fig3, fig4, fig5, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,\
               dash.no_update, dash.no_update, \
               html.Div(children='Last update time: ' + dt.datetime.now().strftime('%H:%M:%S'))
    elif len(stockslist) == 4:
        fig1 = generatingCharts(market_data, stockslist[0], dashboard)
        fig2 = generatingCharts(market_data, stockslist[1], dashboard)
        fig3 = generatingCharts(market_data, stockslist[2], dashboard)
        fig4 = generatingCharts(market_data, stockslist[3], dashboard)
        return fig1, fig2, fig3, fig4, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
               dash.no_update, dash.no_update, dash.no_update, \
               html.Div(children='Last update time: ' + dt.datetime.now().strftime('%H:%M:%S'))
    elif len(stockslist) == 3:
        fig1 = generatingCharts(market_data, stockslist[0], dashboard)
        fig2 = generatingCharts(market_data, stockslist[1], dashboard)
        fig3 = generatingCharts(market_data, stockslist[2], dashboard)
        return fig1, fig2, fig3, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
               dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
               html.Div(children='Last update time: ' + dt.datetime.now().strftime('%H:%M:%S'))
    elif len(stockslist) == 2:
        fig1 = generatingCharts(market_data, stockslist[0], dashboard)
        fig2 = generatingCharts(market_data, stockslist[1], dashboard)
        return fig1, fig2, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
               dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
               html.Div(children='Last update time: ' + dt.datetime.now().strftime('%H:%M:%S'))
    elif len(stockslist) == 1:
        fig1 = generatingCharts(market_data, stockslist[0], dashboard)
        return fig1, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
               dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
               dash.no_update, html.Div(children='Last update time: ' + dt.datetime.now().strftime('%H:%M:%S'))
    else:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
               dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
               html.Div(children='Last update time: ' + dt.datetime.now().strftime('%H:%M:%S'))


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8088, debug=False, dev_tools_ui=False)
