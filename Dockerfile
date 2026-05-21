# Usa uma versão leve do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia a lista de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da sua aplicação para o contêiner
COPY . .

# O Cloud Run injeta a variável de ambiente $PORT dinamicamente. 
# Configuramos o Streamlit para escutar nessa porta.
CMD streamlit run linkedin_streamlit_app.py --server.port=${PORT:-8501} --server.address=0.0.0.0