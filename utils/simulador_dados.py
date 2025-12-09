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

# Variáveis globais
ARQ_VENDAS = os.path.join(FILES_DIR, "dados_vendas.csv")
ARQ_COMPRAS = os.path.join(FILES_DIR, "dados_compras.csv")
ARQ_PRODUCAO = os.path.join(FILES_DIR, "dados_producao.csv")
ARQ_PARADAS = os.path.join(FILES_DIR, "dados_paradas.csv")
ARQ_ESTOQUE = os.path.join(FILES_DIR, "dados_estoque.csv")



# CONFIGURAÇÕES RANDOMIZADAS
# ===============================================

def gerar_configuracoes():
    # Produtos com cores e demandas base aleatórias
    cores = ['Azul', 'Preta', 'Vermelha', 'Verde', 'Amarela', 'Rosa', 'Roxa', 'Laranja', 'Marrom', 'Branca']
    num_produtos = random.randint(4, 8)
    PRODUTOS = [f'Caneta {cor}' for cor in random.sample(cores, num_produtos)]

    # Materiais com quantidades aleatórias
    materiais_base = ['Tinta', 'Tampas', 'Adesivo', 'Caixa', 'Etiqueta', 'Plástico', 'Mola', 'Embalagem', 'Clip']
    num_materiais = random.randint(4, 7)
    MATERIAIS = random.sample(materiais_base, num_materiais)

    # Máquinas com quantidade aleatória
    num_maquinas = random.randint(5, 10)
    MAQUINAS = [f'MC-{i}' for i in range(1, num_maquinas + 1)]

    # Período de dados aleatório
    ANOS_DADOS = 5 #random.randint(1, 6)
    ANO_INICIO = 2020 #random.randint(2020, 2025)
    DATA_INICIO = datetime(ANO_INICIO, 1, 1)
    DIAS = 365 * ANOS_DADOS

    DATAS = [DATA_INICIO + timedelta(days=i) for i in range(DIAS)]

    # Clientes com pesos aleatórios
    nomes_clientes = ['Alfa', 'Beta', 'Gama', 'Delta', 'Épsilon', 'Zeta', 'Ômega', 'Sigma', 'Tau', 'Phi', 'Lambda',
                      'Kappa']
    num_clientes = random.randint(5, 10)
    clientes_selecionados = random.sample(nomes_clientes, num_clientes)

    # Gerar pesos aleatórios e normalizar
    pesos = [round(random.uniform(0.05, 0.3), 2) for _ in range(num_clientes)]
    soma_pesos = sum(pesos)
    pesos_normalizados = [round(p / soma_pesos, 2) for p in pesos]

    CLIENTES = {f"Cliente {nome}": peso for nome, peso in zip(clientes_selecionados, pesos_normalizados)}


    # Preços base aleatórios para produtos
    PRECOS_BASE_VENDA = {produto: round(random.uniform(5.0, 25.0), 2) for produto in PRODUTOS}

    # Demandas base aleatórias
    DEMANDAS_BASE = {produto: random.randint(30, 120) for produto in PRODUTOS}

    # Custos base aleatórios para materiais
    CUSTOS_BASE_MATERIAIS = {material: round(random.uniform(1, 10), 2) for material in MATERIAIS}

    # Valores base aleatórios para estoque
    VALORES_BASE_ESTOQUE = {produto: round(random.uniform(10, 35), 2) for produto in PRODUTOS}

    return {
        'PRODUTOS': PRODUTOS,
        'MATERIAIS': MATERIAIS,
        'MAQUINAS': MAQUINAS,
        'DATAS': DATAS,
        'CLIENTES': CLIENTES,
        'PRECOS_BASE_VENDA': PRECOS_BASE_VENDA,
        'DEMANDAS_BASE': DEMANDAS_BASE,
        'CUSTOS_BASE_MATERIAIS': CUSTOS_BASE_MATERIAIS,
        'VALORES_BASE_ESTOQUE': VALORES_BASE_ESTOQUE,
        'DIAS': DIAS
    }


# Gerar configurações uma vez
CONFIG = gerar_configuracoes()

