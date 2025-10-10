# Simulador Industrial em Python com Streamlit

**Simulação e visualização de indicadores industriais**
---

### Descrição

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

```
simulador_industrial/
│
├── files/                     # Dados CSV simulados
│   ├── dados_vendas.csv
│   ├── dados_compras.csv
│   ├── dados_producao.csv
│   ├── dados_paradas.csv
│   └── dados_estoque.csv
│
├── pages/                     # Páginas individuais do Streamlit
│   ├── 1_Vendas_e_Clientes.py
│   ├── 2_Producao_e_Eficiencia.py
│   ├── 3_Paradas_de_Maquina.py
│   ├── 4_Compras_e_Materiais.py
│   └── 5_Estoque_e_Financeiro.py
│
├── simulador_industrial.py    # Script principal de geração dos dados
└── README.md
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

```
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
Analista de PCP com experiência em planejamento e controle da produção.
Estudante de Física e entusiasta por simulações e aplicações de **Python na indústria e ciência de dados**.
