import streamlit as st
import pandas as pd

from utils.config_home import Carregar_vendas


#Configuração de Pagina
#-----------------------------------------------------------
st.set_page_config('Ferramenta de Analise de produção', layout='wide')
#-----------------------------------------------------------

#Carregamento dos dados

df_vendas = Carregar_vendas()

with st.sidebar:
    st.title('Filtros')
    mes_venda = st.number_input('Escolha o mês:', value=1, min_value=1, max_value=12)
    ano_venda = st.number_input('Escolha o ano:', value=2024, min_value=1900)



df_filtrado = df_vendas[(df_vendas['Data'].dt.year == ano_venda) & (df_vendas['Data'].dt.month == mes_venda)]

col_m01, col_m02, col_m03 = st.columns(3, border=True)

with col_m01:
    valor_total_vendas = df_filtrado['Valor_total'].sum()
    
    #Formatando o valor 
    valor_formatado = f"R$ {valor_total_vendas:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    st.metric('Valor de vendas do Mês', value=valor_formatado, delta_color='off')

with col_m02:    
    qtd_total_vendas = df_filtrado['Quantidade_vendida'].sum()
    
    #Formatando o valor
    qtd_formatada = f"{qtd_total_vendas}".replace(",", "X").replace(".", ",").replace("X", ".")
    st.metric('Quantidade de vendas do Mês', value=qtd_formatada)



st.dataframe(df_filtrado)