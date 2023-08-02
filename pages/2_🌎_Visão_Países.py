# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

# bibliotecas necessárias
import folium
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import re
import inflection
import locale
from forex_python.converter import CurrencyRates
from currency_converter import CurrencyConverter


st.set_page_config( page_title='Visão Países', page_icon='🌎', layout='wide')

# =====================================================================================================
# Funções
#======================================================================================================
def restaurant_by_countries( df1 ):
    """ Esta função tem a responsabilidade de plotar um gráfico de barras
        Tipos de ações:
        1. Dataframe - Quantidade de restaurantes por país
        2. Filtra as colunas 'country_name', 'restaurant_id'
        3. Agrupar por 'country_name'
        4. Contar as linhas
        5. Classificar pela coluna 'restaurant_id'
        6. Renomear as colunas para 'Países' e 'Quantidade de Restaurantes'
        7. Desenhar e plotar um gráfico de linhas
        8. Personalizar a fonte do eixo 'x' e 'y'
                      
        Input: Dataframe
        Output: Gráfico de barras         
    """
    # Contar quantidade de restaurante por país
    df_aux = ( df1.loc[:, ['country_name', 'restaurant_id']]
                  .groupby('country_name')
                  .count().reset_index()
                  .sort_values('restaurant_id', ascending=False) )
    
    df_aux.columns = ['Países', 'Quantidade de Restaurantes']              
    # Desenhar gráfico de Barras
    fig = px.bar( df_aux, x='Países', y='Quantidade de Restaurantes', text='Quantidade de Restaurantes',    color_discrete_sequence=['#4472C4'])
    fig.update_traces(textfont_size=12)
    fig.update_layout( title='Quantidade de Restaurantes por país', title_x=0.3, title_font=dict(size=14, family='Arial Black', color='white'))
    # Personalize a fonte do eixo x
    fig.update_xaxes(tickfont=dict(size=12, family='Arial', color='white'), showgrid=False, title_font=dict(size=14,      family='Arial', color='white'))

    # Personalize a fonte do eixo y
    fig.update_yaxes(tickfont=dict(size=10, family='Arial', color='white'), showgrid=False, showticklabels=False, title_font=dict(size=14, family='Arial', color='white'))

    return fig


def cities_by_countries( df1 ):
    """ Esta função tem a responsabilidade de plotar um gráfico de barras
        Tipos de ações:
        1. Dataframe - Quantidade de cidades por país
        2. Filtra as colunas 'country_name', 'city'
        3. Agrupar por 'country_name'
        4. Contar as linhas únicas
        5. Classificar pela coluna 'city'
        6. Renomear as colunas para 'Países' e 'Quantidade de Cidades'
        7. Desenhar e plotar um gráfico de barras
        8. Personalizar a fonte do eixo 'x' e 'y'
                      
        Input: Dataframe
        Output: Gráfico de linhas         
    """
    # Contar quantidade de cidades por país
    df_aux = ( df1.loc[:, ['country_name', 'city']]
                  .groupby('country_name')
                  .nunique().reset_index()
                  .sort_values('city', ascending=False) )
    
    df_aux.columns = ['Países', 'Quantidade de Cidades']
    
    # Desenhar gráfico de Barras
    fig = px.bar( df_aux, x='Países', y='Quantidade de Cidades', text='Quantidade de Cidades', color_discrete_sequence=['#4472C4'])
    fig.update_traces(textfont_size=12)
    fig.update_layout( title='Quantidade de Cidades por país', title_x=0.3, title_font=dict(size=14, family='Arial Black', color='white'))
    
    # Personalize a fonte do eixo x
    fig.update_xaxes(tickfont=dict(size=12, family='Arial', color='white'), showgrid=False, title_font=dict(size=14,      family='Arial', color='white'))

    # Personalize a fonte do eixo y
    fig.update_yaxes(tickfont=dict(size=10, family='Arial', color='white'), showgrid=False, showticklabels=False, title_font=dict(size=14, family='Arial', color='white'))

    return fig


