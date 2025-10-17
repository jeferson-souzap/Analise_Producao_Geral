import streamlit as st
import pandas as pd



"""
KPIs de Análise Temporal (Tendências)
Aqui você usa a coluna Data para entender o comportamento ao longo do tempo.

Faturamento por Período (Dia, Semana, Mês, Trimestre, Ano): Identifica sazonalidades e tendências.
Crescimento Mensal (MoM - Month over Month): Compara o faturamento de um mês com o anterior (% de crescimento).
Crescimento Anual (YoY - Year over Year): Compara o mesmo período em anos diferentes para eliminar o efeito da sazonalidade.
Acumulado do Ano (YTD - Year to Date): Faturamento total desde o início do ano até a data atual.

"""
