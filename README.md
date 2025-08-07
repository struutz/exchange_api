# 💰 Currency Tracker API

API para gerenciamento de transações com conversão de moedas, baseada em Django + GraphQL. A aplicação consulta taxas de câmbio em tempo real e permite:

- Cadastrar e listar transações
- Converter valores entre moedas
- Visualizar gráficos de gastos por categoria
- Acompanhar um resumo mensal
- Receber alertas via Webhooks

---

## 🧱 Stack utilizada

- [Python 3.11](https://www.python.org/)
- [Django 4+](https://www.djangoproject.com/)
- [Strawberry GraphQL](https://strawberry.rocks/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker + Docker Compose](https://docs.docker.com/)
- Integração com: [ExchangeRatesAPI.io](https://exchangeratesapi.io/)

---

## 🚀 Como rodar o projeto

### Pré-requisitos

- Docker
- Docker Compose
- Make (opcional, mas recomendado)

---

### 🔧 Configuração do ambiente

1. Copie o arquivo de variáveis de ambiente:

```bash
cp .env.example .env
