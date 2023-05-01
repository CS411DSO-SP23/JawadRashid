from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
from mysql_utils import year_pub, prof_pub, add_uni, del_uni, chec_uni
from neo4j_utils import get_uni, get_ratio


import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


app = Dash(__name__)
widgets = [
    #widget 1
    [
        html.Div([
            html.H3(children = 'Comparision of Faculty among universitites', style={"textAlign":"center", "color": "#808080"}),
            dbc.Input(id = 'input_w1', style={"marginLeft":"180px"}),
            html.Button('Search', id = 'search_w1', style={"textAlign":"center"}),
            html.Br(),
            dcc.Graph(id = "fac_graph",style={'width': '50vh', 'height': '30vh'}),
                ]
                ),        
    ],
    #widget 2               
    [
        html.Div([
            html.H3(children = 'Comparision of Publications among universities within a range', style={"textAlign":"center", "color": "#808080"}),
            dbc.Input(id = 'range_1', style={"marginLeft":"130px"}),
            dcc.Input(id = 'range_2'),
            html.Button('Search', id = 'search_w2'),
            html.Br(),
            dcc.Graph(id = "pie_chart",style={'width': '50vh', 'height': '30vh'}),
            ]
            ),
            
    ], 
    #widget 3
    [
        html.Div([
            html.H3(children = 'Comparision of publications by Professor over years', style={"textAlign":"center", "color": "#808080"}),
            dbc.Input(id = 'input_w3', style={"marginLeft":"180px"}),
            html.Button('Search', id = 'search_w3'),
            html.Br(),
            dcc.Graph(id = 'prof_graph',style={'width': '50vh', 'height': '30vh'}),
  
            ]
            ),
            
    ], 
    #widget 4
    [
        html.Div([
            html.H3(children = 'Publications per Faculty Ratio', style={"textAlign":"center", "color": "#808080"}),
            dcc.Slider(5, 15, 5, value = 10, id='ratio_slider'),
            html.Div(id = 'slider-output'),
            dcc.Graph(id = "ratio_graph",style={'width': '50vh', 'height': '30vh'})
            ]
            ),
            
    ], 
    #widget 5
    [
        html.Div([
            html.H3(children = 'Add University', style={"textAlign":"center", "color": "#808080"}),
            dbc.Input(id = 'id_inp', placeholder = "Enter University ID", style={"marginLeft":"220px"}),
            html.Br(),
            dbc.Input(id = 'name_inp', placeholder = "Enter University Name", style={"marginLeft":"220px"}),
            html.Br(),
            dbc.Input(id = 'photo_inp', placeholder = "Enter Photo URL", style={"marginLeft":"220px"}),
            html.Br(),
            html.Br(),
            html.Button('Add University', id = 'add_button', style={"marginLeft":"245px"}),
            html.Br(),
            html.Br(),
            html.Br(),
            dbc.Input(id = 'search_uni', style={"marginLeft":"0px"}),
            html.Button('Search', id = 'search_add'),
            html.Br(),
            html.Br(),
            dash_table.DataTable(
                columns = [{'name': 'University Name', 'id': 'name'}, {'name': 'University Id', 'id': 'id'}],
                id='university_update'),
            html.Br(),
            dbc.Textarea(id='tid', placeholder="This is text area.", style={"width": "100%", "height": "50 px"}),
            ]
        ),          
    ],  
    #widget 6
    [
        html.Div([
            html.H3(children = 'Delete University', style={"textAlign":"center", "color": "#808080"}),
            dbc.Input(id = 'delete_input', style={"marginLeft":"210px"}),
            html.Button('Delete', id = 'search_delete'),
            html.Br(),
            html.Br(),
            html.Br(),
            dbc.Textarea(id='tid_delete', placeholder="This is text area.", style={"width": "98%", "height": "50 px"})
            ]
        ), 
    ]
    ]
background_color: str = "rgb(255,255,255)"

#widget 1
@callback(
    Output('fac_graph', 'figure'),
    State('input_w1', 'value'),
    Input('search_w1', 'n_clicks'),
    )

def update_bar_chart(input_value, n_clicks):
    if not input_value:
        return dash.no_update
    
    dff = get_uni(input_value)
    
    barchart = px.bar(
        data_frame = dff,
        x = dff['university_name'],
        y = dff['faculty_count'],
    )
    return (barchart)

#widget 2
@callback(
    Output('pie_chart', 'figure'),
    State('range_1', 'value'),
    State('range_2', 'value'),
    Input('search_w2', 'n_clicks'))

def update_pie(range1, range2, n_clicks):
    dff = year_pub(range1, range2)

    pie = px.pie(
        data_frame = dff,
        values = dff['Publications'],
        names = dff['University'])
    return (pie)

