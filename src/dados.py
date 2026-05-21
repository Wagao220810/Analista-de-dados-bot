import os
import io
from datetime import datetime

try:
    import pandas as pd
    import numpy as np
    from pandas.io.clipboard import clipboard_get
except ImportError:
    pass

def carregar_arquivo():
    """Carrega arquivo de dados CSV, Excel ou JSON."""
    arquivo = input("\n📂 Digite o caminho do arquivo (CSV/Excel/JSON): ").strip(' "\'')
    
    if not os.path.exists(arquivo):
        print("❌ Arquivo não encontrado!")
        return None
    
    try:
        extensao = os.path.splitext(arquivo)[1].lower()
        readers = {
            '.xlsx': pd.read_excel, '.xls': pd.read_excel, '.json': pd.read_json
        }
        return readers.get(extensao, pd.read_csv)(arquivo)
    except Exception as e:
        print(f"❌ Erro ao carregar: {e}")
        return None

def carregar_area_transferencia():
    """Carrega dados diretamente da área de transferência (clipboard)."""
    print("\n📋 Tentando carregar dados da área de transferência...")
    try:
        return pd.read_clipboard()
    except Exception:
        print("⚠️ Formato tabular padrão falhou. Analisando o conteúdo copiado...")
        try:
            texto_limpo = clipboard_get().strip()
            
            if texto_limpo.startswith(('{', '[')):
                print("🔍 Formato JSON detectado na área de transferência!")
                return pd.read_json(io.StringIO(texto_limpo))
                
            sep = input("🔍 Digite o separador usado (ex: ',', ';', '|' ou deixe em branco para abortar): ")
            return pd.read_clipboard(sep=sep) if sep else None
        except Exception as e2:
            print("❌ Erro definitivo ao carregar da área de transferência.")
            print(f"   Dica: Certifique-se de ter copiado dados estruturados válidos. Detalhe: {e2}")
            return None

def carregar_url():
    """Carrega dados diretamente de uma URL."""
    url_input = input("\n🔗 Digite a URL do arquivo (CSV/Excel/JSON): ")
    url = url_input.strip(' "\'')
    
    if not url.startswith(('http://', 'https://')):
        print("❌ URL inválida! Certifique-se de que ela comece com http:// ou https://")
        return None
        
    print(f"⏳ Baixando dados de: {url} ...")
    try:
        if '.json' in url.lower():
            return pd.read_json(url)
        elif '.xls' in url.lower():
            return pd.read_excel(url)
        else:
            return pd.read_csv(url)
    except Exception as e:
        print(f"❌ Erro ao carregar da URL: {e}")
        print("   Dica: Verifique se o link é público e aponta diretamente para o arquivo bruto (raw).")
        return None

def carregar_banco_dados():
    """Carrega dados diretamente de um banco de dados SQL."""
    print("\n🗄️ CONEXÃO COM BANCO DE DADOS")
    print("Suporta: SQLite, PostgreSQL, MySQL, SQL Server, Oracle, etc.")
    
    try:
        from sqlalchemy import create_engine
    except ImportError:
        print("❌ ERRO: A biblioteca 'SQLAlchemy' não está instalada.")
        print("   Rode no terminal: pip install sqlalchemy")
        return None

    string_conexao = input("\n🔗 Digite a string de conexão (Ex: sqlite:///dados.db): ").strip(' "\'')
    if not string_conexao: return None
        
    query = input("📝 Digite a Query SQL para extrair os dados (Ex: SELECT * FROM clientes): ").strip()
    if not query: return None

    print("⏳ Conectando e executando query...")
    try:
        return pd.read_sql(query, create_engine(string_conexao))
    except Exception as e:
        print(f"❌ Erro ao conectar ou consultar o banco: {e}")
        return None

def exportar_dados(df, output_dir):
    """Exporta os dados carregados para um arquivo CSV ou Excel."""
    print(f"\n💾 EXPORTAR DADOS (PREPARAÇÃO PARA POWER BI)\n{'='*50}")
    opcao = input("Escolha o formato:\n1. Excel (.xlsx)\n2. CSV (.csv)\nOpção (1-2): ").strip()
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    caminho_base = os.path.join(output_dir or '.', f'dados_tratados_{timestamp}')
    
    try:
        if opcao == '1':
            df.to_excel(f"{caminho_base}.xlsx", index=False)
            print(f"✅ Excel exportado: '{caminho_base}.xlsx'\n💡 Dica Power BI: Vá em 'Obter Dados' -> 'Pasta de Trabalho do Excel'!")
        elif opcao == '2':
            df.to_csv(f"{caminho_base}.csv", index=False, sep=';')
            print(f"✅ CSV exportado: '{caminho_base}.csv'\n💡 Dica Power BI: Vá em 'Obter Dados' -> 'Texto/CSV'!")
        else:
            print("❌ Opção inválida!")
            return False
        return True
    except Exception as e:
        print(f"❌ Erro ao exportar dados: {e}")
        return False

def detectar_anomalias(df):
    """Identifica outliers matemáticos no DataFrame usando o método de Tukey (IQR)."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    anomalias_resumo = {}
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        limite_inf = Q1 - 1.5 * IQR
        limite_sup = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < limite_inf) | (df[col] > limite_sup)][col]
        
        if not outliers.empty:
            anomalias_resumo[col] = {
                "quantidade": len(outliers),
                "limites_normais": f"[{limite_inf:.2f}, {limite_sup:.2f}]",
                "amostra_valores": outliers.tolist()[:10] # Envia no max 10 valores 
            }
            
    return anomalias_resumo

if __name__ == "__main__":
    print("ℹ️ Este é um módulo auxiliar do Robô Analista de Dados (apenas definições de funções).")
    print("   Para iniciar o programa, volte para a pasta principal e execute:")
    print("   python data_analyst_robot.py")