import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# CONFIGURAÇÕES GERAIS E VARIÁVEIS GLOBAIS

np.random.seed(42)
random.seed(42)

# Diretório de saída
FILES_DIR = r'D:\#Mega\Jeferson - Dev\02 - Linguagens\Python\Analise_Producao_Geral\files'
os.makedirs(FILES_DIR, exist_ok=True)

# Variáveis globais para uso em outros módulos
ARQ_VENDAS = os.path.join(FILES_DIR, "dados_vendas.csv")
ARQ_COMPRAS = os.path.join(FILES_DIR, "dados_compras.csv")
ARQ_PRODUCAO = os.path.join(FILES_DIR, "dados_producao.csv")
ARQ_PARADAS = os.path.join(FILES_DIR, "dados_paradas.csv")
ARQ_ESTOQUE = os.path.join(FILES_DIR, "dados_estoque.csv")

# Dados básicos
PRODUTOS = ['Caneta Azul', 'Caneta Preta', 'Caneta Vermelha', 'Caneta Verde', 'Caneta Amarela']
MATERIAIS = ['Tinha', 'Tampas', 'Adesivo', 'Caixa', 'Etiqueta']
MAQUINAS = [f'MC-{i}' for i in range(1, 8)]

ANO_INICIO = 2022
DATA_INICIO = datetime(ANO_INICIO, 1, 1)
#DATA_HOJE = datetime.now()
#DATA_INICIO_datetime = datetime(DATA_INICIO.year, DATA_INICIO.month, DATA_INICIO.day)
#DIF_DATA = DATA_HOJE - DATA_INICIO
DIAS = 365*3

DATAS = [DATA_INICIO + timedelta(days=i) for i in range(DIAS)]

# Lista de clientes (com pesos para criar clientes “grandes” e “pequenos”)
CLIENTES = {
    "Cliente Alfa": 0.25,  # compra mais
    "Cliente Beta": 0.20,
    "Cliente Gama": 0.15,
    "Cliente Delta": 0.15,
    "Cliente Épsilon": 0.10,
    "Cliente Zeta": 0.10,
    "Cliente Ômega": 0.05
}


# ===============================================
# VENDAS (atualizada com cliente e valor)
def gerar_vendas():
    registros = []
    for data in DATAS:
        for produto in PRODUTOS:
            demanda_base = {'Caneta Azul': 100, 'Caneta Preta': 80, 'Caneta Vermelha': 60, 'Caneta Verde': 50, 'Caneta Amarela': 40}[produto]
            sazonal = np.sin((data.timetuple().tm_yday / 365) * 2 * np.pi) * 0.2
            vendas = max(int(np.random.normal(demanda_base * (1 + sazonal), 10)), 0)
            
            # Dividir as vendas do dia entre 1 a 4 clientes
            n_clientes = random.randint(1, 4)
            clientes_dia = random.choices(list(CLIENTES.keys()), weights=CLIENTES.values(), k=n_clientes)
            qtd_restante = vendas
            
            for cli in clientes_dia:
                # Distribui a quantidade proporcionalmente
                qtd_cli = max(int(np.random.normal(vendas / n_clientes, 5)), 1)
                qtd_cli = min(qtd_cli, qtd_restante)
                qtd_restante -= qtd_cli

                # Preço unitário variável por produto
                preco_base = {'Caneta Azul': 4.5, 'Caneta Preta': 3, 'Caneta Vermelha': 3.4, 'Caneta Verde': 2.8, 'Caneta Amarela': 1.5}[produto]
                preco_unit = round(np.random.uniform(preco_base * 0.9, preco_base * 1.1), 2)
                valor_total = round(qtd_cli * preco_unit, 2)

                registros.append([
                    data, produto, cli, qtd_cli, preco_unit, valor_total
                ])

                if qtd_restante <= 0:
                    break

    df = pd.DataFrame(registros, columns=[
        'Data', 'Produto', 'Cliente', 'Quantidade_vendida', 'Preco_unitario', 'Valor_total'
    ])
    
    return df


