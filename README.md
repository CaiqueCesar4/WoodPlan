# WoodPlan

**WoodPlan** é um sistema de orçamentos desenvolvido para marcenarias, permitindo o gerenciamento completo de **módulos**, **mão de obra** e **orçamentos de produção**.

O projeto foi desenvolvido em **Python** com **Kivy** para a interface gráfica e **SQLite** como banco de dados local.

---

## Funcionalidades Principais

### Tela Inicial
- Acesso rápido às principais funções:
  - Criar novo orçamento
  - Gerenciar módulos
  - Gerenciar mão de obra
  - Consultar histórico de orçamentos

---

### Gerenciamento de Módulos
- Adicione, edite ou remova módulos.
- Cada módulo possui:
  - **Nome**
  - **Valor base (R$ / m²)**

---

### Gerenciamento de Mão de Obra
- Adicione e gerencie trabalhadores ou serviços.
- Cada registro possui:
  - **Nome do trabalhador**
  - **Custo diário (R$)**

---

### Criação de Orçamentos
- Monte orçamentos de forma simples:
  1. Adicione módulos informando **largura** e **altura** (em metros).  
     O sistema calcula automaticamente a área (m²) e o valor total do módulo.
  2. Adicione mão de obra informando a quantidade de dias de trabalho.
- Todos os valores são somados automaticamente.

---

### Histórico de Orçamentos
- Lista todos os orçamentos criados com:
  - Nome do orçamento
  - Data de criação
  - Valor total calculado

---

## Prévia do Sistema

> Abaixo, algumas telas do sistema em execução:

| Tela Inicial |
| ![Tela Inicial](PROJETOS/tela_inicial.png)
|--------------|

| Gerenciar Mão de Obra | Gerenciar Módulos |
|-----------------------|-------------------|
| ![Tela Inicial](PROJETOS/gerenciar_mao_de_obra.png) | ![Gerenciar Módulos](PROJETOS/gerenciar_modulos.png) |

| Orçamento - Módulos | Orçamento - Mão de Obra |
|---------------------|-------------------------|
| ![Orçamento Módulo](PROJETOS/orcamento_modulo.png) | ![Orçamento Mão de Obra](PROJETOS/orcamento_mao_de_obra.png) |

---

## Estrutura do Projeto

WoodPlan/app/
│
├── main.py # Arquivo principal do aplicativo
├── data.py # Gerenciamento do banco de dados SQLite
│
├── telas/
│ ├── tela_inicial.py # Tela inicial
│ ├── gerenciamento_modulos.py # Tela de gerenciamento de módulos
│ ├── gerenciamento_mao_de_obra.py # Tela de gerenciamento da mão de obra
│ ├── orcamento_modulo.py # Etapa 1 da criação do orçamento
│ ├── orcamento_mao_de_obra.py # Etapa 2 da criação do orçamento
│ └── historico_orcamentos.py # Tela de histórico de orçamentos
│
├── theme.kv # Arquivo de tema e estilo global
├── orcamento.db # Banco de dados SQLite
└── PROJETOS/ # Pasta para imagens de prévia

---

## Tecnologias Utilizadas
- **Python 3.10+**
- **Kivy** — Interface gráfica
- **SQLite** — Banco de dados local
- **dbdiagram.io** — Modelagem do banco

---

## Como Executar o Projeto

### Instale as dependências
pip install kivy

### Execute o aplicativo
python main.py
