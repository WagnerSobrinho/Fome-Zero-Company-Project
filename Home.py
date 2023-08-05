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
# Problema de Negócio

A empresa Fome Zero é uma marketplace de restaurantes, ou seja, seu core business é facilitar o encontro e negociações entre consumidores e restaurantes. Os restaurantes realizam o cadastro dentro da plataforma do Fome Zero, que disponibiliza aos consumidores, informações como, localização, tipo de culinária, se possuem sistema de reservas, se realizam entregas, avaliação dos restaurantes, quantidade de avaliações realizadas, dentre outras informações.


## O Desafio

Acabei de ser contratado como Cientista de Dados da empresa Fome Zero e a minha principal tarefa nesse momento foi ajudar o CEO Kleiton Guerra a identificar pontos chaves da empresa, respondendo às perguntas que ele fez utilizando dados!

O CEO Guerra também foi recém-contratado e precisa entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a Fome Zero, e para isso, ele precisa que seja feita uma análise nos dados da empresa e que sejam gerados dashboards, a partir dessas análises, responder às seguintes perguntas:

## 1. Visão Geral

1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?

## 2. Visão País

1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?
9. Qual o nome do país que possui, na média, a maior nota média registrada?
10. Qual o nome do país que possui, na média, a menor nota média registrada?
11. Qual a média de preço de um prato para dois por país?


## 3. Visão Cidades

1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?


## 4. Visão Restaurantes

1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de um prato para duas pessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?
6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?
7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?


## 5. Visão Culinária

1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação?
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação?
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?
12. Qual o tipo de culinária que possui a maior nota média?
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?

O CEO também pediu que fosse gerado dashboards que permitisse que ele visualizasse as principais informações das perguntas que ele fez. O CEO precisa dessas informações o mais rápido possível, uma vez que ele também é novo na empresa e irá utilizá-las para entender melhor a empresa Fome Zero para conseguir tomar decisões mais assertivas.

O meu trabalho foi utilizar os dados que a empresa Fome Zero possuia e responder as perguntas feitas do CEO e criar os dashboards solicitados.

        
## Premissas do Dashboard:
1. Os dados utilizados para criação deste Dashboard foram obtidos via plataforma Kaggle:
https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv
2. O Dashboard foi construido para acompanhar as métricas e ajudar na gestão da plataforma, além de ajudar em insights para alavancar o crescimento do negócio. Disponibilizado alguns KPI's iniciais ao dashboard, podendo ser agregado outros;
3. Os indicadores foram agrupados por algumas perspectivas de negócio:
	- Visão Geral:
      - Visão Geral da plataforma com os Quantidade de restaurantes cadastrados, Quantidade de países cadastrados, Quantidade de cidades cadastradas, Quantidade de avaliações realizadas e tipos de culinárias;
      - Visão Geográfica:  Insights de geolocalização dos restaurantes.

	- Visão por Países:
      - Principais métricas, Quantidade de restaurantes por país, Quantidade de cidades por país, Quantidade média de avaliações por país, Preço médio de prato para duas pessoas por país.
          
	- Visão por Cidades:
       - Principais métricas, Top 10 cidades com mais restaurantes cadastrados, Top 7 cidades com mais restaurantes com avaliação acima de 4, Top 7 cidades com mais restaurantes com avaliação abaixo de 2.5, Top 10 cidade com mais restaurante com tipo de culinária única.
    
	- Visão por Culinárias:
      -  Principais métricas, Melhores Restaurantes pelos principais tipos de culinária, Top 10 Restaurante com as melhores avaliações, Top 10 Culinária melhor avaliada e Top 10 Culinária pior avaliada.

4. Para uma melhor análise, foi realizado a conversão dos valores do pratos de cada restaurante para dólar, utilizando o câmbio do dia 14/07/2023.
5. Alterado a coluna de código de país para o nome do país.
6. Criado uma coluna de categoria de tipo preço com base no range de valores.
7. Nos casos onde houve empate entre restaurantes, foi considerado o restaurante com registro mais antigo.
8. Categorizado, inicialmente, todos os restaurantes somente por um tipo de culinária.
      
## Como utilizar este Dashboard.
- Na barra lateral é possível realizar alguns filtros, como:
    - excluir ou incluir restaurantes sem avaliação;
    - excluir ou incluir restaurantes sem registro de custo médio do prato para duas pessoas;
    - escolher o conjunto de países de interesse;    
    - configurar o dashboard para limitar os gráficos aos mais relevantes, sendo possível configurar a quantidade a                ser exibida;
    - adicionar cores aos gráficos sinalizando o país;
    - utilizar o zoom para observar os restaurantes individualmente;
    - filtrar por país de interesse ou filtrar vários países.
      
Ao se escolher todos os restaurantes, o sistema pode apresentar um pouco de lentidão no processamento dos dados;

## Alguns Insights de dados.
Quantidade de restaurantes, países, cidades, avaliações realizadas e culinária cadastrados na Base.
Quantidade de restaurantes cadastrados por país
Quantidade de cidades cadastradas por país
Quantidade Média de Avaliações por país
Preço Médio do prato para duas pessoas por país
Top 10 cidades com mais restaurantes cadastrados 
Top 7 cidades com mais restaurantes com média de avaliação acima de 4
Top 7 cidades com mais restaurantes com média de avaliação abaixo de 2.5
Melhores Restaurantes pelos principais tipos de culinária
Top 10 Restaurantes com Melhores avaliações
Top 10 Culinária Melhor Avaliada
Top 10 Culinária Pior Avaliada


## O produto final do Projeto.
Painel online, hospedado em Cloud e disponível para acesso em qualquer dispositivo conectado à internet.
O painel pode ser acessado atráves desse link: [https://wagnersobrinho-project-fome-zero-company.streamlit.app/] (https://wagnersobrinho-project-fome-zero-company.streamlit.app/)

## Conclusão.
O objetivo deste projeto é criar um conjunto de gráficos e / ou tabelas que exibam essas métricas da melhor forma possível para o CEO entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a empresa.

## Próximos passos:

- Realizar uma nova avaliação global dos dados para obter mais insights para o negócio;
- Reduzir o número de perguntas;
- Aumentar o número de gráficos com outras perpectivas de análises.

            
Ask for help
- Time de Data Science no Discord
  - wagnersobrinho    
""")
