import os
import sys

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    from pandas.io.clipboard import clipboard_set
except ImportError:
    pass

def gerar_graficos_basicos(df, output_dir):
    """Gera e salva gráficos estatísticos básicos."""
    print("\n📊 GERANDO GRÁFICOS...")
    plt.style.use('default')
    sns.set_palette("husl")
    
    # 1. Histograma Geral
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if not numeric_cols.empty:
        df[numeric_cols].hist(figsize=(12, 8))
        plt.tight_layout()
        filepath = os.path.join(output_dir, 'histograma_geral.png')
        plt.savefig(filepath)
        plt.show()
        print(f"✅ Histograma salvo em '{filepath}'")
        
    # 2. Heatmap de Correlação
    if len(numeric_cols) > 1:
        plt.figure(figsize=(10, 8))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', center=0)
        plt.title('Matriz de Correlação')
        plt.tight_layout()
        filepath = os.path.join(output_dir, 'correlacao_heatmap.png')
        plt.savefig(filepath)
        plt.show()
        print(f"✅ Heatmap de correlação salvo em '{filepath}'")
        
    # 3. Gráficos de Barras
    cat_cols = df.select_dtypes(include=['object', 'str']).columns
    for col in cat_cols[:5]:
        if df[col].nunique() < 20:
            plt.figure(figsize=(10, 6))
            df[col].value_counts().plot(kind='bar')
            plt.title(f'Distribuição - {col}')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            filepath = os.path.join(output_dir, f'barras_{col}.png')
            plt.savefig(filepath)
            plt.show()
            print(f"✅ Gráfico de barras para '{col}' salvo em '{filepath}'")

def gerar_scripts_powerbi(output_dir):
    """Gera scripts Python prontos para Visuais do Power BI."""
    print("\n🪄 GERADOR DE DASHBOARD INTERATIVO PARA POWER BI (Nível Sênior)")
    print("="*50)
    
    script_pbi = '''# --- VISUAL PYTHON PARA POWER BI: DASHBOARD INTERATIVO SÊNIOR ---
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
'''
    
    try:
        filepath = os.path.join(output_dir or '.', 'script_pbi_interativo.py')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(script_pbi)
        
        clipboard_set(script_pbi)
        
        print(f"✅ Script de Dashboard Interativo gerado em: '{filepath}'")
        print("✨ SCRIPT COPIADO AUTOMATICAMENTE PARA SUA ÁREA DE TRANSFERÊNCIA! ✨")
        return True
    except Exception as e:
        print(f"❌ Erro ao gerar scripts: {e}")
        return False

def gerar_dashboard_html(df, output_dir):
    """Gera um dashboard HTML interativo estilo Tableau/Power BI usando PyGWalker."""
    print("\n🚀 GERANDO DASHBOARD INTERATIVO (ESTILO POWER BI)")
    print("="*50)
    try:
        import pygwalker as pyg
        import webbrowser
        
        print("⏳ Construindo a interface visual de arrastar e soltar (isso pode levar alguns segundos)...")
        
        filepath = os.path.join(output_dir or '.', 'dashboard_powerbi_style.html')
        
        html_code = pyg.to_html(df)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_code)
        
        print(f"✅ Dashboard profissional gerado com sucesso!")
        print("🌐 Abrindo no seu navegador...")
        
        path_absoluto = os.path.abspath(filepath)
        webbrowser.open(f'file://{path_absoluto}')
    except ImportError:
        print("❌ ERRO: A biblioteca 'pygwalker' não está instalada.")
        print("   Rode no terminal: pip install pygwalker")
    except Exception as e:
        print(f"❌ Erro ao gerar dashboard: {e}")

if __name__ == "__main__":
    print("ℹ️ Este é um módulo auxiliar do Robô Analista de Dados (apenas definições de funções visuais).")
    print("   Para iniciar o programa, volte para a pasta principal e execute:")
    print("   python data_analyst_robot.py")