def avg_cities_by_countries( df1 ):
    """ Esta função tem a responsabilidade de plotar um gráfico de barras
        Tipos de ações:
        1. Dataframe - Quantidade média de avaliações por país
        2. Filtra as colunas 'country_name', 'votes'
        3. Agrupar por 'country_name'
        4. Calcular a média
        5. Classificar pela coluna 'votes'
        6. Renomear as colunas para 'Países' e 'Quantidade de Avaliações'
        7. Desenhar e plotar um gráfico de barras
        8. Personalizar a fonte do eixo 'x' e 'y'
                      
        Input: Dataframe
        Output: Gráfico de barras         
    """
    # Quantidade média de avaliações por país
    df_aux = ( df1.loc[:, ['country_name', 'votes']]
                  .groupby('country_name')
                  .mean().reset_index()
                  .sort_values('votes', ascending=False))
    df_aux['votes'] = df_aux['votes'].map('{:.0f}'.format)
    df_aux.columns = ['Países', 'Quantidade de Avaliações']
    
    # Desenhar gráfico de Barras
    fig = px.bar( df_aux, x='Países', y='Quantidade de Avaliações', text='Quantidade de Avaliações', color_discrete_sequence=['#4472C4'])
    fig.update_traces(textfont_size=12)
    
    # Personalize a fonte do eixo x
    fig.update_xaxes(tickfont=dict(size=12, family='Arial', color='white'), showgrid=False, title_font=dict(size=14, family='Arial', color='white'))

    # Personalize a fonte do eixo y
    fig.update_yaxes(tickfont=dict(size=10, family='Arial', color='white'), showgrid=False, showticklabels=False, title_font=dict(size=14, family='Arial', color='white'))

    return fig



def avg_for_two_by_countries( df1 ):
    """ Esta função tem a responsabilidade de plotar um gráfico de barras
        Tipos de ações:
        1. Dataframe - Preço médio de prato para duas pessoas por país
        2. Filtra as colunas 'country_name', 'average_cost_usd'
        3. Agrupar por 'country_name'
        4. Calcular a média
        5. Classificar pela coluna 'average_cost_usd'
        6. Fomatar a coluna 'average_cost_usd' para mostrar 2 dígitos após o separador
        6. Renomear as colunas para 'Países' e 'Preço Médio Prato duas pessoa'
        7. Desenhar e plotar um gráfico de barras
        8. Personalizar a fonte do eixo 'x' e 'y'
                      
        Input: Dataframe
        Output: Gráfico de barras         
    """
    # Preço médio prato para duas pessoas
    df_aux = ( df1.loc[:, ['average_cost_usd', 'country_name']]
                        .groupby('country_name')
                        .mean().reset_index()
                        .sort_values('average_cost_usd', ascending=False) )
    df_aux['average_cost_usd'] = df_aux['average_cost_usd'].map('{:.2f}'.format)
    df_aux.columns = ['Países', 'Preço Médio Prato duas pessoas']    
         
    # Desenhar gráfico de Barras
    fig = px.bar( df_aux, x='Países', y='Preço Médio Prato duas pessoas', text='Preço Médio Prato duas pessoas', color_discrete_sequence=['#4472C4'])
    fig.update_traces(textfont_size=12)
    
    # Personalize a fonte do eixo x
    fig.update_xaxes(tickfont=dict(size=12, family='Arial', color='white'), showgrid=False, title_font=dict(size=14, family='Arial', color='white'))

    # Personalize a fonte do eixo y
    fig.update_yaxes(tickfont=dict(size=10, family='Arial', color='white'), showgrid=False, showticklabels=False, title_font=dict(size=14, family='Arial', color='white'))

    return fig



