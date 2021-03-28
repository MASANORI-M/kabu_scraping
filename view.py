import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import datetime
from assets.database import db_session
from assets.models import Data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#df = pd.read_csv('assets/kabu_data.csv')

data = db_session.query(Data.date, Data.kabukas, Data.dekidakas).all()

dates = []
kabukas = []
dekidakas = []

for datum in data:
    dates.append(datum.date)
    kabukas.append(datum.kabukas)
    dekidakas.append(datum.dekidakas)

diff_kabukas = pd.Series(kabukas).diff().values
diff_dekidakas = pd.Series(dekidakas).diff().values

# dates = []
# for _date in df['date']:
#     date = datetime.datetime.strptime(_date, '%Y/%m/%d').date()
#     dates.append(date)
#
# n_kabuka = df['kabuka'].values
# n_dekidaka = df['dekidaka'].values
#
# diff_kabuka = df['kabuka'].diff().values
# diff_dekidaka = df['dekidaka'].diff().values

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(children = [
    html.H2(children = '菊水化学工業株式会社株価、出来高推移Webスクレイピング'),
    html.Div(children = [
        dcc.Graph(
            id = 'kabuka_graph',
            figure = {
                'data':[
                    go.Scatter(
                        x = dates,
                        y = kabukas,
                        mode = 'lines+markers',
                        name = '株価推移[円]',
                        opacity = 0.7,
                        yaxis = 'y1'
                    ),
                    go.Bar(
                        x = dates,
                        y = diff_kabukas,
                        name = '株価増減[円]',
                        yaxis = 'y2'
                    )
                ],
                'layout': go.Layout(
                    title = '株価の推移',
                    xaxis = dict(title = 'date'),
                    yaxis = dict(title = '株価推移[円]', side = 'left', showgrid = False, range = [100, max(kabukas) + 10]),
                    yaxis2 = dict(title = '株価増減[円]', side = 'right', showgrid = False, overlaying = 'y', range = [0, max(kabukas[1:])]),
                    margin = dict(l = 200, r = 200, b = 100, t = 100)
                )
            }
        ),
        dcc.Graph(
            id = 'dekidaka_graph',
            figure = {
                'data':[
                    go.Scatter(
                        x = dates,
                        y = dekidakas,
                        mode = 'lines+markers',
                        name = '出来高数',
                        opacity = 0.7,
                        yaxis = 'y1'
                    ),
                    go.Bar(
                        x = dates,
                        y = diff_dekidakas,
                        name = '増減数',
                        yaxis = 'y2'
                    )
                ],
                'layout': go.Layout(
                    title = '出来高数の推移',
                    xaxis = dict(title = 'date'),
                    yaxis = dict(title = '出来高数', side = 'left', showgrid = False, range = [0, max(dekidakas) + 10]),
                    yaxis2 = dict(title = '増減数', side = 'right', showgrid = False, overlaying = 'y', range = [0, max(dekidakas[1:])]),
                    margin = dict(l = 200, r = 200, b = 100, t = 100)
                )
            }
        )

    ])
], style = {
    'textAlign' : 'center',
    'width' : '1200px',
    'margin' : '0 auto'
})

if __name__ == '__main__':
    app.run_server(debug=True)
