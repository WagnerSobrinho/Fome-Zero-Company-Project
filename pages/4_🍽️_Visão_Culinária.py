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


st.set_page_config( page_title='Visão Culinária', page_icon='🍽️', layout='wide')

# =====================================================================================================
# Funções
#======================================================================================================
def top_cuisines( df1 ):
    cuisines = {
        "Italian": "",
        "American": "",
        "Arabian": "",
        "Japanese": "",
        "Brazilian": "",
    }

    cols = [
        "restaurant_id",
        "restaurant_name",
        "country_name",
        "city",
        "cuisines",
        "average_cost_usd",
        "currency",
        "aggregate_rating",
        "votes",
    ]

    for key in cuisines.keys():

        lines = df1["cuisines"] == key

        cuisines[key] = (
            df1.loc[lines, cols]
            .sort_values(["aggregate_rating", "restaurant_id"], ascending=[False, True])
            .iloc[0, :]
            .to_dict()
        )

    return cuisines


def top_restaurants(countries, cuisines, top_n):
    
    cols = [
        "restaurant_id",
        "restaurant_name",
        "country_name",
        "city",
        "cuisines",
        "average_cost_usd",
        "aggregate_rating",
        "votes",
    ]

    linhas = (df1["cuisines"].isin(cuisines)) & (df1["country_name"].isin(countries))

    df_aux = df1.loc[linhas, cols].sort_values(
        ["aggregate_rating", "restaurant_id"], ascending=[False, True]
    )

    # Aplicar a formatação à coluna 'restaurant_id' usando a função apply
    df_aux['restaurant_id'] = df_aux['restaurant_id'].apply(format_restaurant_id)

    # Aplicar a formatação à coluna 'votes' usando a função apply
    df_aux['votes'] = df_aux['votes'].apply(format_votes_with_separator)

    
    return df_aux.head(top_n)



def top_10(df1, melhores=True):
    if melhores:
        df_aux = (df1.loc[:, ['aggregate_rating', 'cuisines']]
                   .groupby('cuisines')
                   .mean().reset_index()
                   .sort_values('aggregate_rating', ascending=False)).head(top_n)
    else:
        df_aux = (df1.loc[:, ['aggregate_rating', 'cuisines']]
                   .groupby('cuisines')
                   .mean().reset_index()
                   .sort_values('aggregate_rating', ascending=True)).head(top_n)

    df_aux['aggregate_rating'] = df_aux['aggregate_rating'].map('{:.2f}'.format)

    df_aux.columns = ['Culinária', 'Avaliação Média']

    # Desenhar gráfico de Barras
    fig = px.bar(df_aux, x='Culinária', y='Avaliação Média', text='Avaliação Média', color_discrete_sequence=['#636EFA'],
)
    fig.update_traces(textfont_size=12)

    # Personalize a fonte do eixo x
    fig.update_xaxes(tickfont=dict(size=12, family='Arial', color='white'), showgrid=False, title_font=dict(size=14, family='Arial', color='white'))

    # Personalize a fonte do eixo y
    fig.update_yaxes(tickfont=dict(size=12, family='Arial', color='white'), showgrid=False, showticklabels=False, title_font=dict(size=14, family='Arial', color='white'))

    return fig


def format_restaurant_id(restaurant_id):
        return '{:d}'.format(restaurant_id)

def format_votes_with_separator(x):
    return f"{x:,}".replace(",",".")


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

    # 4 . Exluir dados duplicados na coluna Restaurant ID.
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
df = pd.read_csv( 'dataset/zomato.csv' )

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
st.title( '🍽️' 'Fome Zero - Visão Culinária' )

#image_path = 'pngwing.com.png'
image = Image.open( 'pngwing.com.png' )
st.sidebar.image( image, width=230 )

st.sidebar.markdown( '# Fome Zero Company' )
st.sidebar.markdown( '#### Restaurant Management Platform in Countries and Town' )
st.sidebar.markdown( """---""" )

# Filtro país
countries = st.sidebar.multiselect( 
    'Escolha os países que deseja visualizar as informações',
    df1.loc[:, 'country_name'].unique(), 
    default=['Australia', 'Brazil', 'Canada', 'England', 'Qatar', 'South Africa', 'United States of America'] )

st.sidebar.markdown( """---""" )

# Filtro quantidade de restaurantes
top_n = st.sidebar.slider(
    'Selecione a quantidade de restaurantes que deseja visualizar', 1, 20, 10,
)



