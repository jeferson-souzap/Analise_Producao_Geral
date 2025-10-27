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
#st.sidebar.page_link('pages/Simulador_Vendas.py', label='Simulador Vendas')

#FUNÇÕES


#VARIAVEIS GOBLAIS
df_vendas = Carregar_vendas()

#-------------------------------------------------------------------------------


# Configuração de janelas
tab01, tab02 = st.tabs([
    "Indicadores Venda",
    "Forecast - IA"
])

with tab01:
    # Header com filtros
    col_title, col_mes, col_ano = st.columns([3, 1, 1])

    with col_title:
        st.markdown("## Análise Geral de Vendas")

    with col_mes:
        #Material para teste do selectbox
        #mes = st.selectbox("Mês", ["Todos", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"], label_visibility="collapsed")
        anos_disponiveis = sorted(df_vendas['Data'].dt.year.unique(), reverse=True)
        ano_venda = st.selectbox('Escolha o ano:', anos_disponiveis, label_visibility="collapsed")

    with col_ano:
        #ano = st.selectbox("Ano", ["2024", "2023", "2022"], label_visibility="collapsed")
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



    # Dados de exemplo para os gráficos
    # Receita Mensal
    meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    receita_mensal = [45000000, 38000000, 42000000, 48000000, 43000000, 50000000,
                      52000000, 55000000, 58000000, 60000000, 63000000, 65000000]

    # Top 5 Clientes
    clientes_top5 = {
        'Cliente': ['Cliente 2', 'Cliente 13', 'Cliente 4', 'Cliente 14', 'Cliente 16'],
        'Receita': [16883354, 15456514, 14627368, 14095247, 13980792]
    }

    # Percentual por Categoria
    categorias = ['Acessórios', 'Periféricos', 'Mobile', 'Informática']
    percentuais = [39.94, 9.22, 26.1, 24.74]

    # Top Clientes por Receita
    top_clientes = {
        'Produto': ['Teclado', 'Notebook', 'Tablet', 'Headset', 'Mouse', 'Celular', 'Monitor', 'Impressora'],
        'Receita': [13009323, 12030996, 11794829, 11066709, 8312167, 8218292, 6413774, 6252610]
    }

    # Layout de gráficos
    col_left, col_right = st.columns([2, 1])

    with col_left:
        # Grafico atualizado para dados "REAIS"
        st.markdown("#### Receita Mensal")

        df_filtrado_receita = df_vendas[df_vendas['Data'].dt.year == ano_venda]
        meses_portugues = {
            1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
            7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
        }

        df_filtrado_receita['Mes_abreviado'] = df_filtrado_receita['Data'].dt.month.map(meses_portugues)
        df_receita_mensal = df_filtrado_receita.groupby('Mes_abreviado')['Valor_total'].sum().reset_index()

        fig_receita = go.Figure()
        fig_receita.add_trace(go.Scatter(
            x=df_receita_mensal['Mes_abreviado'],
            y=df_receita_mensal['Valor_total'],
            fill='tozeroy',
            fillcolor='rgba(45, 212, 191, 0.3)',
            line=dict(color='rgb(20, 184, 166)', width=2),
            mode='lines'

        ))

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

    with col_right:
        # Top Clientes por Receita
        st.markdown("#### Top Clientes por Receita")

        df_top_clientes = pd.DataFrame(top_clientes)

        fig_top_clientes = go.Figure()
        fig_top_clientes.add_trace(go.Bar(
            y=df_top_clientes['Produto'],
            x=df_top_clientes['Receita'],
            orientation='h',
            marker=dict(color='rgb(20, 184, 166)'),
            text=[f'R$ {v:,.0f}' for v in df_top_clientes['Receita']],
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

    # Segunda linha de gráficos
    col_left2, col_right2 = st.columns([1, 1])

    with col_left2:
        # Top 5 Clientes por Receita
        st.markdown("#### Top 5 Clientes por Receita")

        df_clientes = pd.DataFrame(clientes_top5)

        fig_clientes = go.Figure()
        fig_clientes.add_trace(go.Bar(
            x=df_clientes['Cliente'],
            y=df_clientes['Receita'],
            marker=dict(color='rgb(20, 184, 166)'),
            text=[f'R$ {v:,.0f}' for v in df_clientes['Receita']],
            textposition='outside',
            textfont=dict(size=10)
        ))

        fig_clientes.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            showlegend=False
        )

        st.plotly_chart(fig_clientes, use_container_width=True)

    with col_right2:
        # Gráfico de Rosca - Percentual por Categoria
        st.markdown("#### Percentual de Vendas por Categoria")

        fig_donut = go.Figure(data=[go.Pie(
            labels=categorias,
            values=percentuais,
            hole=0.5,
            marker=dict(colors=['#14b8a6', '#2dd4bf', '#5eead4', '#99f6e4']),
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(size=11)
        )])

        fig_donut.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )

        st.plotly_chart(fig_donut, use_container_width=True)