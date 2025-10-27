# Simulador Industrial em Python com Streamlit

## Descrição

Este projeto gera e visualiza **dados sintéticos de uma indústria fictícia**, cobrindo o fluxo completo do **Planejamento e Controle da Produção (PCP)** — desde **vendas e compras** até **produção, paradas e estoque**.

Os dados simulados são usados em **dashboards interativos no Streamlit**, com **uma página dedicada para cada indicador de produção**.
O objetivo é criar um **portfólio analítico profissional**, demonstrando como aplicar **Python e ciência de dados na indústria.**

---

### Indicadores simulados e visualizados

| Indicador                    | Fonte de dados       | Objetivo da análise                    |
| ---------------------------- | -------------------- | -------------------------------------- |
| **Vendas e Clientes**        | `dados_vendas.csv`   | Curva ABC, ticket médio, sazonalidade  |
| **Produção e Eficiência**    | `dados_producao.csv` | Acompanhamento planejado vs. produzido |
| **Paradas de Máquina**       | `dados_paradas.csv`  | Causas e impacto em horas de parada    |
| **Compras de Matéria-Prima** | `dados_compras.csv`  | Custos e volumes adquiridos            |
| **Estoque Diário**           | `dados_estoque.csv`  | Saldo, valor total e giro de estoque   |

Cada indicador será exibido em uma **página independente** dentro do aplicativo Streamlit, permitindo **navegação modular** e **comparações integradas**.

---

### Estrutura do projeto

``` bash
│   Home.py                  # Página principal do painel (dashboard inicial)
│   README.md                # Documentação do projeto
│   requirements.txt         # Lista de dependências necessárias
│
├───config
│       db_config.py         # Configuração de conexão e parâmetros do banco de dados
│
├───files
│       dados_compras.csv    # Dados simulados de compras
│       dados_estoque.csv    # Dados simulados de estoque
│       dados_paradas.csv    # Registro de paradas de produção
│       dados_producao.csv   # Dados simulados de produção
│       dados_vendas.csv     # Dados de vendas para análise
│       producao_simulada.csv# Base de simulação de produção
│
├───notebook
│   │   Analise.ipynb        # Notebook para análise exploratória e testes de indicadores   
│
├───pages
│       01_Dados_Simulados.py   # Página interativa para geração e visualização dos dados simulados
│       02_Indicadores_Venda.py # Página com dashboards e indicadores de vendas
│
└───utils
    │   config_home.py       # Configurações e funções específicas da página inicial
    │   config_vendas.py     # Funções auxiliares para o módulo de vendas
    │   simulador_dados.py   # Módulo de geração e manipulação de dados simulados

```

---

### Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/seu-usuario/simulador-industrial.git
cd simulador-industrial
pip install -r requirements.txt
```

**`requirements.txt` sugerido:**

``` bash
pandas
numpy
streamlit
plotly
```

---

### Como usar

1. **Gerar os dados simulados**

   ```bash
   python simulador_industrial.py
   ```

2. **Executar o dashboard**

   ```bash
   streamlit run app.py
   ```

3. **Explorar as páginas**

   * Cada página exibirá um **indicador de produção** com:

     * Gráficos interativos (Plotly);
     * Filtros por data, produto e máquina;
     * Análises automáticas (médias, tendências e top 10).

---

### Conceitos aplicados

* Simulação de dados industriais com distribuições estatísticas;
* Manipulação de DataFrames com **Pandas**;
* Visualização de séries temporais e Pareto com **Plotly**;
* Estrutura modular de páginas com **Streamlit**;
* Aplicação prática de **Python no PCP e manufatura**.

---

### Possíveis expansões

* [ ] Curva ABC automática de **produtos e clientes**
* [ ] Indicador de **OEE (Eficiência Global do Equipamento)**
* [ ] Painel de **KPIs financeiros** (custo, margem e faturamento)
* [ ] Integração com **MySQL ou SQLite**
* [ ] Exportação automática de relatórios em PDF

---

### Autor

**Jeferson de Souza**
Analista de PCP | Python | Data Analytics | SQL
Conectando operação industrial à análise de dados

Estudante de Física e Analista de PCP explorando o uso de Python e C++ em análise de dados, simulações científicas e otimização de processos industriais.

Este repositório reúne meus estudos e projetos voltados à ciência de dados aplicada à indústria, automação e visualização de indicadores de produção.
Sempre buscando unir teoria, prática e tecnologia para resolver problemas reais.
