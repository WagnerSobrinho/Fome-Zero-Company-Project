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


st.set_page_config( page_title='Visão Cidades', page_icon='🏙️', layout='wide')

# =====================================================================================================
# Funções
#======================================================================================================
def top_restaurant( df1 ):
    """ Esta função tem a responsabilidade de plotar um gráfico de barras
        Tipos de ações:
        1. Dataframe - Top 10 Cidades com mais restaurantes cadastrados
        2. Filtra as colunas 'country_name', 'city'
        4. Agrupa por 'country_name' e 'city'
        5. Contar as cidades, renomeie para 'Quantidade de Restaurantes'
        6. Classificar pelas colunas 'Quantidade de Restaurantes'  e 'country_name'
        7. Agrupa por cidades e define para mostrar 10 cidades
        8. Desenhar e plotar um gráfico de barras
        9. Personalizar a fonte do eixo 'x' e 'y'
                      
        Input: Dataframe
        Output: Gráfico de barras         
    """
    #Top 10 Cidades com mais restaurantes cadastrados
    top_cities = df1.groupby(['country_name', 'city']).size().reset_index(name='Quantidade de Restaurantes')
    top_cities = top_cities.sort_values(['Quantidade de Restaurantes', 'country_name'], ascending=[False, True]).head(10)
    top_cities = top_cities.groupby('city').head(10)
        
    # Plota o gráfico de barras
    fig = px.bar(top_cities, x='city', y='Quantidade de Restaurantes', text='Quantidade de Restaurantes', color='country_name')
    fig.update_traces(textfont_size=12)

    fig.update_layout(
    title='Top 10 Cidades com mais restaurantes cadastrados',
    title_x=0.3,
    title_font=dict(size=14, family='Arial', color='white'),
)
    fig.update_layout(xaxis_title='Cidade', yaxis_title='Quantidade de Restaurantes', showlegend=True,
                  legend_title_text='País')

    # Personalize a fonte do eixo x
    fig.update_xaxes(
    tickfont=dict(size=12, family='Arial', color='white'),
    showgrid=False,
    title_font=dict(size=14, family='Arial', color='white'),
)

    # Personalize a fonte do eixo y
    fig.update_yaxes(
    tickfont=dict(size=12, family='Arial', color='white'),
    showgrid=False,
    showticklabels=False,
    title_font=dict(size=14, family='Arial', color='white'),
)

    return fig


def top7_cities_aval4( df1 ):
    """ Esta função tem a responsabilidade de plotar um gráfico de barras
        Tipos de ações:
        1. Dataframe - Top 7 cidades com mais restaurantes com média de avaliação acima de 4
        2. Filtra as linhas da coluna 'aggregate_rating' com avaliação maio que 4
        3. Filtra as colunas 'restaurant_id', 'city' e 'country_name'
        4. Agrupa por 'country_name' e 'city'
        5. Contar as cidades, renomeie para 'Quantidade de Restaurantes'
        6. Classificar pelas colunas 'Quantidade de Restaurantes'  e 'country_name'
        7. Agrupa por cidades e define para mostrar 7 cidades
        8. Desenhar e plotar um gráfico de barras
        9. Personalizar a fonte do eixo 'x' e 'y'
                      
        Input: Dataframe
        Output: Gráfico de barras         
    """
    
    #Top 7 cidades com mais restaurantes com média de avaliação acima de 4'
    top_cities = df1.loc[df1['aggregate_rating'] > 4, ['restaurant_id', 'city', 'country_name']].groupby(['country_name', 'city']).size().reset_index(name='Quantidade de Restaurantes')
    top_cities = top_cities.sort_values(['Quantidade de Restaurantes', 'country_name'], ascending=[False, True]).head(7)
    top_cities = top_cities.groupby('city').head(7)
        
    # Plota o gráfico de barras
    fig = px.bar(top_cities, x='city', y='Quantidade de Restaurantes', text='Quantidade de Restaurantes', color='country_name')
    fig.update_traces(textfont_size=12)  
    fig.update_layout(xaxis_title='Cidade', yaxis_title='Quantidade de Restaurantes', showlegend=True,
                  legend_title_text='País')

    # Personalize a fonte do eixo x
    fig.update_xaxes(
    tickfont=dict(size=12, family='Arial', color='white'),
    showgrid=False,
    title_font=dict(size=14, family='Arial', color='white'),
)

    # Personalize a fonte do eixo y
    fig.update_yaxes(
    tickfont=dict(size=12, family='Arial', color='white'),
    showgrid=False,
    showticklabels=False,
    title_font=dict(size=14, family='Arial', color='white'),
)

    return fig


def top7_cities_aval25( df1 ):
    """ Esta função tem a responsabilidade de plotar um gráfico de barras
        Tipos de ações:
        1. Dataframe - Top 7 cidades com mais restaurantes com média de avaliação abaixo de 2.5
        2. Filtra as linhas da coluna 'aggregate_rating' com avaliação menor que 2.5
        3. Filtra as colunas 'restaurant_id', 'city' e 'country_name'
        4. Agrupa por 'country_name' e 'city'
        5. Contar as cidades, renomeie para 'Quantidade de Restaurantes'
        6. Classificar pelas colunas 'Quantidade de Restaurantes'  e 'country_name'
        7. Agrupa por cidades e define para mostrar 7 cidades
        8. Desenhar e plotar um gráfico de barras
        9. Personalizar a fonte do eixo 'x' e 'y'
                      
        Input: Dataframe
        Output: Gráfico de barras         
    """