# ===============================================
# COMPRAS DE MATÉRIA-PRIMA
def gerar_compras():
    registros = []
    for data in DATAS:
        for material in MATERIAIS:
            qtd = max(int(np.random.normal(500,80)), 0)
            custo_unit = {'Tinha': 12, 'Tampas': 8, 'Adesivo': 15, 'Caixa': 6, 'Etiqueta': 10}[material]
            registros.append([data, material, qtd, custo_unit, qtd * custo_unit])
    return pd.DataFrame(registros, columns=['Data', 'Material', 'Quantidade', 'Custo_unitário', 'Custo_total'])


# ===============================================
# APONTAMENTO DE PRODUÇÃO (com máquinas)
def gerar_producao(vendas_df):
    registros = []
    for data in DATAS:
        maquinas_ativas = random.sample(MAQUINAS, k=random.randint(5, len(MAQUINAS)))
        for mc in maquinas_ativas:
            produto = random.choice(PRODUTOS)
            vendas_dia = int(vendas_df[(vendas_df['Data'] == data) & (vendas_df['Produto'] == produto)]['Quantidade_vendida'].sum())
            planejado = int(vendas_dia * np.random.uniform(1.05, 1.15))
            produzido = max(int(np.random.normal(planejado * np.random.uniform(0.9, 1.0), 5)), 0)
            horas = round(produzido / 50 * np.random.uniform(6, 10), 2)
            registros.append([data, mc, produto, planejado, produzido, horas])
    return pd.DataFrame(registros, columns=['Data', 'Maquina', 'Produto', 'Planejado', 'Produzido', 'Horas_maquina'])

# ===============================================
# PARADAS DE MÁQUINA
def gerar_paradas():
    registros = []
    motivos = ['Setup', 'Falta de material', 'Manutenção', 'Quebra', 'Ajuste de processo']
    for data in DATAS:
        for mc in MAQUINAS:
            if random.random() < 0.3:
                for _ in range(random.randint(1, 3)):
                    duracao = round(np.random.uniform(0.5, 3), 2)
                    registros.append([data, mc, random.choice(motivos), duracao])
    return pd.DataFrame(registros, columns=['Data', 'Maquina', 'Motivo', 'Horas_paradas'])

# ===============================================
# SALDO DE ESTOQUE
def gerar_estoque(vendas_df, producao_df):
    registros = []
    
    # Valor base médio por produto (simulado)
    preco_base = {'Caneta Azul': 25, 'Caneta Preta': 30, 'Caneta Vermelha': 20, 'Caneta Verde': 18, 'Caneta Amarela': 15}
    #PRODUTOS = ['Caneta Azul', 'Caneta Preta', 'Caneta Vermelha', 'Caneta Verde', 'Caneta Amarela']
    # Saldo inicial aleatório por produto
    saldo = {p: random.randint(200, 400) for p in PRODUTOS}
    
    for data in DATAS:
        for produto in PRODUTOS:
            vendido = int(vendas_df[
                (vendas_df['Data'] == data) & (vendas_df['Produto'] == produto)
            ]['Quantidade_vendida'].sum())
            
            produzido = producao_df[
                (producao_df['Data'] == data) & (producao_df['Produto'] == produto)
            ]['Produzido'].sum()
            
            # Atualiza o saldo diário
            saldo[produto] += produzido - vendido
            saldo_atual = max(saldo[produto], 0)
            
            # Valor unitário com pequena flutuação simulada
            preco_unit = round(np.random.uniform(preco_base[produto] * 0.9, preco_base[produto] * 1.1), 2)
            
            # Valor total em estoque
            valor_total = round(saldo_atual * preco_unit, 2)
            
            registros.append([data, produto, saldo_atual, preco_unit, valor_total])
    
    return pd.DataFrame(
        registros,
        columns=['Data', 'Produto', 'Saldo_estoque', 'Valor_unitario', 'Valor_total_estoque']
    )



# ===============================================
# EXECUÇÃO GERAL

if __name__ == "__main__":
    vendas = gerar_vendas()
    compras = gerar_compras()
    producao = gerar_producao(vendas)
    paradas = gerar_paradas()
    estoque = gerar_estoque(vendas, producao)

    vendas.to_csv(ARQ_VENDAS, index=False)
    compras.to_csv(ARQ_COMPRAS, index=False)
    producao.to_csv(ARQ_PRODUCAO, index=False)
    paradas.to_csv(ARQ_PARADAS, index=False)
    estoque.to_csv(ARQ_ESTOQUE, index=False)

    print(f"✅ Dados simulados gerados com sucesso na pasta '{FILES_DIR}'")