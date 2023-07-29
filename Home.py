import streamlit as st
from PIL import Image
from st_pages import Page, Section, show_pages, add_page_title
from st_pages import show_pages_from_config


st.set_page_config(
    page_title='Home',
    page_icon='🎲'
)

#image_path = 'pngwing.com.png'
image = Image.open( 'pngwing.com.png' )
st.sidebar.image( image, width=230 )

st.sidebar.markdown( '# Fome Zero Company' )
st.sidebar.markdown( '#### Restaurant Management Platform in Countries and Town' )
st.sidebar.markdown( """---""" )

st.sidebar.markdown( '### Powered by Wagner Sobrinho' )

st.write( '# Fome Zero Company - Dashboard' )

st.markdown(
    """
A empresa Fome Zero é uma marketplace de restaurantes, ou seja, seu core business é facilitar o encontro e                   negociações entre consumidores e restaurantes. Os restaurantes realizam o cadastro dentro da plataforma do Fome Zero,        que disponibiliza aos consumidores, informações como, localização, tipo de culinária, se possui sistema de reservas, se realiza entregas, avaliação do restaurante, dentre outras informações.
        
##### Premissas do Dashboard:
1. Os dados utilizados para criação deste Dashboard foram obtidos via plataforma Kaggle:
https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv
2. O Dashboard foi construido para acompanhar as métricas e ajudar na gestão da plataforma, além de ajudar em insights para alavancar o crescimento do negócio. Disponibilizado alguns KPI's iniciais ao dashboard, podendo ser agregado outros;
3. Os indicadores foram agrupados por algumas perspectivas de negócio:
	- Visão Geral;
	- Visão por Países;
	- Visão por Cidades;
	- Visão por Culinárias.
4. Para uma melhor análise, foi realizado a conversão dos valores do pratos de cada restaurante para dólar, utilizando o câmbio do dia 14/07/2023.
5. Durante a exploração dos dados, os poucos dados discrepantes foram substituídos pelo valor médio correspondente
6. Existem restaurantes não avaliados ou sem registro do valor do prato, esses restaurantes foram mantidos na base e podem ser eliminados dos gráficos através dos filtros na barra lateral;
7. Nos casos onde houve empate entre restaurantes, foi considerado o restaurante com registro mais antigo.
      
##### Como utilizar este Dashboard.
- Na barra lateral é possível realizar alguns filtros, como:
    - excluir ou incluir restaurantes sem avaliação;
    - excluir ou incluir restaurantes sem registro de custo médio do prato para duas pessoas;
    - escolher o conjunto de países de interesse;    
    - configurar o dashboard para limitar os gráficos aos mais relevantes, sendo possível configurar a quantidade a                ser exibida;
    - adicionar cores aos gráficos sinalizando o país;
    - utilizar o zoom para observar os restaurantes individualmente;
    - filtrar por país de interesse ou filtrar vários países.
      
Ao se escolher todos os restaurantes, o sistema pode apresentar um pouco de lentidão no processamento dos dados;
    
- Visão Geral
    - Visão Geral da Plataforma com os números dos Steakholders. Principais números referentes à plataforma de delivery;
    - Visão Geográfica:  Insights de geolocalização.
- Visão Empresa
    - Visão Gerencial:   Métricas gerais de comportamento.
    - Visão Tática:      Indicadores semanais de crescimento.   
- Visão Entregadores
    - Acompanhamento dos indicadores semanais de crescimento.
- Visão Restaurantes
    - Acompanhamento dos indicadores semanais de crescimento dos restaurantes.
- Visão Culinárias


##### Próximos passos:

- Realizar uma nova avaliação global dos dados para obter mais insights para o negócio.

            
        Ask for help
        - Time de Data Science no Discord
            - wagnersobrinho    
    """)