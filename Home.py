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
5. 5. Alterado a coluna de código de país para o nome do país.
6. Criado uma coluna de categoria de tipo preço com base no range de valores.
7. Nos casos onde houve empate entre restaurantes, foi considerado o restaurante com registro mais antigo.
8. Categorizado, inicialmente, todos os restaurantes somente por um tipo de culinária.
      
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
    
- Visão Geral:
    - Visão Geral da plataforma com a Quantidade de restaurantes cadastrados, Quantidade de países cadastrados, Quantidade de cidades cadastradas, Quantidade de avaliações realizadas e tipos de culinárias;
    - Visão Geográfica:  Insights de geolocalização dos restaurantes.

- Visão por Países:
    - Principais métricas, Quantidade de restaurantes por país, Quantidade de cidades por país, Quantidade média de avaliações por país, Preço médio de prato para duas pessoas por país.
          
- Visão por Cidades:
    - Principais métricas, Top 10 cidades com mais restaurantes cadastrados, Top 7 cidades com mais restaurantes com avaliação acima de 4, Top 7 cidades com mais restaurantes com avaliação abaixo de 2.5, Top 10 cidade com mais restaurante com tipo de culinária única.
    
- Visão por Culinárias:
    -  Principais métricas, Melhores Restaurantes pelos principais tipos de culinária, Top 10 Restaurante com as melhores avaliações, Top 10 Culinária melhor avaliada e Top 10 Culinária pior avaliada.


##### Próximos passos:

- Realizar uma nova avaliação global dos dados para obter mais insights para o negócio;
- Reduzir o número de perguntas;
- Aumentar o número de gráficos com outras perpectivas de análises.

            
        Ask for help
        - Time de Data Science no Discord
            - wagnersobrinho    
    """)