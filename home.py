import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from IPython.core.pylabtools import figsize

#Carregando procedimento que carrega os dados do CSV
from utils.config_home import Carregar_vendas
from utils.Config_geral import formatar_brl

#Configuração de Pagina
#-----------------------------------------------------------
st.set_page_config('Ferramenta de Analise de produção', layout='wide')
#-----------------------------------------------------------

#Carregamento dos dados
#-----------------------------------------------------------
df_vendas = Carregar_vendas()


#Configuração de data
#-----------------------------------------------------------
dt_inicio = df_vendas['Data'].min()
dt_final = df_vendas['Data'].max()

dat_inicio = dt_inicio.date()
dat_final = dt_final.date()



# Menu lateral
with st.sidebar:
    st.title('Filtros')
    #mes_venda = st.number_input('Escolha o mês:', value=1, min_value=1, max_value=12)
    #ano_venda = st.number_input('Escolha o ano:', value=2024, min_value=1900)
    #st.write(f'Data Minima = {dat_inicio}')
    #st.write(f'Data Máximo = {dat_final}')

    anos_disponiveis = sorted(df_vendas['Data'].dt.year.unique(), reverse=True)
    ano_venda = st.selectbox('Escolha o ano:', anos_disponiveis)

    meses_disponiveis = sorted(df_vendas['Data'].dt.month.unique(), reverse=False)
    mes_venda = st.selectbox('Escolha o ano:', meses_disponiveis)

    #barra fica ruim de filtrar
    #mes_venda = st.slider('Escolha o mês:', min_value=1, max_value=12, value=datetime.now().month)

    st.divider()

    #Mostras as datas simuladas para teste
    dt_inicio = df_vendas['Data'].min().strftime('%d/%m/%Y')
    dt_final = df_vendas['Data'].max().strftime('%d/%m/%Y')
    st.info(f"Período total dos dados:\n\nDe **{dt_inicio}** a **{dt_final}**")



with st.expander('VENDAS', expanded=True):
    df_filtrado = df_vendas[(df_vendas['Data'].dt.year == ano_venda) & (df_vendas['Data'].dt.month == mes_venda)]

    with st.container(border=True):
        col_m01, col_m02, col_m03 = st.columns(3)

        #Valor Total de Venda filtrado
        with col_m01:
            valor_total_vendas = df_filtrado['Valor_total'].sum()
            st.metric(
                'Faturamento Total',
                value=formatar_brl(valor_total_vendas)
            )

        #Tick médio
        with col_m02:
            ticket_medio_global = df_filtrado['Valor_total'].mean()
            st.metric(
                'Ticket Médio Global',
                value=formatar_brl(ticket_medio_global)
            )

        with col_m03:
            qtd_vendas = df_filtrado.shape[0]
            st.metric('Quantidade de Vendas', value=qtd_vendas)


    #Falta fazer top cliente e o top produto
    #vale a pena criar um grafico simples com o top 5 clientes e produtos
    #Top 5 clientes
    st.subheader("Análise de Performance")
    col_g01, col_g02 = st.columns(2)

    with col_g01:
        st.markdown("##### Top 5 Clientes")
        top_clientes = df_filtrado.groupby('Cliente')['Valor_total'].sum().nlargest(5).sort_values(ascending=True)
        st.bar_chart(top_clientes, color='#1f77b4', horizontal=True)

    with col_g02:
        st.markdown("##### Top 5 Produtos")
        top_produtos = df_filtrado.groupby('Produto')['Valor_total'].sum().nlargest(5).sort_values(ascending=True)
        st.bar_chart(top_produtos, color='#ff7f0e', horizontal=True)



with st.expander('Visualizar dados detalhados do período'):
    st.dataframe(df_filtrado, use_container_width=True)

    #Não precisa disso os dados estão na pasta files
    st.download_button(
        label="Baixar dados como CSV",
        data=df_filtrado.to_csv(index=False).encode('utf-8'),
        file_name=f'vendas_{mes_venda}_{ano_venda}.csv',
        mime='text/csv',
    )