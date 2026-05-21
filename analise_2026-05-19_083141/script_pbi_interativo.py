# --- VISUAL PYTHON PARA POWER BI: DASHBOARD INTERATIVO SÊNIOR ---
# 1. Adicione um "Visual de script Python" no Power BI.
# 2. Arraste colunas (numéricas e categóricas) para a área de "Valores".
# 3. Cole este código abaixo e execute:

import plotly.express as px
import pandas as pd

# Fallback inteligente: se rodar fora do Power BI (ex: localmente no VS Code), gera dados de teste
try:
    dataset
except NameError:
    import numpy as np
    print("⚠️ Executando fora do Power BI! Gerando dados de demonstração...")
    dataset = pd.DataFrame({
        'Indicador X': np.random.randn(100), 'Indicador Y': np.random.randn(100),
        'Peso': np.random.rand(100) * 20, 'Categoria': np.random.choice(['Grupo A', 'Grupo B', 'Grupo C'], 100)
    })

# O Power BI agrupa os dados selecionados na variável 'dataset'
df_limpo = dataset.dropna()

num_cols = df_limpo.select_dtypes(include='number').columns.tolist()
cat_cols = df_limpo.select_dtypes(exclude='number').columns.tolist()

if len(num_cols) >= 2:
    fig = px.scatter(
        df_limpo, 
        x=num_cols[0], y=num_cols[1], 
        color=cat_cols[0] if len(cat_cols) > 0 else None,
        size=num_cols[2] if len(num_cols) > 2 else None,
        hover_data=df_limpo.columns.tolist(),
        title=f"Visão Sênior Interativa: {num_cols[0]} vs {num_cols[1]}",
        template="plotly_dark"
    )
    fig.show() # Renderiza interativamente no Power BI!
else:
    import matplotlib.pyplot as plt
    plt.text(0.5, 0.5, "Adicione ao menos 2 colunas numéricas", ha='center')
    plt.axis('off')
    plt.show()