def clean_code( df1 ):
    """ Esta função tem a responsabilidade de limpar o dataframe
        Tipos de limpeza:
        1. Remoção dos dados NaN
        2. Mudança do tipo da coluna de dados
        3. Remoção dos espaços da variáveis de texto
        4. Renomear as colunas do Dataframe
        5. Crias novas colunas
        6. Categorizar colunas
        7. Conversão de valores de coluna

        Input: Dataframe
        Output: Dataframe        
    """
    
    # 1. Removendo os espacos dentro de strings/texto/object
    df1.loc[:, 'Restaurant Name'] = df1.loc[:, 'Restaurant Name'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Address'] = df1.loc[:, 'Address'].str.strip()
    df1.loc[:, 'Locality'] = df1.loc[:, 'Locality'].str.strip()
    df1.loc[:, 'Locality Verbose'] = df1.loc[:, 'Locality Verbose'].str.strip()
    df1.loc[:, 'Cuisines'] = df1.loc[:, 'Cuisines'].str.strip()
    df1.loc[:, 'Currency'] = df1.loc[:, 'Currency'].str.strip()
    df1.loc[:, 'Rating color'] = df1.loc[:, 'Rating color'].str.strip()
    df1.loc[:, 'Rating text'] = df1.loc[:, 'Rating text'].str.strip()
    
    # 2. Renomear as colunas do DataFrame
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "_")
    cols_old = list(df1.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df1.columns = cols_new

    # 3. Categorizar, todos os restaurantes somente por um tipo de culinária
    df1["cuisines"] = df1.loc[:, "cuisines"].astype(str).apply(lambda x: x.split(",")[0])

    # 4 . Exluir dados duplicados na coluna Restaurants ID.
    df1['restaurant_id'] = df1['restaurant_id'].drop_duplicates()
    df1 = df1.dropna(subset=['restaurant_id'])
    df1['restaurant_id'] = df1['restaurant_id'].astype('int64')

    #limpando linhas 'nan' da coluna identificada
    linhas_vazias = df1['cuisines'] != 'nan'
    df1 = df1.loc[linhas_vazias, :]

    #Excluir as linhas com 'Mineira' na coluna 'cuisines'
    linhas_vazias = df1['cuisines'] != 'Mineira'
    df1 = df1.loc[linhas_vazias, :]

    #Excluir as linhas com 'Drinks Only' na coluna 'cuisines'
    linhas_vazias = df1['cuisines'] != 'Drinks Only'
    df1 = df1.loc[linhas_vazias, :]

    # 5. Excluir a linha com base no valor do Restaurant ID (nesse caso, 16608070)
    restaurant_id_to_delete = 16608070
    df1 = df1[df1['restaurant_id'] != restaurant_id_to_delete]

    # 6. Redefinir os índices do dataframe após a exclusão da linha:
    df1.reset_index(drop=True, inplace=True)

    return df1

#Criar coluna de categoria com base no range de valores
def create_price_type(df1):
    def get_price_type(price_range):
        if price_range == 1:
            return 'cheap'
        elif price_range == 2:
            return 'normal'
        elif price_range == 3:
            return 'expensive'
        else:
            return 'gourmet'

    df1['price_type'] = df1['price_range'].apply(get_price_type)
        
    return df1


#Substituir a coluna com o ID dos paises pelo nome do país
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}

def country_name(country_code):
    return COUNTRIES.get(country_code, "Unknown")

# Renomear a coluna 'country_code' por 'country_name'
def rename_country( df1 ):
    df1['country_code'] = df1['country_code'].apply(country_name)
    df1 = df1.rename(columns={'country_code': 'country_name'})
    return df1


# Criar coluna com o nome das cores com base nos códigos de cores
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}

def color_name(rating_color):
    return COLORS.get(rating_color)

def color_rename_name ( df1 ):
    df1['color_name'] = df1['rating_color'].apply(color_name)

    return df1


