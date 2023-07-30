# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

# bibliotecas necessárias
import folium
import pandas as pd
import streamlit as st
from folium.plugins import MarkerCluster
from PIL import Image
from streamlit_folium import folium_static
import re
import inflection
import locale
from forex_python.converter import CurrencyRates
from currency_converter import CurrencyConverter


st.set_page_config( page_title='Visão Geral', page_icon='🏢', layout='wide')

# =====================================================================================================
# Funções
#======================================================================================================
def criar_map(df1):
    # """ Esta função tem a responsabilidade de plotar um mapa
    #     Tipos de ações:
    #     1. Dataframe - Cidades com latitude e longitude
    #     2. Criar uma figura e definir o tamanho
    #     3. Defnir o mapa e add na figura
    #     4. Definira clausterização e add no mapa
    #     5. Selecionar as colunas 'restaurant_name', 'average_cost_usd', 'cuisines', 'aggregate_rating' e 'color_name'
    #     2. Definir um for para que traga a informações acima seja mostrada em um popup assim que a posição seja escolhida
    #     4. Definir os marcadores no mapa, selecionando as colunas 'latitude' e 'longitude'
    #     8. Desenhar e plotar o mapa
                              
    #     Input: Dataframe
    #     Output: Mapa com clausterização         
    # """
    f = folium.Figure(width=1920, height=1080)

    m = folium.Map(max_bounds=True).add_to(f)

    marker_cluster = MarkerCluster().add_to(m)

    for _, line in df1.iterrows():

        name = line["restaurant_name"]
        price_for_two = line["average_cost_usd"]
        cuisine = line["cuisines"]
        rating = line["aggregate_rating"]
        color = f'{line["color_name"]}'

        html = "<p><strong>{}</strong></p>"
        html += "<p>Preço para dois: {} American dollar US$"
        html += "<br />Culinária: {}"
        html += "<br />Avaliação Média: {}/5.0"
        html = html.format(name, price_for_two, cuisine, rating, color)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["latitude"], line["longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to(marker_cluster)

    folium_static(m, width=1024, height=768)


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
df = pd.read_csv( '..\dataset\zomato.csv' )

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
st.title( '🏢' 'Fome Zero - Visão Geral' )

#image_path = 'pngwing.com.png'
image = Image.open( 'pngwing.com.png' )
st.sidebar.image( image, width=230 )

st.sidebar.markdown( '# Fome Zero Company' )
st.sidebar.markdown( '#### Restaurant Management Platform in Countries and Town' )
st.sidebar.markdown( """---""" )

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
    st.header( 'O melhor lugar para encontrar seu restaurante favorito!' )

    st.markdown('### Temos as seguintes marcas dentro da nossa plataforma:')
        
    col1, col2, col3, col4, col5 = st.columns( 5, gap='medium' )
    with col1:
        # Restaurantes cadastrados
        restaurants_unique = len( df1.loc[:, 'restaurant_id'].unique() )
        restaurants_unique = f'{restaurants_unique:,}'
        restaurants_unique = restaurants_unique.replace(",", ".")
        col1.metric( '### Restaurantes\nCadastrados', restaurants_unique )
            
    with col2:
        # Países Cadastrados
        paises_unique = len(df1.loc[:, 'country_name'].unique() )
        col2.metric( '### Países\nCadastrados', paises_unique )
            
    with col3:
        # Cidades Cadastradas
        cidades_unique = len(df1.loc[:, 'city'].unique() )
        col3.metric( '### Cidades\nCadastradas', cidades_unique )
            
    with col4:
        # Avaliações
        total_avaliacoes = df1.loc[:, 'votes'].sum()
        total_avaliacoes = f'{total_avaliacoes:,}'
        total_avaliacoes = total_avaliacoes.replace(",", ".")
        col4.metric('### Avaliações\nRealizadas', total_avaliacoes)
                    
    with col5:
        # Tipos de Culinária
        culinaria_unique = len(df1.loc[:, 'cuisines'].unique() )
        col5.metric( '### Tipos de\nCulinária', culinaria_unique )

    # Criar o mapa
    map_df1 = df1.loc[df1["country_name"].isin(countries), :]

    criar_map(map_df1)
