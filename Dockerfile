FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean

WORKDIR /app

# Copia apenas os requirements primeiro (para cache)
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante da aplicação
COPY . .

# Exposição de porta
EXPOSE 8000

# EntryPoint de produção (sobrescrito no docker-compose em dev)
CMD ["gunicorn", "exchange_api.wsgi:application", "--bind", "0.0.0.0:8000"]
