# Usa uma imagem oficial do Python leve
FROM python:3.12-slim

# Evita que o Python gere arquivos .pyc e garante logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias para o Postgres
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências do projeto
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o restante do código do projeto
COPY . /app/

# Expõe a porta 8000
EXPOSE 8000

# Comando para rodar o servidor quando o container subir
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]