#widget 3
@callback(
    Output('prof_graph', 'figure'),
    State('input_w3', 'value'),
    Input('search_w3', 'n_clicks'),)
def update_histo(input_value, n_clicks):
    if not input_value:
        return dash.no_update
    
    dff = prof_pub(input_value)

    histo = px.histogram(
        data_frame = dff,
        x = dff['year'],
        y = dff['count'])
    return (histo)

#widget 4
@callback(
    #Output('slider-output', 'children'),
    Output('ratio_graph', 'figure'),
    Input('ratio_slider', 'value'))

def update_slider(input_value):

    dff = get_ratio(input_value)

    barchart = px.histogram(
        data_frame = dff,
        x = dff['university.name'],
        y = dff['Publ_to_Faclty_Ratio']
    )
    return barchart

#widget 5


@callback(
    Output('university_update', 'data'),
    State('search_uni'        , 'value'),
    Input('search_add'        , 'n_clicks')
)
def update_table(search_uni, n_clicks):
    if not search_uni:
        return dash.no_update
    
    result = chec_uni(search_uni)
    return(result)


@callback(
    Output('tid', 'value'),
    State('id_inp'   , 'value'),
    State('name_inp' , 'value'),
    State('photo_inp', 'value'),
    Input('add_button'  , 'n_clicks')
)
def update_uni(id_value, name_value, photo_value, n_clicks):
    if not id_value and name_value and photo_value:
        return dash.no_update
    add_uni(id_value, name_value, photo_value)
    result = chec_uni(name_value)
    print(result)
    return (result)

#widget 6
@callback(
    Output('tid_delete', 'value'),
    State('delete_input', 'value'),
    Input('search_delete', 'n_clicks')
)
def delete_uni_table(uni_name, n_clicks):
    if not uni_name:
        return dash.no_update
    del_uni(uni_name)
    result = chec_uni(uni_name)
    print(result)
    return result
 


app.layout = html.Div([
    html.H1(children='Comparision of Faculty and Publications among Universities', style={"textAlign":"center", "color": "#FF5F05"}),
    dbc.Modal([dbc.ModalHeader(dbc.ModalTitle(id="enlarge_widget_title"), close_button=True), dbc.ModalBody(id="enlarge_widget_body")], "enlarge_widget", size="xl", is_open=False, centered=True),
    html.Table(html.Tbody(
        [html.Tr([
                    #widget 1
                    html.Td(
                        html.Div(widgets[0], style={"border":"5px solid #FF5F05", "borderRadius":"20px", "margin":"auto", "background":background_color, "height":"420px"}), style={"paddingLeft":"5px", "paddingRight":"5px", "paddingBottom":"5px"}
                    ), 
                    #widget 2
                    html.Td(
                        html.Div(widgets[1], style={"padding":"1%", "border":"5px solid #FF5F05", "borderRadius":"20px", "background":background_color, "margin":"auto", "height":"420px"}), style={"paddingLeft":"5px", "paddingRight":"5px", "paddingBottom":"5px"}
                        ),
                    #widget 3
                    html.Td(
                        html.Div(widgets[2], style={"padding":"1%", "margin":"auto", "border":"5px solid #FF5F05", "borderRadius":"20px", "background":background_color, "height": "420px"}), style={"paddingLeft":"5px", "paddingRight":"5px", "paddingBottom":"5px"}
                        )
                ]),
         html.Tr([
                    #widget 4
                    html.Td(
                        html.Div(widgets[3], style={"padding":"1%", "margin":"auto", "border":"5px solid #FF5F05", "borderRadius":"20px", "background":background_color, "height":"420px"}), style={"paddingLeft":"5px", "paddingRight":"5px"}
                        ),
                    #widget 5
                    html.Td(
                        html.Div(widgets[4], style={"padding":"1%", "margin":"auto", "border":"5px solid #FF5F05", "borderRadius":"20px", "background":background_color, "height":"420px"}), style={"paddingLeft":"5px", "paddingRight":"5px"}
                        ),
                    #widget 6
                    html.Td(
                        html.Div(widgets[5], style={"border":"5px solid #FF5F05", "borderRadius":"20px", "margin":"auto", "background":background_color, "height":"420px"}), style={"paddingLeft":"5px", "paddingRight":"5px"}
                        ), 
                ])
        ]
    ), style={"tableLayout": "fixed", "width": "100%", "height": "100%"}),
    html.H6(id="faculty_info_widget_change_trigger", style={"visibility":"hidden"})
], style={"background":"rgb(255,255,255)", "margin":0, "padding":0, "width":"100%", "height":"100%", "top":"0px", "left":"0px", "zIndex":"1000"})


if __name__ == '__main__':
    app.run_server()
