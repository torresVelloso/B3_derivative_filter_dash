from datetime import datetime
import pandas as pd
#import plotly.express as px
import dash
from dash import dcc, html, Input, Output, dash_table, State


B3_file = 'COTAHIST_D14082024.txt' #using data: 12/08/2024
columns_size = [2,8,2,12,3,12,10,3,4,13,13,13,13,13,13,13,5,18,18,13,1,8,7,13,12,3]
df_b3 = pd.read_fwf(B3_file, widths =columns_size, header=0)
df_b3.columns = [
"tipo_registro",
"data_pregao",
"cod_bdi",
"cod_negociacao",
"tipo_mercado",
"noma_empresa",
"especificacao_papel",
"prazo_dias_merc_termo",
"moeda_referencia",
"preco_abertura",
"preco_maximo",
"preco_minimo",
"preco_medio",
"preco_ultimo_negocio",
"preco_melhor_oferta_compra",
"preco_melhor_oferta_venda",
"numero_negocios",
"quantidade_papeis_negociados",
"volume_total_negociado",
"preco_exercicio",
"ìndicador_correcao_precos",
"data_vencimento" ,
"fator_cotacao",
"preco_exercicio_pontos",
"codigo_isin",
"num_distribuicao_papel"]

df_b3 = df_b3.drop(len(df_b3["data_pregao"])-1)

# Ajustar valores com virgula (dividir os valores dessas colunas por 100)
listComma=[
"preco_abertura",
"preco_maximo",
"preco_minimo",
"preco_medio",
"preco_ultimo_negocio",
"preco_melhor_oferta_compra",
"preco_melhor_oferta_venda",
"volume_total_negociado",
"preco_exercicio",
"preco_exercicio_pontos"
]

for colum in listComma:
    df_b3[colum]=[i/100. for i in df_b3[colum]]


today= datetime.now().date()
df_b3['data_vencimento'] = pd.to_datetime(df_b3['data_vencimento'], format= '%Y%m%d', errors = 'coerce')
df_b3 = df_b3[df_b3['data_vencimento'] > pd.Timestamp(today)]

app = dash.Dash(__name__)

app.layout = html.Div([
                
                html.Div([
                    html.Label('Enter Ticker: '),
                    dcc.Input(id='tick', value='', type='text', placeholder='Enter ticker...')   
                        ]),       
                html.Div([
                    html.Label('Minimum Volume:'),
                    dcc.Input(id='volume', value='', type='number', placeholder='Enter min volume')
                        ]),
                html.Div(id='table-container'),
                html.Button('Search', id='search-button', n_clicks=0)
                        
                ])
@app.callback(
    Output('table-container', 'children'), #CONTINUE FROM HERE
    Input('search-button', 'n_clicks'),
    [State('tick', 'value'), State('volume','value')]
)

def update_table(n_clicks,tick,volume):
    
 if n_clicks > 0:
    #filter df based on input values
    filtered_df = df_b3.copy()
    
    if tick:
        filtered_df = filtered_df[(filtered_df['cod_negociacao'].str.contains(tick, case=False, na=False))]    

    if volume:
        filtered_df = filtered_df[filtered_df['volume_total_negociado']>= volume]

    filtered_df.drop(['tipo_registro',	'especificacao_papel',	'prazo_dias_merc_termo','moeda_referencia', 'ìndicador_correcao_precos' ,	
                      'fator_cotacao',	'preco_exercicio_pontos','num_distribuicao_papel','cod_bdi','preco_ultimo_negocio', 'preco_melhor_oferta_compra','preco_melhor_oferta_venda','preco_medio'], axis=1, inplace=True)
    # Sort the DataFrame by 'volume_total_negociado' in descending order
    filtered_df = filtered_df.sort_values(by='volume_total_negociado', ascending=False)
   
    # Verify that filtered_df is still a DataFrame and has not become a function or empty object
    if isinstance(filtered_df, pd.DataFrame):
        # Create a DataTable to display filtered data

        return dash_table.DataTable(
            data=filtered_df.to_dict('records'),
            columns=[{'name': col, 'id': col} for col in filtered_df.columns],
            style_table={'overflowX': 'auto'}  # Enable horizontal scrolling
        )
    else:
        # Return an error message or empty response if filtered_df is not a DataFrame
        return html.Div("No data available based on the filters.")

 return html.Div() #return empty div if no clicks or initial load
if __name__ == '__main__':
    app.run_server(debug=True)   









