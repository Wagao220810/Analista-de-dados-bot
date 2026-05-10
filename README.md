# 🤖 Robô Analista de Dados

Um assistente interativo de linha de comando (CLI) escrito em Python, desenvolvido para automatizar tarefas rotineiras de Análise de Dados, gerar dashboards e obter insights avançados utilizando Inteligência Artificial.

## ✨ Funcionalidades Principais

- **Múltiplas Fontes de Dados**: Carregue arquivos locais (CSV, Excel, JSON), copie e cole direto da sua Área de Transferência (Clipboard), baixe dados via URL ou conecte-se a Bancos de Dados SQL (PostgreSQL, MySQL, SQL Server, SQLite).
- **Análise Exploratória Automática (EDA)**: Gere estatísticas descritivas, informações do dataset e identifique valores nulos em segundos.
- **Geração de Gráficos**: Criação automática de histogramas, heatmaps de correlação e gráficos de barras usando Matplotlib e Seaborn.
- **Detecção de Anomalias**: Identifica outliers automaticamente com base no método IQR (Intervalo Interquartil).
- **Integração com BI**: Exporte dados tratados para Power BI ou gere scripts Python mágicos de gráficos interativos com Plotly.
- **Dashboards Interativos em HTML**: Gere interfaces visuais ricas estilo Tableau/Power BI utilizando `PyGWalker`.
- **Inteligência Artificial (Google Gemini)**:
  - Gere insights descritivos textuais baseados em amostras de dados.
  - **Auto-Pilot**: Análise completa e autônoma do dataset gerando um relatório gerencial Markdown de ponta a ponta.

##  Pré-requisitos e Instalação

1. **Python 3.8+** instalado em sua máquina.
2. Clone o repositório e navegue até a pasta do projeto.
3. Instale as bibliotecas necessárias rodando o comando abaixo no terminal:

```bash
pip install pandas matplotlib seaborn openpyxl sqlalchemy pygwalker google-generativeai plotly
```

> **Nota sobre Banco de Dados:** Para usar a funcionalidade de conexão SQL com bancos específicos, instale o driver correspondente (ex: `psycopg2-binary` para PostgreSQL, `pymysql` para MySQL ou `pyodbc` para SQL Server). O SQLite tem suporte nativo.

## 🔑 Configurando a Chave de API da IA (Gemini)

Para utilizar as funcionalidades de Inteligência Artificial, você precisará de uma API Key gratuita do Google AI Studio.

Existem duas formas de fornecer a chave para o Robô:
1. **Recomendado:** Crie uma variável de ambiente no seu sistema operacional chamada `GEMINI_API_KEY` com o valor da sua chave.
2. **Manual:** Deixe em branco e o robô solicitará a chave diretamente no terminal na primeira vez que uma função de IA for acionada.

⚠️ **Atenção:** Evite salvar (hardcode) chaves de API diretamente no código-fonte, especialmente ao subir para um repositório público no GitHub!

## 🎮 Como Usar

Execute o script principal diretamente pelo terminal:

```bash
python robo_analista_dados.py
```

Um menu interativo será exibido:

```text
============================================================
🤖 ROBÔ ANALISTA DE DADOS
============================================================
1. 📂 Carregar dataset (Arquivo)
2. 📋 Carregar dataset (Área de Transferência)
3. 🔗 Carregar dataset (URL)
4. 🗄️ Carregar dataset (Banco de Dados SQL)
5. 📈 Estatísticas descritivas
6. ℹ️  Informações do dataset
...
14. 🚪 Sair
============================================================
Escolha (1-14):
```

Siga as instruções na tela e os arquivos gerados (gráficos, planilhas limpas, HTMLs e relatórios) serão automaticamente salvos e organizados em uma nova pasta `analise_YYYY-MM-DD_HHMMSS`.

## 🛠️ Tecnologias Utilizadas

- **Pandas** - Manipulação e análise de dados.
- **Matplotlib & Seaborn** - Visualização estática de dados.
- **PyGWalker** - Interface visual de dados exploratória (HTML).
- **Plotly** - Geração de visuais interativos em Python para Power BI.
- **SQLAlchemy** - Toolkit SQL e ORM.
- **Google Generative AI (Gemini)** - LLM para insights e relatórios gerenciais.

## 📄 Licença

Este projeto é de código aberto e está disponível sob a Licença MIT.