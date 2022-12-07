from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv('crimedata.csv')
states = sorted(df['state'].unique())
df['all_crimes'] = df['murders'] + df['rapes'] + df['robberies'] + df['assaults'] + df['burglaries'] + df[
    'larcenies'] + df['autoTheft'] + df['arsons']

app.layout = html.Div(children=[

    html.Div([
        html.Div([
            dcc.Dropdown(options={'all_crimes': 'Общее количество преступлений', 'autoTheftPerPop': 'Частота угонов',
                                  'burglPerPop': 'Частота кражи со взломом',
                                  'rapesPerPop': 'Частота изнасилований', 'murdPerPop': 'Частота убийств',
                                  'arsonsPerPop': 'Частота поджогов', 'larcPerPop': 'Частота воровств'},
                         value='autoTheftPerPop', id='crime')],
            style={'width': '45%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(options={'population': 'Население', 'medIncome': 'Средний доход',
                                  'blackPerCap': 'Доля чернокожих', 'PolicPerPop': 'Доля полиции',
                                  'pctUrban': 'Урбанизация'}, value='medIncome', id='feature')],
            style={'width': '45%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown([i for i in states], 'NY', id='state')], style={'width': '10%',
                                                                         'display': 'inline-block'}),
        dcc.Graph(id='graphic')
    ]),
    html.Div([
        html.Div([
            dcc.Dropdown([i for i in states], 'NY', id='state_2')], style={'width': '100%',
                                                                           'display': 'inline-block'}),
        dcc.Graph(id='pie_people')
    ]),
    html.Div([
        html.Div([
            dcc.Dropdown([i for i in states], 'NY', id='state_3')], style={'width': '100%',
                                                                           'display': 'inline-block'}),
        dcc.Graph(id='pie_crimes')
    ]),
    html.Div([
        html.Div([
            dcc.Dropdown(options={'all_crimes': 'Общее количество преступлений', 'autoTheftPerPop': 'Частота угонов',
                                  'burglPerPop': 'Частота кражи со взломом',
                                  'rapesPerPop': 'Частота изнасилований', 'murdPerPop': 'Частота убийств',
                                  'arsonsPerPop': 'Частота поджогов', 'larcPerPop': 'Частота воровств'},
                         value='all_crimes', id='type_of_crime')], style={'width': '100%',
                                                                          'display': 'inline-block'}),
        dcc.Graph(id='crimes_in_states')
    ]),
    html.Div([
        dcc.Graph(id='population_in_states',
                  figure=px.histogram(df.groupby(['state']).agg({'population': 'max'}).reset_index(), x='state',
                                      y='population').update_layout(xaxis_title='Штат', yaxis_title=f'Население',
                                                                    title=f'Население по штатам'))
    ]),
])


@app.callback(
    Output('graphic', 'figure'),
    Input('crime', 'value'),
    Input('feature', 'value'),
    Input('state', 'value'))
def update_graph(crime_value, feature_value, state):
    df_new = df[df['state'] == state]
    df_new = df_new.sort_values(by=feature_value)

    fig = px.line(
        df_new,
        y=crime_value,
        x=feature_value)
    fig.update_layout(xaxis_title=feature_value,
                      yaxis_title=crime_value,
                      title=f'Зависимость преступлений типа {crime_value} от {feature_value} в штате {state}')

    return fig


@app.callback(
    Output('pie_people', 'figure'),
    Input('state_2', 'value')
)
def update_output(state):
    df_new = df[df['state'] == state]
    df_new = df_new.iloc[0]
    fig = px.pie(df_new, names=['Чернокожие', 'Белые', 'Азиаты', 'Латиноамериканцы'],
                 values=[df_new['racepctblack'], df_new['racePctWhite'],
                         df_new['racePctAsian'], df_new['racePctHisp']])

    fig.update_layout(title=f'Соотношение рас людей в {state}')
    return fig


@app.callback(
    Output('pie_crimes', 'figure'),
    Input('state_3', 'value')
)
def update_output(state):
    df_new = df[df['state'] == state]
    df_new = df_new.iloc[0]
    fig = px.pie(df_new,
                 names=['Убийства', 'Изнасилование', 'Грабежи', 'assaults', 'Кражи', 'Воровство', 'Угоны', 'Поджоги'],
                 values=[df_new['murders'], df_new['rapes'],
                         df_new['robberies'], df_new['assaults'],
                         df_new['burglaries'], df_new['larcenies'],
                         df_new['autoTheft'], df_new['arsons']])

    fig.update_layout(title=f'Соотношение типов преступлений в {state}')
    return fig


@app.callback(
    Output('crimes_in_states', 'figure'),
    Input('type_of_crime', 'value'))
def update_output(type_of_crime):
    df_new = df.groupby(['state']).agg({type_of_crime: 'sum'}).reset_index()
    fig = px.histogram(df_new, x='state', y=type_of_crime)
    fig.update_layout(xaxis_title='Штат',
                      yaxis_title=f'Количество {type_of_crime}',
                      title=f'Количество {type_of_crime} по штатам')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
