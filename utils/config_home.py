import pandas as pd
import streamlit as st
from utils.simulador_dados import ARQ_VENDAS


@st.cache_data #Não esquecer do cache 
def Carregar_vendas():
    df_vendas = pd.read_csv(ARQ_VENDAS)
    df_vendas['Data'] = pd.to_datetime(df_vendas['Data'], errors='coerce') #format='%Y-%m-%d')
    df_vendas['Quantidade_vendida'] = pd.to_numeric(df_vendas['Quantidade_vendida'], errors='coerce', dtype_backend='numpy_nullable')
    return df_vendas