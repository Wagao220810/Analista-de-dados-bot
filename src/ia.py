import os
import io
import webbrowser
import sys
import json
import pandas as pd

def _configurar_gemini():
    """Configura a API do Gemini e retorna o módulo genai."""
    try:
        import google.generativeai as genai
    except ImportError as e:
        print("❌ ERRO: A biblioteca 'google-generativeai' não está instalada.")
        print(f"   Detalhe técnico: {e}")
        if getattr(sys, 'frozen', False):
            print("   ⚠️ Você está rodando a versão .exe (standalone)!")
            print("   Para a IA funcionar, recompile o programa forçando a importação:")
            print("   pyinstaller --onefile --hidden-import google.generativeai data_analyst_robot.py")
        else:
            print("   Rode no terminal: pip install google-generativeai")
        return None

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    
    chaves_falsas = ["", "sua_chave_aqui", "AIzaSySuaChaveGiganteAqui123456789"]
    if api_key in chaves_falsas:
        print("\n⚠️ Chave de API ausente ou chave de teste detectada!")
        api_key = input("🔑 Cole sua API Key REAL do Google Gemini (ou Enter para cancelar): ").strip()
        if not api_key:
            return None
        os.environ["GEMINI_API_KEY"] = api_key
        
    genai.configure(api_key=api_key)
    return genai

def _obter_modelo(genai, preferencia="flash"):
    """Busca o modelo adequado disponível na API."""
    try:
        modelos_disponiveis = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    except Exception as e:
        if "API_KEY_INVALID" in str(e) or "API key not valid" in str(e):
            raise Exception("A API Key informada é inválida ou incorreta (recusada pelo Google). Cole a chave correta e tente novamente!")
        raise e
        
    if not modelos_disponiveis:
        raise Exception("Sua API Key não tem acesso a nenhum modelo de geração de texto.")
        
    modelo_escolhido = modelos_disponiveis[0]
    for m in modelos_disponiveis:
        if preferencia in m:
            modelo_escolhido = m
            break
    return genai.GenerativeModel(modelo_escolhido), modelo_escolhido

def explicar_anomalias(anomalias_resumo):
    """Usa a API do Gemini para interpretar os outliers detectados."""
    genai = _configurar_gemini()
    if not genai: return
        
    try:
        prompt = f"Você é um Cientista de Dados Sênior. Encontramos as seguintes anomalias (outliers) no dataset:\n{anomalias_resumo}\n\nPor favor, sugira possíveis motivos no mundo real que explicariam o aparecimento dessas anomalias nestas colunas. Seja direto, criativo e analítico."
        print("⏳ Investigando anomalias com o Gemini...\n")
        
        model, nome_modelo = _obter_modelo(genai, "flash")
        print(f"⚙️ Modelo selecionado automaticamente: {nome_modelo}")
        response = model.generate_content(prompt)
        
        print("✨ ANÁLISE DE ANOMALIAS PELO GEMINI ✨")
        print("-" * 50)
        print(response.text)
        print("-" * 50)
    except Exception as e:
        print(f"❌ Erro ao comunicar com a API do Gemini: {e}")

def obter_insights(df, output_dir):
    """Gera insights textuais usando a API do Gemini."""
    genai = _configurar_gemini()
    if not genai: return
        
    try:
        estatisticas = df.describe().to_string()
        amostra = df.head().to_string()
        prompt = f"Você é um Analista de Dados Sênior. Analise as estatísticas descritivas e a amostra dos dados abaixo. Forneça um resumo executivo com os 3 principais insights de negócios. Seja direto, claro e use linguagem profissional de negócios.\n\nEstatísticas:\n{estatisticas}\n\nAmostra de Dados:\n{amostra}"
        
        print("⏳ Analisando dados com o Gemini... (isso pode levar alguns segundos)\n")
        
        model, nome_modelo = _obter_modelo(genai, "flash")
        print(f"⚙️ Modelo selecionado automaticamente: {nome_modelo}")
        response = model.generate_content(prompt)
        
        print("✨ INSIGHTS GERADOS PELO GEMINI ✨")
        print("-" * 50)
        print(response.text)
        print("-" * 50)
        
        if output_dir:
            filepath = os.path.join(output_dir, 'insights_gemini.txt')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"✅ Insights textuais salvos em: '{filepath}'")
    except Exception as e:
        print(f"❌ Erro ao comunicar com a API do Gemini: {e}")