#Top 7 cidades com mais restaurantes com média de avaliação abaixo de 2.5'

    top_cities = df1.loc[df1['aggregate_rating'] < 2.5, ['restaurant_id', 'city', 'country_name']].groupby(['country_name', 'city']).size().reset_index(name='Quantidade de Restaurantes')
    top_cities = top_cities.sort_values(['Quantidade de Restaurantes', 'country_name'], ascending=[False, True]).head(7)
    top_cities = top_cities.groupby('city').head(7)
        
    # Plota o gráfico de barras
    fig = px.bar(top_cities, x='city', y='Quantidade de Restaurantes', text='Quantidade de Restaurantes', color='country_name')
    fig.update_traces(textfont_size=12)
    fig.update_layout(xaxis_title='Cidade', yaxis_title='Quantidade de Restaurantes', showlegend=True,
                  legend_title_text='País')

    # Personalize a fonte do eixo x
    fig.update_xaxes(
    tickfont=dict(size=12, family='Arial', color='white'),
    showgrid=False,
    title_font=dict(size=14, family='Arial', color='white'),
)

    # Personalize a fonte do eixo y
    fig.update_yaxes(
    tickfont=dict(size=12, family='Arial', color='white'),
    showgrid=False,
    showticklabels=False,
    title_font=dict(size=14, family='Arial', color='white'),
)

    return fig


def top10_cities_culinaria_unica( df1 ):
    """ Esta função tem a responsabilidade de plotar um gráfico de barras
        Tipos de ações:
        1. Dataframe - 10 cidades com mais restaurantes com tipo de culinária única
        2. Filtra as colunas 'cuisines', 'city' e 'country_name'
        3. Agrupa por 'country_name' e 'city'
        4. Contas as cidades únicas
        5. Classificar pelas colunas 'cuisines'  e 'country_name'
        6. Agrupa por cidades e define para mostrar 10 cidades
        7. Desenhar e plotar um gráfico de barras
        8. Personalizar a fonte do eixo 'x' e 'y'
                      
        Input: Dataframe
        Output: Gráfico de barras         
    """
    #Top 10 cidades com mais restaurantes com tipo de culinária única
    top_cities = df1.loc[:,['cuisines', 'city', 'country_name']].groupby(['country_name', 'city']).nunique().reset_index()
    top_cities = top_cities.sort_values(['cuisines', 'country_name'], ascending=[False, True]).head(10)
    top_cities = top_cities.groupby('city').head(10)
        
    # Plota o gráfico de barras
    fig = px.bar(top_cities, x='city', y='cuisines', text='cuisines', color='country_name')
    fig.update_traces(textfont_size=12)

    fig.update_layout(
    title='Top 10 Cidades com mais restaurantes com tipo de culinária única',
    title_x=0.3,
    title_font=dict(size=14, family='Arial', color='white'),
)
    fig.update_layout(xaxis_title='Cidade', yaxis_title='Quantidade de Restaurantes', showlegend=True,
                  legend_title_text='País')

    # Personalize a fonte do eixo x
    fig.update_xaxes(
    tickfont=dict(size=12, family='Arial', color='white'),
    showgrid=False,
    title_font=dict(size=14, family='Arial', color='white'),
)

    # Personalize a fonte do eixo y
    fig.update_yaxes(
    tickfont=dict(size=12, family='Arial', color='white'),
    showgrid=False,
    showticklabels=False,
    title_font=dict(size=14, family='Arial', color='white'),
)

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
df = pd.read_csv( '\dataset\zomato.csv' )

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
# Função para converter o valor para dólar americano
df1 = average_cost_usd ( df1 )
# ======================================

# =======================================
# Barra Lateral
# =======================================
st.title( '🏙️' 'Fome Zero - Visão Cidades' )

#image_path = 'pngwing.com.png'
image = Image.open( 'pngwing.com.png' )
st.sidebar.image( image, width=230 )

st.sidebar.markdown( '# Fome Zero Company' )
st.sidebar.markdown( '#### Restaurant Management Platform in Countries and Town' )
st.sidebar.markdown( """---""" )

st.sidebar.markdown( '# Filtro' )

countries = st.sidebar.multiselect( 
    'Escolha os países que deseja visualizar as informações',
    df1.loc[:, 'country_name'].unique(), 
    default=['Australia', 'Brazil', 'Canada', 'England', 'India', 'Indonesia', 'New Zeland', 'Philippines', 'Qatar', 'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates', 'United States of America'] )

st.sidebar.markdown( """---""" )
st.sidebar.markdown( '### Powered by Wagner Sobrinho' )

# Filtro de país
linhas_selecionadas = df1['country_name'].isin( countries )
df1 = df1.loc[linhas_selecionadas, :]


# =======================================
# Layout no Streamlit
# =======================================
with st.container():
    fig = top_restaurant( df1 )
    st.plotly_chart(fig,use_container_width=True)
   
with st.container():
    st.markdown("""---""")
    col1, col2 = st.columns( 2 )
        
    with col1:
        st.markdown( '###### Top 7 cidades com mais restaurantes com média de avaliação acima de 4' )
        fig = top7_cities_aval4( df1 )
        st.plotly_chart( fig, use_container_width=True )       
            
    with col2:
        st.markdown( '###### Top 7 cidades com mais restaurantes com média de avaliação abaixo de 2.5' )
        fig = top7_cities_aval25( df1 )
        st.plotly_chart( fig, use_container_width=True )

with st.container():
    st.markdown("""---""")
    fig = top10_cities_culinaria_unica( df1 )
    st.plotly_chart(fig,use_container_width=True)     