st.sidebar.markdown( """---""" )

# Filtro tipo culinária
cuisines = st.sidebar.multiselect( 
    'Escolha o tipo de Culinária',
    df1.loc[:, 'cuisines'].unique(),
    default=['Home-made', 'Italian', 'Brazilian', 'BBQ', 'Japanese', 'American', 'Arabian'] )


st.sidebar.markdown( """---""" )
st.sidebar.markdown( '### Powered by Wagner Sobrinho' )


# Filtro de país
linhas_selecionadas = df1['country_name'].isin( countries )
df1 = df1.loc[linhas_selecionadas, :]



# =======================================
# Layout no Streamlit
# =======================================

with st.container():
    st.markdown('## Melhores Restaurantes pelos principais tipos de culinária')
            
    cuisines = top_cuisines( df1 )
            
    italian, american, arabian, japanese, brazilian = st.columns( 5, gap='medium' )
        
    with italian:
        st.metric(
            label=f'Italiana: {cuisines["Italian"]["restaurant_name"]}',
            value=f'{cuisines["Italian"]["aggregate_rating"]}/5.0',
            help=f"""
            País: {cuisines["Italian"]["country_name"]}\n
            Cidade: {cuisines["Italian"]["city"]}\n
            Média Prato para dois: {cuisines["Italian"]["average_cost_usd"]} dolares
            """,
        )

    with american:
                st.metric(
                    label=f'Americana: {cuisines["American"]["restaurant_name"]}',
                    value=f'{cuisines["American"]["aggregate_rating"]}/5.0',
                    help=f"""
                    País: {cuisines["American"]['country_name']}\n
                    Cidade: {cuisines["American"]['city']}\n
                    Média Prato para dois: {cuisines["American"]['average_cost_usd']} dolares
                    """,
        )

    with arabian:
                st.metric(
                    label=f'Arabe: {cuisines["Arabian"]["restaurant_name"]}',
                    value=f'{cuisines["Arabian"]["aggregate_rating"]}/5.0',
                    help=f"""
                    País: {cuisines["Arabian"]['country_name']}\n
                    Cidade: {cuisines["Arabian"]['city']}\n
                    Média Prato para dois: {cuisines["Arabian"]['average_cost_usd']} dolares
                    """,
                )

    with japanese:
                st.metric(
                    label=f'Japonesa: {cuisines["Japanese"]["restaurant_name"]}',
                    value=f'{cuisines["Japanese"]["aggregate_rating"]}/5.0',
                    help=f"""
                    País: {cuisines["Japanese"]['country_name']}\n
                    Cidade: {cuisines["Japanese"]['city']}\n
                    Média Prato para dois: {cuisines["Japanese"]['average_cost_usd']} dolares
                    """,
        )
        
    with brazilian:
                st.metric(
                    label=f'Brasileira: {cuisines["Brazilian"]["restaurant_name"]}',
                    value=f'{cuisines["Brazilian"]["aggregate_rating"]}/5.0',
                    help=f"""
                    País: {cuisines["Brazilian"]['country_name']}\n
                    Cidade: {cuisines["Brazilian"]['city']}\n
                    Média Prato para dois: {cuisines["Brazilian"]['average_cost_usd']} dolares
                    """,
        )

with st.container():
    st.markdown("""---""")
    centered_header = f'<p style="font-size:36px">Top {str(top_n)} Restaurantes com Melhores avaliações</p>'
    st.markdown( centered_header, unsafe_allow_html=True)
    top10restaurant = top_restaurants(countries, cuisines, top_n)
    st.dataframe(top10restaurant, use_container_width=True)

with st.container():
    st.markdown("""---""")
    col1, col2 = st.columns( 2 )
        
    with col1:
        centered_markdown = f'<p style="font-size:16px; text-align:center">Top {str(top_n)} Melhores Tipos de Culinárias</p>'
        st.markdown(centered_markdown, unsafe_allow_html=True)
        melhores_fig = top_10(df1, melhores=True)
        st.plotly_chart(melhores_fig, use_container_width=True)       
            
    with col2:
        centered_markdown = f'<p style="font-size:16px; text-align:center">Top {str(top_n)} Piores Tipos de Culinárias</p>'
        st.markdown(centered_markdown, unsafe_allow_html=True)
        piores_fig = top_10(df1, melhores=False)
        st.plotly_chart(piores_fig, use_container_width=True)