def analise_automatizada(df, output_dir):
    """Executa uma análise completa (Auto-Pilot) do dataset usando o Gemini."""
    print("⚙️ 1/3 Extraindo contexto total dos dados (Estatísticas, Nulos, Estrutura)...")
    buffer_info = io.StringIO()
    df.info(buf=buffer_info)
    info_str = buffer_info.getvalue()
    
    estatisticas = df.describe().to_string()
    amostra = df.head().to_string()
    nulos = df.isnull().sum().to_string()
    
    print("🧠 2/3 Preparando o cérebro da IA...")
    genai = _configurar_gemini()
    if not genai: return False
        
    try:
        prompt = f"""Você é um Cientista de Dados Sênior Autônomo.
Sua missão é atuar como um "Piloto Automático" e realizar a análise completa deste dataset.
Vou fornecer o contexto estrutural e estatístico. Sua saída deve ser um relatório definitivo, analítico e extremamente profissional formatado em Markdown.

INFORMAÇÕES DO DATASET:
--- INFORMAÇÕES GERAIS E TIPOS ---
{info_str}
--- VALORES NULOS (MISSING DATA) ---
{nulos}
--- ESTATÍSTICAS DESCRITIVAS ---
{estatisticas}
--- AMOSTRA DOS DADOS (PRIMEIRAS LINHAS) ---
{amostra}

Crie um relatório rico focado em negócios, contendo obrigatoriamente:
# 📊 Relatório Analítico Executivo
1. **Visão Geral e Qualidade dos Dados:** O que este dataset representa? Os dados estão limpos? Existem nulos problemáticos?
2. **Principais Insights Estatísticos:** Padrões interessantes, médias e variações que chamam a atenção.
3. **Detecção de Anomalias:** Possíveis outliers e comportamentos anormais.
4. **Próximos Passos e Ações de Negócio:** Recomendações práticas do que fazer com base nesses números.
"""
        print("⏳ 3/3 O Gemini está redigindo o Relatório Executivo (isso pode demorar uns 15 segundos)...")
        
        model, nome_modelo = _obter_modelo(genai, "pro")
        print(f"🤖 Modelo selecionado automaticamente: {nome_modelo}")
        response = model.generate_content(prompt)
        
        filepath = os.path.join(output_dir or '.', 'Relatorio_Completo_AutoPilot_Gemini.md')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        # Converte o Markdown para um Relatório HTML elegante pronto para Salvar como PDF
        try:
            import markdown
            # Converte o texto e suporta tabelas
            html_content = markdown.markdown(response.text, extensions=['tables'])
            html_styled = f"""
            <html><head><meta charset='utf-8'><style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: 40px auto; color: #333; padding: 20px; }}
                h1, h2, h3 {{ color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #f8f9fa; font-weight: bold; }}
                .btn-print {{ float: right; background: #007bff; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 5px; font-weight: bold; }}
                .btn-print:hover {{ background: #0056b3; }}
                @media print {{ .btn-print {{ display: none; }} body {{ margin: 0; padding: 0; }} }}
            </style></head><body>
            <button class="btn-print" onclick="window.print()">🖨️ Salvar como PDF</button>
            {html_content}
            </body></html>
            """
            html_filepath = os.path.join(output_dir or '.', 'Relatorio_AutoPilot.html')
            with open(html_filepath, 'w', encoding='utf-8') as f:
                f.write(html_styled)
            
            print(f"✅ Versão para Impressão/PDF gerada em: '{html_filepath}'")
            webbrowser.open(f'file://{os.path.abspath(html_filepath)}')
        except ImportError:
            print("💡 DICA: Instale a biblioteca 'markdown' (pip install markdown) para gerar o relatório com layout pronto para PDF!")

        print("\n✨ RELATÓRIO COMPLETADO COM SUCESSO ✨")
        print(f"✅ Arquivo salvo em: '{filepath}'")
        print("💡 DICA: Abra o arquivo .md gerado no VS Code (ou em qualquer leitor de Markdown) para ver a formatação!")
        return True
    except Exception as e:
        print(f"❌ Erro ao gerar análise automatizada: {e}")
        return False

def estruturar_coluna_caotica(df, coluna):
    """
    (ETL Inteligente) Usa o Gemini em modo JSON estrito para extrair 
    entidades estruturadas de textos bagunçados e criar novas colunas.
    """
    genai_module = _configurar_gemini()
    if not genai_module:
        return df
        
    _, nome_modelo = _obter_modelo(genai_module, "flash")
    
    # Força a API a retornar EXCLUSIVAMENTE um objeto JSON válido
    modelo = genai_module.GenerativeModel(
        model_name=nome_modelo,
        generation_config={"response_mime_type": "application/json"}
    )
    
    # Proteção de Rate Limit: Para testes locais, processaremos apenas uma amostra se for muito grande
    df_alvo = df.head(50) if len(df) > 50 else df
    if len(df) > 50:
        print(f"⚠️ Aviso: Dataset grande ({len(df)} linhas). Processando apenas as 50 primeiras para evitar bloqueios da API.")
    
    resultados = []
    
    for index, texto in df_alvo[coluna].items():
        if pd.isna(texto) or str(texto).strip() == "":
            resultados.append({}) # Linha vazia, JSON vazio
            continue
            
        prompt = f"Você é um pipeline de extração de dados. Analise o texto abaixo.\nExtraia entidades como: Nome, CPF, Data, Valor Financeiro, Status, Telefone ou Email.\nRetorne apenas as chaves que conseguir encontrar.\n\nTEXTO:\n{texto}"
        
        try:
            resposta = modelo.generate_content(prompt)
            dados_json = json.loads(resposta.text)
            resultados.append(dados_json)
        except Exception as e:
            resultados.append({"erro_extracao_ia": "falha"})
            
    df_estruturado = pd.DataFrame(resultados)
    df_estruturado = df_estruturado.add_prefix(f"{coluna}_ia_")
    df_estruturado.index = df_alvo.index
    df_final = pd.concat([df, df_estruturado], axis=1)
    
    return df_final