# Atribuir às variáveis globais
PRODUTOS = CONFIG['PRODUTOS']
MATERIAIS = CONFIG['MATERIAIS']
MAQUINAS = CONFIG['MAQUINAS']
DATAS = CONFIG['DATAS']
CLIENTES = CONFIG['CLIENTES']
PRECOS_BASE_VENDA = CONFIG['PRECOS_BASE_VENDA']
DEMANDAS_BASE = CONFIG['DEMANDAS_BASE']
CUSTOS_BASE_MATERIAIS = CONFIG['CUSTOS_BASE_MATERIAIS']
VALORES_BASE_ESTOQUE = CONFIG['VALORES_BASE_ESTOQUE']
DIAS = CONFIG['DIAS']


# ===============================================
# VENDAS (atualizada com cliente e valor)
def gerar_vendas():
    registros = []
    for data in DATAS:
        for produto in PRODUTOS:
            demanda_base = DEMANDAS_BASE[produto]
            # Sazonalidade baseada no dia do ano
            sazonal = np.sin((data.timetuple().tm_yday / 365) * 2 * np.pi) * random.uniform(0.1, 0.3)
            # Variação aleatória adicional
            variacao_extra = random.uniform(0.8, 1.2)
            vendas = max(int(np.random.normal(demanda_base * (1 + sazonal) * variacao_extra, 15)), 0)

            # Dividir as vendas do dia entre 1 a 4 clientes
            n_clientes = random.randint(1, min(4, len(CLIENTES)))
            clientes_dia = random.choices(list(CLIENTES.keys()), weights=CLIENTES.values(), k=n_clientes)
            qtd_restante = vendas

            for cli in clientes_dia:
                # Distribui a quantidade proporcionalmente
                qtd_cli = max(int(np.random.normal(vendas / n_clientes, 8)), 1)
                qtd_cli = min(qtd_cli, qtd_restante)
                qtd_restante -= qtd_cli

                # Preço unitário variável por produto
                preco_base = PRECOS_BASE_VENDA[produto]
                preco_unit = round(np.random.uniform(preco_base * 0.85, preco_base * 1.15), 2)
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
    # Frequência aleatória de compras (nem todo material é comprado todo dia)
    frequencia_compra = {material: random.uniform(0.3, 0.8) for material in MATERIAIS}

    for data in DATAS:
        for material in MATERIAIS:
            if random.random() < frequencia_compra[material]:
                qtd_base = random.randint(200, 800)
                qtd = max(int(np.random.normal(qtd_base, 100)), 0)
                custo_unit_base = CUSTOS_BASE_MATERIAIS[material]
                custo_unit = round(np.random.uniform(custo_unit_base * 0.9, custo_unit_base * 1.1), 2)
                registros.append([data, material, qtd, custo_unit, round(qtd * custo_unit, 2)])

    return pd.DataFrame(registros, columns=['Data', 'Material', 'Quantidade', 'Custo_unitário', 'Custo_total'])


# ===============================================
# APONTAMENTO DE PRODUÇÃO (com máquinas)
def gerar_producao(vendas_df):
    registros = []

    # Eficiência base aleatória por máquina
    eficiencia_maquinas = {maquina: random.uniform(0.85, 1.1) for maquina in MAQUINAS}

    for data in DATAS:
        # Número aleatório de máquinas ativas
        maquinas_ativas = random.sample(MAQUINAS, k=random.randint(3, len(MAQUINAS)))

        for mc in maquinas_ativas:
            produto = random.choice(PRODUTOS)
            vendas_dia = int(
                vendas_df[(vendas_df['Data'] == data) & (vendas_df['Produto'] == produto)]['Quantidade_vendida'].sum())

            # Fator de planejamento aleatório
            fator_planejamento = random.uniform(1.05, 1.2)
            planejado = int(vendas_dia * fator_planejamento)

            # Produção considerando eficiência da máquina
            fator_eficiencia = eficiencia_maquinas[mc]
            produzido = max(int(np.random.normal(planejado * fator_eficiencia, 10)), 0)

            # Horas de operação baseadas na produção
            horas_base = produzido / random.uniform(40, 60)
            horas = round(horas_base * random.uniform(0.8, 1.2), 2)

            registros.append([data, mc, produto, planejado, produzido, horas])

    return pd.DataFrame(registros, columns=['Data', 'Maquina', 'Produto', 'Planejado', 'Produzido', 'Horas_maquina'])


