import streamlit as st
import pandas as pd
import os
from pathlib import Path

import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

#CHAMADA DE FUNÇÃO AUXLIAR
from utils.config_vendas import Carregar_vendas
from utils.Config_geral import formatar_brl

#CONFIGURAÇÃO DA PAGINA
st.set_page_config('Indicadores de Vendas', layout="wide", initial_sidebar_state="collapsed")

#FUNÇÕES

#VARIAVEIS GOBLAIS
df_vendas = Carregar_vendas()

#-------------------------------------------------------------------------------


# Configuração de janelas
tab01, tab02, tab03 = st.tabs([
    "Indicadores Venda",
    "Forecast - IA",
    "S&OP"
])


with tab01:
    # Header com filtros
    col_title, col_mes, col_ano = st.columns([3, 1, 1])

    with col_title:
        st.markdown("## Análise Geral de Vendas")

    with col_mes:
        anos_disponiveis = sorted(df_vendas['Data'].dt.year.unique(), reverse=True)
        ano_venda = st.selectbox('Escolha o ano:', anos_disponiveis, label_visibility="collapsed")

    with col_ano:
        meses_disponiveis = sorted(df_vendas['Data'].dt.month.unique(), reverse=False)
        mes_venda = st.selectbox('Escolha o ano:', meses_disponiveis, label_visibility="collapsed")
    st.markdown("---")

    with st.container(border=True):
        df_filtrado = df_vendas[(df_vendas['Data'].dt.year == ano_venda) & (df_vendas['Data'].dt.month == mes_venda)]

        colm01, colm02, colm03 = st.columns(3, vertical_alignment="center")
        with colm01:
            valor_total_vendas=df_filtrado['Valor_total'].sum()
            st.metric(
                'Faturamento Total',
                value=formatar_brl(valor_total_vendas)
            )

        with colm02:
            qtd_vendas = df_filtrado.shape[0]
            st.metric('Quantidade de Vendas', value=qtd_vendas)

        with colm03:
            ticket_medio_global = df_filtrado['Valor_total'].mean()
            st.metric(
                'Ticket Médio Global',
                value=formatar_brl(ticket_medio_global)
            )


    st.markdown("<br>", unsafe_allow_html=True)


    # Receita Mensal  - Grafico atualizado para dados "REAIS"
    with st.container():

        st.markdown(f"#### Receita Mensal ano {ano_venda}")

        df_filtrado_receita = df_vendas[df_vendas['Data'].dt.year == ano_venda]
        meses_portugues = {
            1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
            7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
        }

        df_filtrado_receita['Mes_abreviado'] = df_filtrado_receita['Data'].dt.month.map(meses_portugues)
        df_receita_mensal = df_filtrado_receita.groupby('Mes_abreviado')['Valor_total'].sum().reset_index()

        #testando a biblioteca go / grafico mais bonitinho
        fig_receita = go.Figure()
        fig_receita.add_trace(go.Scatter(
            x=df_receita_mensal['Mes_abreviado'],
            y=df_receita_mensal['Valor_total'],
            fill='tozeroy',
            fillcolor='rgba(45, 212, 191, 0.3)',
            line=dict(color='rgb(20, 184, 166)', width=2)
            # mode='lines'

        ))

        #estudar melhor cada argumento do grafico
        fig_receita.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)'),
            hovermode='x unified'
        )

        st.plotly_chart(fig_receita, use_container_width=True)


#------------------------------------------------------------------------------


    col_left, col_right = st.columns([2, 2])

    # Top 5 Clientes por Receita com dados "REAIS"
    with col_left:
        st.markdown(f"#### Top 5 Clientes por valor {ano_venda}")


        df_top5_clientes = df_vendas.groupby('Cliente')['Valor_total'].sum().reset_index()
        df_top5_clientes = df_top5_clientes.sort_values('Valor_total', ascending=False)

        fig_clientes = go.Figure()
        fig_clientes.add_trace(go.Bar(
            x=df_top5_clientes['Cliente'],
            y=df_top5_clientes['Valor_total'],
            marker=dict(color='rgb(20, 184, 166)'),
            text=[f'R$ {v:,.0f}' for v in df_top5_clientes['Valor_total']],
            textposition='outside',
            textfont=dict(size=10)
        ))

        fig_clientes.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            showlegend=False
        )

        st.plotly_chart(fig_clientes, use_container_width=True)

    # Top Clientes por Receita - Gráfico atualizado para dados "REAIS"
    with col_right:
        st.markdown(f"#### Top Produtos ano {ano_venda}")

        df_top_produtos = df_filtrado.groupby('Produto')['Valor_total'].sum().reset_index()
        df_top_produtos = df_top_produtos.sort_values('Valor_total', ascending=True)

        fig_top_clientes = go.Figure()
        fig_top_clientes.add_trace(go.Bar(
            y=df_top_produtos['Produto'],
            x=df_top_produtos['Valor_total'],
            orientation='h',
            marker=dict(color='rgb(20, 184, 166)'),
            text=[f'R$ {v:,.0f}' for v in df_top_produtos['Valor_total']],
            textposition='outside',
            textfont=dict(size=10)
        ))

        fig_top_clientes.update_layout(
            height=300,
            margin=dict(l=20, r=80, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False),
            showlegend=False
        )

        st.plotly_chart(fig_top_clientes, use_container_width=True)

    # Grafico Faturamento mensal
    #Será que da para colocar linha de tendência?
    with st.container():
        st.subheader(f"Vendas por dia do mês 0{mes_venda}")

        df_vendas_mes = df_filtrado.groupby('Data')['Valor_total'].sum().reset_index()

        #st.dataframe(df_vendas_mes)

        fig_vendas_mes = go.Figure()
        fig_vendas_mes.add_trace(go.Bar(
            x=df_vendas_mes['Data'],
            y=df_vendas_mes['Valor_total'],
            marker=dict(color='rgb(20, 184, 166)'),
            text=[f'R$ {v:,.0f}' for v in df_vendas_mes['Valor_total']],
            textposition='outside',
            textfont=dict(size=10)
        ))

        fig_vendas_mes.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            showlegend=False
        )

        st.plotly_chart(fig_vendas_mes, use_container_width=True)










#Previsão de venda baseado em estatística
with tab02:
    st.subheader('Local onde a mágica acontece')
    with st.container(border=True):
        col_tab01, col_tab02 = st.columns(2)
        with col_tab01:
            mes_previsao = st.number_input('Mes de previsão')
            ano_previsao = st.number_input('Ano de previsão')

        with col_tab02:
            periodo_meses = st.number_input('Periodo Meses')
            periodo_anos = st.number_input('Periodo Anos')

        st.button('Gerar')



    with st.container(border=True):
        pass


# Página de S&OP
with tab03:
    st.subheader('Local onde a mágica é confrontada')