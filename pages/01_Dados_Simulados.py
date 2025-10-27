import streamlit as st
import pandas as pd

from utils.simulador_dados import ARQ_PRODUCAO, ARQ_VENDAS, ARQ_COMPRAS, ARQ_PARADAS, ARQ_ESTOQUE


#Configuração da página
st.set_page_config('Dados Simulados', layout='wide')

st.markdown('## Configuração de simulação de dados')

DIAS = st.number_input('Informe a quantidade de dias para simulação:', min_value=30)
LOCAL_FILES = st.text_input('Informe onde deseja salvar os arquivos', placeholder='D:/local')
st.button('Gerar arquivos')

st.divider()

with st.expander('Dados de Venda', expanded=False):
    st.markdown('### Simulação de venda')
    #st.write(ARQ_PRODUCAO)
    df_vendas_simulada = pd.read_csv(ARQ_VENDAS)
    st.dataframe(df_vendas_simulada)


with st.expander('Dados de Compras', expanded=False):
    st.markdown('### Simulação de Compra de Materia-Prima')
    df_compras_simulada = pd.read_csv(ARQ_COMPRAS)
    st.dataframe(df_compras_simulada)



with st.expander('Dados de Apontamento', expanded=False):
    st.markdown('### Simulação de Apontamento')
    #st.write(ARQ_PRODUCAO)
    df_prod_simulada = pd.read_csv(ARQ_PRODUCAO)
    st.dataframe(df_prod_simulada)


with st.expander('Dados de parada de máquina', expanded=False):
    st.markdown('### Simulação de Paradas de Máquina')
    #st.write(ARQ_PRODUCAO)
    df_paradas_simulada = pd.read_csv(ARQ_PARADAS)
    st.dataframe(df_paradas_simulada)


with st.expander('Dados de Estoque', expanded=False):
    st.markdown('### Simulação de Saldo de Estoque')
    #st.write(ARQ_PRODUCAO)
    df_estoque_simulado = pd.read_csv(ARQ_ESTOQUE)
    st.dataframe(df_estoque_simulado)
