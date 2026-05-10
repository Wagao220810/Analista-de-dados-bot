# 🤖 Robô Analista de Dados

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas)
![Gemini AI](https://img.shields.io/badge/Google_Gemini-AI_Analysis-8E75B2?style=for-the-badge&logo=google)
![Power BI](https://img.shields.io/badge/Power_BI-Integration-F2C811?style=for-the-badge&logo=powerbi)

> Um assistente de linha de comando (CLI) automatizado para análise de dados, visualização interativa e geração de insights com Inteligência Artificial (Google Gemini).

---

## 📌 Sobre o Projeto

O **Robô Analista de Dados** é uma ferramenta completa desenhada para acelerar o processo de Análise Exploratória de Dados (EDA). Ele permite carregar arquivos de múltiplas fontes, gerar estatísticas detalhadas, criar gráficos automáticos, detectar anomalias e emitir relatórios executivos escritos inteiramente por IA.

Ideal para Cientistas de Dados, Analistas de BI e profissionais que desejam automatizar tarefas repetitivas e focar na extração de valor.

---

## ✨ Funcionalidades (Features)

- **Carregamento Multi-Fonte:** Suporta CSV, Excel, JSON, Área de Transferência, URLs Diretas e Bancos de Dados SQL.
- **Análise Exploratória Rápida:** Geração de estatísticas descritivas e contagem de valores nulos com 1 clique.
- **Visualização de Dados:** Geração automática de Histogramas, Heatmaps de Correlação e Gráficos de Barras.
- **Integração com Power BI:** Exportação de dados limpos e geração de scripts Python em Plotly para visuais 100% interativos no Power BI.
- **Dashboard HTML:** Criação de interface drag-and-drop (arrastar e soltar) estilo Tableau usando `PyGWalker`.
- **Inteligência Artificial (Gemini):**
  - 🔍 **Detecção de Anomalias:** Identifica outliers e usa a IA para explicar possíveis causas no mundo real.
  - 🧠 **Insights Executivos:** Gera um resumo dos 3 principais indicadores de negócio baseados na amostra.
  - 🚀 **Auto-Pilot:** Analisa todo o dataset e redige um relatório técnico avançado em formato Markdown.

---

## 📸 Galeria (Screenshots)

*Adicione aqui as capturas de tela para demonstrar o projeto em ação!*

### 1. Menu Principal no Terminal
![Menu Principal do Robô](docs/menu.png)

### 2. Dashboard Interativo (PyGWalker)
![Dashboard HTML Interativo](docs/dashboard.png)

### 3. Relatórios Gerados pelo Gemini
![Auto-Pilot Relatório Markdown](docs/relatorio.png)

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter o Python instalado na sua máquina. Você também precisará de uma chave de API do Google AI Studio para as funções do Gemini.

### Instalação

1. Clone este repositório:
```bash
git clone https://github.com/Wagao220810/robo-analista-dados.git
cd robo-analista-dados
```

2. Instale as dependências necessárias:
```bash
pip install pandas matplotlib seaborn numpy openpyxl google-generativeai pygwalker sqlalchemy
```

3. Execute o robô:
```bash
python robo_analista_dados.py
```

---

## 🏗️ Arquitetura e Clean Code

Este projeto foi desenvolvido utilizando boas práticas de engenharia de software:
- **Tabela de Despacho (Dispatch Dictionary):** Substituição de cadeias complexas de `if/else` por um dicionário de ações para o menu, tornando o código modular e fácil de expandir (OCP - Open/Closed Principle).
- **Decorators Customizados:** Criação do decorator `@dados_carregados_required` para validação de estado, evitando redundância de código antes de executar análises.
- **Tratamento de Exceções (Fail-Fast):** Captura robusta de erros ao importar bibliotecas, ler arquivos de formatos desconhecidos ou falhas na API do Gemini.

---

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Se você tem alguma ideia para melhorar o robô, sinta-se à vontade para abrir uma *Issue* ou enviar um *Pull Request*.

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/NovaFuncionalidade`)
3. Faça o Commit de suas mudanças (`git commit -m 'Adicionando nova funcionalidade'`)
4. Faça o Push para a Branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---

<div align="center">
  Feito com ☕ e 🐍 por Wagner
</div>