# Dicionário de taxas de câmbio para conversão para dólar americano
exchange_rates = {
    'Botswana Pula(P)': 0.0907,   # Taxa de câmbio dia 14/07/23 para Botswana Pula para USD
    'Brazilian Real(R$)': 0.1922,   # Taxa de câmbio dia 14/07/23 para Real brasileiro para USD
    'Dollar($)': 1.0,      # Taxa de câmbio dia 14/07/23 para Dólar para USD
    'Emirati Diram(AED)': 0.2723,   # Taxa de câmbio dia 14/07/23 para Emirati Dirham para USD
    'Indian Rupees(Rs.)': 0.0134,   # Taxa de câmbio dia 14/07/23 para Rúpia indiana para USD
    'Indonesian Rupiah(IDR)': 7.1e-5,   # Taxa de câmbio dia 14/07/23 para Rupia indonésia para USD
    'NewZealand($)': 0.7033,   # Taxa de câmbio dia 14/07/23 para Dólar da Nova Zelândia para USD
    'Pounds(£)': 1.3804,   # Taxa de câmbio dia 14/07/23 para Libra esterlina para USD
    'Qatari Rial(QR)': 0.2747,   # Taxa de câmbio dia 14/07/23 para Rial do Qatar para USD
    'Rand(R)': 0.0675,   # Taxa de câmbio dia 14/07/23 para Rand sul-africano para USD
    'Sri Lankan Rupee(LKR)': 0.005,    # Taxa de câmbio dia 14/07/23 para Rupia do Sri Lanka para USD
    'Turkish Lira(TL)': 0.1147    # Taxa de câmbio dia 14/07/23 para Lira turca para USD
}

# Função para converter o valor para dólar americano
def convert_to_usd( row ):
    currency = row['currency']
    average_cost = row['average_cost_for_two']
    
    if currency in exchange_rates:
        exchange_rate = exchange_rates[currency]
        converted_cost = average_cost * exchange_rate
        return converted_cost
    else:
        return average_cost

# Criar a nova coluna 'average_cost_usd' com os valores convertidos
def average_cost_usd ( df1 ):
    df1['average_cost_usd'] = round(df1.apply(convert_to_usd, axis=1), 2)

    return df1
    

# ====================================Inicio da estrutura lógica do código==============================
    
# ======================================
# Import dataset
# ======================================
df = pd.read_csv( 'dataset\zomato.csv' )

# ======================================
#Limpando os dados
# ======================================
df1 = clean_code( df )
# ======================================
#Criar coluna de categoria com base no range de valores
df1 = create_price_type(df1)
# ======================================
#Renomear coluna Country_Code
df1 = rename_country( df1 )
# ======================================
# Criar coluna com o nome das cores com base nos códigos de cores
df1 = color_rename_name ( df1 )
# ======================================
# Converter o valor da coluna para dólar americano
df1 = average_cost_usd ( df1 )
# ======================================

# =======================================
# Barra Lateral
# =======================================
st.title( '🌎' 'Fome Zero - Visão Países' )

#image_path = 'pngwing.com.png'
image = Image.open( 'pngwing.com.png' )
st.sidebar.image( image, width=230 )

st.sidebar.markdown( '# Fome Zero Company' )
st.sidebar.markdown( '#### Restaurant Management Platform in Countries and Town' )
st.sidebar.markdown( """---""" )

st.sidebar.markdown( '# Filtro' )

country_options = st.sidebar.multiselect( 
    'Escolha os países que deseja visualizar as informações',
    ['Australia', 'Brazil', 'Canada', 'England', 'India', 'Indonesia', 'New Zeland', 'Philippines', 'Qatar', 'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates', 'United States of America'], 
    default=['Australia', 'Brazil', 'Canada', 'England', 'India', 'Indonesia', 'New Zeland', 'Philippines', 'Qatar', 'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates', 'United States of America'] )

st.sidebar.markdown( """---""" )
st.sidebar.markdown( '### Powered by Wagner Sobrinho' )

# Filtro de país
linhas_selecionadas = df1['country_name'].isin( country_options )
df1 = df1.loc[linhas_selecionadas, :]


# =======================================
# Layout no Streamlit
# =======================================
with st.container():
    fig = restaurant_by_countries( df1 )
    st.plotly_chart(fig,use_container_width=True)


with st.container():
    st.markdown("""---""")
    fig = cities_by_countries( df1 )
    st.plotly_chart(fig,use_container_width=True)

with st.container():
    st.markdown("""---""")
    col1, col2 = st.columns( 2 )
        
    with col1:
        st.markdown( '###### Quantidade média de avaliação por país' )
        fig = avg_cities_by_countries( df1 )
        st.plotly_chart( fig, use_container_width=True )       
            
    with col2:
        st.markdown( '###### Preço médio prato para duas pessoas por país' )
        fig = avg_for_two_by_countries( df1 )
        st.plotly_chart( fig, use_container_width=True )              









            
        