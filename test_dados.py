import pytest
import pandas as pd
import sys
import os
from unittest.mock import patch

# Garante que o Python encontre a pasta src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import dados

@patch('src.dados.os.path.exists')
@patch('builtins.input')
@patch('src.dados.pd.read_csv')
def test_carregar_arquivo_csv(mock_read_csv, mock_input, mock_exists):
    """Testa a leitura de um CSV "falso" usando mocks."""
    # 1. Arrange: Prepara os dublês
    mock_input.return_value = "caminho_falso.csv" # Simula o usuário digitando o caminho
    mock_exists.return_value = True               # Simula que o arquivo existe
    
    df_esperado = pd.DataFrame({'Nome': ['João', 'Maria'], 'Idade': [30, 25]})
    mock_read_csv.return_value = df_esperado      # Simula o Pandas lendo o CSV
    
    # 2. Act: Executa a função
    df_resultado = dados.carregar_arquivo()
    
    # 3. Assert: Verifica se a função repassou tudo corretamente
    assert df_resultado.equals(df_esperado)
    mock_read_csv.assert_called_once_with("caminho_falso.csv")