# ===============================================
# PARADAS DE MÁQUINA
def gerar_paradas():
    registros = []
    motivos = ['Setup', 'Falta de material', 'Manutenção', 'Quebra', 'Ajuste de processo', 'Troca de ferramenta',
               'Limpeza', 'Falta de energia']

    # Probabilidade de parada por máquina (algumas quebram mais que outras)
    prob_parada_maquinas = {maquina: random.uniform(0.2, 0.5) for maquina in MAQUINAS}

    for data in DATAS:
        for mc in MAQUINAS:
            if random.random() < prob_parada_maquinas[mc]:
                num_paradas = random.randint(1, 3)
                for _ in range(num_paradas):
                    duracao = round(np.random.uniform(0.3, 4), 2)
                    motivo = random.choice(motivos)
                    registros.append([data, mc, motivo, duracao])

    return pd.DataFrame(registros, columns=['Data', 'Maquina', 'Motivo', 'Horas_paradas'])


# ===============================================
# SALDO DE ESTOQUE
def gerar_estoque(vendas_df, producao_df):
    registros = []

    # Saldo inicial aleatório por produto
    saldo = {p: random.randint(100, 500) for p in PRODUTOS}

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

            # Valor unitário com flutuação
            valor_base = VALORES_BASE_ESTOQUE[produto]
            preco_unit = round(np.random.uniform(valor_base * 0.85, valor_base * 1.15), 2)

            # Valor total em estoque
            valor_total = round(saldo_atual * preco_unit, 2)

            registros.append([data, produto, saldo_atual, preco_unit, valor_total])

    return pd.DataFrame(
        registros,
        columns=['Data', 'Produto', 'Saldo_estoque', 'Valor_unitario', 'Valor_total_estoque']
    )


# ===============================================
# FUNÇÃO PARA MOSTRAR CONFIGURAÇÕES
def mostrar_configuracoes():
    """Exibe as configurações geradas randomicamente"""
    print("═" * 60)
    print("CONFIGURAÇÕES GERADAS RANDOMICAMENTE")
    print("═" * 60)
    print(f"Produtos ({len(PRODUTOS)}): {', '.join(PRODUTOS)}")
    print(f"Materiais ({len(MATERIAIS)}): {', '.join(MATERIAIS)}")
    print(f"Máquinas ({len(MAQUINAS)}): {', '.join(MAQUINAS)}")
    print(f"Período: {DATAS[0].strftime('%d/%m/%Y')} a {DATAS[-1].strftime('%d/%m/%Y')} ({DIAS} dias)")
    print(f"Clientes ({len(CLIENTES)}):")
    for cliente, peso in CLIENTES.items():
        print(f"   - {cliente}: {peso:.2f}")
    print("═" * 60)


# ===============================================
# EXECUÇÃO GERAL

if __name__ == "__main__":
    # Mostrar configurações
    mostrar_configuracoes()

    # Gerar dados
    print("Gerando dados de vendas...")
    vendas = gerar_vendas()

    print("Gerando dados de compras...")
    compras = gerar_compras()

    print("Gerando dados de produção...")
    producao = gerar_producao(vendas)

    print("Gerando dados de paradas...")
    paradas = gerar_paradas()

    print("Gerando dados de estoque...")
    estoque = gerar_estoque(vendas, producao)

    # Salvar arquivos
    vendas.to_csv(ARQ_VENDAS, index=False)
    compras.to_csv(ARQ_COMPRAS, index=False)
    producao.to_csv(ARQ_PRODUCAO, index=False)
    paradas.to_csv(ARQ_PARADAS, index=False)
    estoque.to_csv(ARQ_ESTOQUE, index=False)

    print(f" Dados simulados gerados com sucesso na pasta '{FILES_DIR}'")

    # Estatísticas básicas
    print("\n ESTATÍSTICAS DOS DADOS GERADOS:")
    print(f"   - Vendas: {len(vendas):,} registros")
    print(f"   - Compras: {len(compras):,} registros")
    print(f"   - Produção: {len(producao):,} registros")
    print(f"   - Paradas: {len(paradas):,} registros")
    print(f"   - Estoque: {len(estoque):,} registros")
    print(f"   - Valor total vendas: R$ {vendas['Valor_total'].sum():,.2f}")