import sys
import os
from functools import wraps
from datetime import datetime
import threading
import time
import itertools

# --- HABILITA CORES ANSI NO TERMINAL ---
if os.name == 'nt':
    os.system('') # "Liga" o processamento de cores no Windows

class Cor:
    AZUL = '\033[94m'
    CYAN = '\033[96m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    MAGENTA = '\033[95m'
    NEGRITO = '\033[1m'
    RESET = '\033[0m'

# --- CONFIGURAÇÃO PARA O PYINSTALLER (.exe) ---
# 1. Garante que o .exe encontre a pasta 'src' na memória temporária
if getattr(sys, 'frozen', False):
    sys.path.insert(0, sys._MEIPASS)
else:
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Globais que serão carregadas preguiçosamente (Lazy Loading)
pd = None
ia = None
visualizacao = None
dados = None

def dados_carregados_required(func):
    """Decorator para verificar se o DataFrame foi carregado antes de executar uma função."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.df is None:
            print(f"\n{Cor.VERMELHO}❌ ERRO: Nenhum dado foi carregado. Use a opção '1' para carregar.{Cor.RESET}")
            return
        return func(self, *args, **kwargs)
    return wrapper


class RoboAnalistaDados:
    def __init__(self):
        self.df = None
        self.output_dir = None
        print(f"{Cor.VERDE}{Cor.NEGRITO}🤖 Robô Analista de dados INICIADO!{Cor.RESET}")
        print(f"{Cor.AMARELO}📊 Suporta CSV, Excel (.xlsx) e JSON{Cor.RESET}")
        
        # Estrutura unificada de Menu (Descrição, Função)
        self.opcoes_menu = {
            '1': ("📂 Carregar dataset (Arquivo)", self.carregar_dados),
            '2': ("📋 Carregar dataset (Área de Transferência)", self.carregar_area_transferencia),
            '3': ("🔗 Carregar dataset (URL)", self.carregar_url),
            '4': ("🗄️ Carregar dataset (Banco de Dados SQL)", self.carregar_banco_dados),
            '5': ("📈 Estatísticas descritivas", self.estatisticas_descritivas),
            '6': ("ℹ️  Informações do dataset", self.info_dados),
            '7': ("📊 Gerar gráficos", self.graficos),
            '8': ("🔍 Detectar anomalias", self.detectar_anomalias),
            '9': ("💾 Exportar dados (Para BI)", self.exportar_dados),
            '10': ("🪄  Gerar Scripts Visuais Power BI", self.gerar_scripts_powerbi),
            '11': ("🚀 Gerar Dashboard HTML (Estilo Power BI)", self.gerar_dashboard_html),
            '12': (f"{Cor.MAGENTA}🧠 Gerar Insights com IA (Gemini){Cor.RESET}{Cor.CYAN}", self.obter_insights_ia),
            '13': ("🤖 Analisar Tudo Automaticamente com IA (Auto-Pilot)", self.analise_automatizada_ia),
            '14': (f"{Cor.VERDE}📊 Gerar Relatório Executivo Corporativo{Cor.RESET}{Cor.CYAN}", self.gerar_relatorio_executivo),
            '15': ("🧹 Limpeza de Dados Caóticos com IA (ETL Inteligente)", self.limpar_dados_caoticos_ia),
            '16': (f"{Cor.AMARELO}🇧🇷 Traduzir Dados para Português (IA){Cor.RESET}{Cor.CYAN}", self.traduzir_dados_ptbr)
        }

    def _criar_diretorio_saida(self):
        """Cria um diretório de saída único para os resultados da análise."""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        self.output_dir = f"analise_{timestamp}"
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"📂 Os resultados serão salvos em: '{self.output_dir}'")

    def _abrir_pasta_saida(self):
        """Abre a pasta de saída no explorador de arquivos automaticamente (Windows, Mac, Linux)."""
        if not self.output_dir:
            return
        try:
            if sys.platform == 'win32': os.startfile(self.output_dir)
            else: 
                import subprocess
                cmd = 'open' if sys.platform == 'darwin' else 'xdg-open'
                subprocess.Popen([cmd, self.output_dir])
        except Exception:
            pass

    def _garantir_dependencias(self):
        """Aplica Lazy Loading: Carrega os pacotes pesados apenas na hora de usar."""
        global pd, ia, visualizacao, dados
        if pd is not None:
            return
        
        print("⏳ Inicializando motores de Análise e IA (isso ocorre apenas na 1ª vez)...")
        try:
            import pandas as pd
            from dotenv import load_dotenv
            load_dotenv()  # Carrega variáveis de ambiente
            
            if not os.getenv("GEMINI_API_KEY"):
                print("\n⚠️ AVISO: 'GEMINI_API_KEY' não encontrada. Verifique o arquivo .env.")
            
            from src import ia, visualizacao, dados
        except ImportError as e:
            print(f"\n{Cor.VERMELHO}❌ ERRO: Dependências ausentes! Detalhe: {e}")
            if getattr(sys, 'frozen', False):
                print(f"   Dica: Adicione --hidden-import {getattr(e, 'name', 'modulo')} no pyinstaller.{Cor.RESET}")
            else:
                print(f"   pip install pandas matplotlib seaborn openpyxl python-dotenv google-generativeai{Cor.RESET}")
            input(f"\n{Cor.CYAN}Pressione Enter para sair...{Cor.RESET}")
            sys.exit(1)

    def _processar_novo_df(self, novo_df, mensagem_sucesso="✅ Dados carregados!"):
        """Processa e exibe o novo DataFrame carregado."""
        if novo_df is not None:
            self.df = novo_df
            self._criar_diretorio_saida()
            print(f"{Cor.VERDE}{mensagem_sucesso} {self.df.shape[0]} linhas, {self.df.shape[1]} colunas{Cor.RESET}")
            print(f"\n{Cor.CYAN}📋 Primeiras 5 linhas:{Cor.RESET}")
            print(self.df.head())
            return True
        return False

    def _exibir_cabecalho(self, titulo):
        """Gera um cabeçalho padronizado e reduz a repetição de prints."""
        print(f"\n{titulo}\n{'='*50}")

    def carregar_dados(self):
        return self._processar_novo_df(dados.carregar_arquivo(), "✅ Dados carregados!")

    def carregar_area_transferencia(self):
        return self._processar_novo_df(dados.carregar_area_transferencia(), "✅ Dados carregados da área de transferência!")

    def carregar_url(self):
        return self._processar_novo_df(dados.carregar_url(), "✅ Dados carregados com sucesso da URL!")
    
    def carregar_banco_dados(self):
        return self._processar_novo_df(dados.carregar_banco_dados(), "✅ Dados carregados com sucesso do banco!")

    @dados_carregados_required
    def estatisticas_descritivas(self):
        self._exibir_cabecalho("📈 ESTATÍSTICAS DESCRITIVAS")
        print(self.df.describe())
    
    @dados_carregados_required
    def info_dados(self):
        self._exibir_cabecalho("ℹ️  INFORMAÇÕES DO DATASET")
        self.df.info()
        print(f"\nValores ausentes:\n{self.df.isnull().sum()}")
    
    @dados_carregados_required
    def graficos(self):
        visualizacao.gerar_graficos_basicos(self.df, self.output_dir)

    @dados_carregados_required
    def detectar_anomalias(self):
        self._exibir_cabecalho("🔍 DETECÇÃO DE ANOMALIAS (Outliers)")
        anomalias = dados.detectar_anomalias(self.df)
        
        if not anomalias:
            print("✅ Nenhuma anomalia (outlier) detectada nas colunas numéricas.")
            return
            
        for col, info in anomalias.items():
            print(f"\n{col}:\n  Limites: {info['limites_normais']}\n  Encontrados: {info['quantidade']}\n  Amostra: {info['amostra_valores']}")
                
        if input("\n🤖 Deseja que a IA analise essas anomalias? (s/n): ").strip().lower() in ['s', 'sim', 'y']:
            ia.explicar_anomalias(anomalias)

    @dados_carregados_required
    def exportar_dados(self):
        if dados.exportar_dados(self.df, self.output_dir): self._abrir_pasta_saida()

    @dados_carregados_required
    def gerar_scripts_powerbi(self):
        if visualizacao.gerar_scripts_powerbi(self.output_dir):
            print("\n💡 DICA SÊNIOR PARA O POWER BI:\n   0. Instale: pip install plotly\n   1. No Power BI, clique em 'Py' (Visual de script Python).\n   2. Arraste colunas, cole o script e pronto!")
            self._abrir_pasta_saida()

    @dados_carregados_required
    def gerar_dashboard_html(self):
        visualizacao.gerar_dashboard_html(self.df, self.output_dir)

    @dados_carregados_required
    def obter_insights_ia(self):
        self._exibir_cabecalho("🧠 GERANDO INSIGHTS COM INTELIGÊNCIA ARTIFICIAL (GEMINI)")
        ia.obter_insights(self.df, self.output_dir)

    @dados_carregados_required
    def analise_automatizada_ia(self):
        self._exibir_cabecalho("🚀 INICIANDO AUTO-PILOT: ANÁLISE COMPLETA COM IA...")
        if ia.analise_automatizada(self.df, self.output_dir): self._abrir_pasta_saida()

    @dados_carregados_required
    def gerar_relatorio_executivo(self):
        self._exibir_cabecalho("📊 GERANDO RELATÓRIO EXECUTIVO PROFISSIONAL PARA O CLIENTE...")
        print("⏳ Processando estatísticas... (Isso pode levar alguns segundos)")
        try:
            import sweetviz as sv
            report_path = os.path.join(self.output_dir, "Relatorio_Executivo_Cliente.html")
            sv.analyze(self.df).show_html(filepath=report_path, open_browser=False, layout='widescreen', scale=1.0)
            
            print("🌍 Traduzindo layout e aprimorando o visual do relatório...")
            try:
                with open(report_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                traducoes = {
                    "Associations": "Correlações", "Summary": "Resumo", "Missing": "Dados Ausentes",
                    "Distinct": "Valores Únicos", "Numerical": "Numérico", "Categorical": "Categórico",
                    "Text": "Texto", "Values": "Valores", "Zeroes": "Zeros", "Maximum": "Máximo",
                    "Minimum": "Mínimo", "Average": "Média", "Rows": "Linhas", "Duplicates": "Duplicadas",
                    "RAM": "Uso de Memória", "Feature": "Variável", "Features": "Variáveis", "Dataframe": "Conjunto de Dados",
                    "MAX": "MÁX", "MIN": "MÍN", "AVG": "MÉDIA", "Median": "Mediana",
                    "Quantiles": "Quantis", "Standard deviation": "Desvio Padrão", 
                    "Variance": "Variância", "Range": "Amplitude", "Kurtosis": "Curtose", 
                    "Skewness": "Assimetria", "Sum": "Soma", "Type": "Tipo", 
                    "Outliers": "Anomalias (Outliers)", "Most Frequent": "Mais Frequentes",
                    "Smallest": "Menores", "Largest": "Maiores"
                }
                
                for eng, ptbr in traducoes.items():
                    html_content = html_content.replace(f">{eng}<", f">{ptbr}<")
                    html_content = html_content.replace(f">{eng.upper()}<", f">{ptbr.upper()}<")
                
                # --- APLICAR TEMA ESCURO (DARK MODE) VIA CSS ---
                css_dark_mode = "<style>html { filter: invert(1) hue-rotate(180deg); background-color: #111; }</style></head>"
                html_content = html_content.replace("</head>", css_dark_mode)
                
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            except Exception as e:
                print(f"⚠️ Aviso: Falha na tradução: {e}")
            
            print(f"\n✅ Relatório gerado! Arquivo pronto em:\n   -> {report_path}")
            
            self._abrir_pasta_saida()
            
        except ImportError:
            print("\n❌ ERRO: Instale a biblioteca necessária: pip install sweetviz")

    @dados_carregados_required
    def limpar_dados_caoticos_ia(self):
        self._exibir_cabecalho("🧹 ETL INTELIGENTE: LIMPANDO DADOS CAÓTICOS COM IA")
        
        coluna = input("Digite o nome da coluna de texto que está bagunçada: ").strip()
        if coluna not in self.df.columns:
            print(f"❌ Coluna '{coluna}' não encontrada.")
            return
            
        print(f"\n⏳ Enviando amostras de '{coluna}' para a IA estruturar via JSON...\n")
        
        print("⏳ Aguardando processamento da Inteligência Artificial... (Isso pode levar alguns minutos)")
        self.df = ia.estruturar_coluna_caotica(self.df, coluna)
        print("✅ Dados estruturados! Use as opções '5' ou '6' para visualizar.")

    @dados_carregados_required
    def traduzir_dados_ptbr(self):
        self._exibir_cabecalho("🇧🇷 TRADUZINDO DADOS PARA PORTUGUÊS (IA)")
        print("⏳ Iniciando tradução do conjunto de dados... (Isso pode levar alguns minutos)")
        
        try:
            import json
            import google.generativeai as genai
            
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                print("❌ ERRO: Chave API do Gemini não encontrada. Verifique o arquivo .env.")
                return
                
            genai.configure(api_key=api_key)
            
            # Busca dinamicamente um modelo de geração de texto disponível para sua chave
            nome_modelo = "gemini-1.5-flash" # Fallback padrão
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        if 'flash' in m.name or 'pro' in m.name:
                            nome_modelo = m.name.replace('models/', '') # Remove o prefixo para evitar duplicidade na chamada
                            if 'flash' in nome_modelo:  # Dá preferência ao flash por ser mais rápido para traduções
                                break
            except Exception as e:
                print(f"⚠️ Aviso ao buscar modelos: {e}")
            
            print(f"🤖 Modelo IA selecionado: {nome_modelo}")
            model = genai.GenerativeModel(nome_modelo)
            
            # 1. Traduzir nomes das colunas
            print("🔄 Traduzindo nomes das colunas...")
            colunas_originais = list(self.df.columns)
            prompt_colunas = (
                "Você é um tradutor de dados especialista em Ciência de Dados. "
                "Traduza os seguintes nomes de colunas para o Português do Brasil (PT-BR). "
                "Retorne APENAS um objeto JSON válido, sem formatação markdown, "
                "onde a chave é o nome original e o valor é a tradução.\n"
                f"Nomes originais: {colunas_originais}"
            )
            
            response = model.generate_content(prompt_colunas)
            texto_json = response.text.replace("```json", "").replace("```", "").strip()
            
            try:
                mapa_colunas = json.loads(texto_json)
                self.df.rename(columns=mapa_colunas, inplace=True)
                print("✅ Colunas traduzidas com sucesso!")
            except json.JSONDecodeError:
                print(f"⚠️ Aviso: A IA não retornou um JSON válido para as colunas. Resposta bruta:\n{texto_json}")

            # 2. Traduzir dados categóricos e textos
            colunas_texto = self.df.select_dtypes(include=['object', 'string']).columns
            if not colunas_texto.empty:
                print("🔄 Traduzindo valores de texto (limite de 50 valores únicos por coluna para não sobrecarregar)...")
                for col in colunas_texto:
                    valores_unicos = self.df[col].dropna().unique()
                    
                    if 0 < len(valores_unicos) <= 50:
                        prompt_valores = (
                            "Traduza os seguintes valores categóricos de dados para Português do Brasil (PT-BR). "
                            "Retorne APENAS um objeto JSON válido, sem markdown, onde a chave é o valor original e o valor é a tradução.\n"
                            f"Valores: {list(valores_unicos)}"
                        )
                        try:
                            resp_val = model.generate_content(prompt_valores)
                            txt_val = resp_val.text.replace("```json", "").replace("```", "").strip()
                            mapa_valores = json.loads(txt_val)
                            self.df[col] = self.df[col].replace(mapa_valores)
                            print(f"   - Coluna '{col}' traduzida.")
                        except Exception as e:
                            print(f"⚠️ Não foi possível traduzir a coluna '{col}': {e}")
                    else:
                        print(f"   - Coluna '{col}' ignorada (muitos valores únicos ou vazia).")

            print("\n✅ Tradução concluída com sucesso! Use a opção '5' ou '6' para ver os dados atualizados.")
            
        except Exception as e:
            print(f"\n❌ Erro inesperado durante a tradução: {e}")

    def _executar_com_tratamento(self, func):
        """Executa a função em uma thread isolada com tratamento de erros na GUI."""
        try:
            print("\n" + "="*55)
            self._garantir_dependencias()
            func()
            print("="*55 + "\n")
        except Exception as e:
            print(f"\n❌ Erro inesperado durante execução: {e}\n")

    def iniciar_gui(self):
        """Inicia a Interface Gráfica Moderna com CustomTkinter."""
        try:
            import customtkinter as ctk
        except ImportError:
            print(f"\n{Cor.VERMELHO}❌ ERRO: CustomTkinter não instalado. Execute: pip install customtkinter{Cor.RESET}")
            return

        import builtins
        import re

        # Configurações do Tema
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        app = ctk.CTk()
        app.title("🤖 Robô Analista de Dados - Piloto IA")
        app.geometry("1100x700")

        # -- Divisão da Tela: Menu lateral e Painel Principal --
        sidebar = ctk.CTkScrollableFrame(app, width=350, corner_radius=0)
        sidebar.pack(side="left", fill="y")

        main_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="transparent")
        main_frame.pack(side="right", fill="both", expand=True)

        console = ctk.CTkTextbox(main_frame, font=("Consolas", 13), wrap="word")
        console.pack(fill="both", expand=True, padx=10, pady=10)

        # -- Magia Negra 1: Redirecionar 'prints' para a Tela (Thread-safe) --
        class ThreadSafeRedirector:
            def __init__(self, widget):
                self.widget = widget
                self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

            def write(self, str_text):
                clean_text = self.ansi_escape.sub('', str_text) # Limpa cores ANSI do terminal antigo
                self.widget.after(0, self._insert_text, clean_text)

            def _insert_text(self, text):
                self.widget.insert("end", text)
                self.widget.see("end")

            def flush(self): pass

        sys.stdout = ThreadSafeRedirector(console)

        # -- Magia Negra 2: Transformar 'inputs' em Pop-ups (Thread-safe) --
        def get_input_threadsafe(prompt):
            result = [None]
            event = threading.Event()
            def show_dialog():
                clean_prompt = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', prompt)
                dialog = ctk.CTkInputDialog(text=clean_prompt, title="Entrada Solicitada")
                result[0] = dialog.get_input()
                event.set()
            app.after(10, show_dialog)
            event.wait() # Pausa a thread de processamento até o usuário digitar
            return result[0] or ""

        builtins.input = get_input_threadsafe

        # -- Renderizando Botões do Menu Lateral --
        ctk.CTkLabel(sidebar, text="🤖 Menu Principal", font=("Segoe UI", 22, "bold")).pack(pady=(20, 10))

        # Função Wrapper para evitar congelamento da GUI ao clicar
        def executar_acao(func):
            def wrapper():
                threading.Thread(target=self._executar_com_tratamento, args=(func,), daemon=True).start()
            return wrapper

        for key, (desc, func) in self.opcoes_menu.items():
            clean_desc = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', desc)
            btn = ctk.CTkButton(sidebar, text=clean_desc, command=executar_acao(func), anchor="w", font=("Segoe UI", 14))
            btn.pack(fill="x", padx=15, pady=5)

        # -- Botões de Utilitários Extras --
        btn_limpar = ctk.CTkButton(sidebar, text="🧹 Limpar Console", fg_color="#E67E22", hover_color="#D35400", command=lambda: console.delete("0.0", "end"))
        btn_limpar.pack(fill="x", padx=15, pady=(20, 5))

        btn_sair = ctk.CTkButton(sidebar, text="🚪 Sair", fg_color="#C0392B", hover_color="#922B21", command=app.quit)
        btn_sair.pack(fill="x", padx=15, pady=5)

        # Mensagens de Boas-Vindas Iniciais
        print("🤖 Interface Gráfica do Robô Analista CARREGADA com Sucesso!")
        print("📊 Suporta leitura de CSV, Excel (.xlsx), JSON, Clipboard e Bancos SQL.")
        print("👈 Selecione uma opção no menu lateral para iniciar sua Análise Exploratória...\n")

        app.mainloop()

if __name__ == "__main__":
    try:
        robo = RoboAnalistaDados()
        robo.iniciar_gui()
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado: {e}")
