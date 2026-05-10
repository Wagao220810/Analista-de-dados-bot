import pytest
import pandas as pd
import sys
import os
from unittest.mock import patch

# Garante que o Python encontre o arquivo robo_analista_dados.py na mesma pasta
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from robo_analista_dados import RoboAnalistaDados

def test_inicializacao_robo():
    """Testa se o robô inicia vazio e com as variáveis corretas."""
    robo = RoboAnalistaDados()
    
    assert robo.df is None
    assert robo.output_dir is None

@patch('robo_analista_dados.RoboAnalistaDados._criar_diretorio_saida')
def test_processar_novo_df(mock_criar_dir):
    """Testa a injeção de dados no robô usando um DataFrame falso (Dummy)."""
    robo = RoboAnalistaDados()
    
    # 1. Preparação (Arrange): Cria um DataFrame de mentira
    df_fake = pd.DataFrame({'Coluna1': [1, 2, 3], 'Coluna2': ['A', 'B', 'C']})
    
    # 2. Ação (Act): Envia os dados para a função do robô
    sucesso = robo._processar_novo_df(df_fake)
    
    # 3. Verificação (Assert): Confirma se o resultado foi o esperado
    assert sucesso is True
    assert robo.df is not None
    assert robo.df.shape == (3, 2)  # Deve ter 3 linhas e 2 colunas
    
    mock_criar_dir.assert_called_once()  # Garante que ele tentou criar a pasta de saída