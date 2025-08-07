# Caminho do arquivo Makefile: na raiz do projeto

# Variáveis
PROJECT_NAME=backend
DOCKER_COMPOSE=docker-compose
PYTHON_MANAGE=python manage.py
EXEC_BACKEND=$(DOCKER_COMPOSE) exec $(PROJECT_NAME)
EXEC_POSTGRES=$(DOCKER_COMPOSE) exec postgres

# Comandos Docker
up:
	$(DOCKER_COMPOSE) up --build -d

down:
	$(DOCKER_COMPOSE) down -v

restart: down up

logs:
	$(DOCKER_COMPOSE) logs -f

# Banco de dados
psql:
	$(EXEC_POSTGRES) psql -U local -d local-tests

migrate:
	$(EXEC_BACKEND) $(PYTHON_MANAGE) migrate

makemigrations:
	$(EXEC_BACKEND) $(PYTHON_MANAGE) makemigrations

createsuperuser:
	$(EXEC_BACKEND) $(PYTHON_MANAGE) createsuperuser

# Django
shell:
	$(EXEC_BACKEND) $(PYTHON_MANAGE) shell

collectstatic:
	$(EXEC_BACKEND) $(PYTHON_MANAGE) collectstatic --noinput

# Testes
test:
	$(EXEC_BACKEND) pytest

test-watch:
	$(EXEC_BACKEND) ptw --runner "pytest --reuse-db"

coverage:
	$(EXEC_BACKEND) pytest --cov=.

coverage-html:
	$(EXEC_BACKEND) pytest --cov=. --cov-report html

# Utilitários
build:
	$(DOCKER_COMPOSE) build

bash:
	$(EXEC_BACKEND) bash

ps:
	$(DOCKER_COMPOSE) ps

prune:
	docker system prune -f

help:
	@echo "Comandos disponíveis:"
	@echo "  up               - Sobe os containers com build"
	@echo "  down             - Derruba os containers e remove volumes"
	@echo "  restart          - Reinicia a stack"
	@echo "  logs             - Mostra logs dos containers"
	@echo "  psql             - Acessa o PostgreSQL"
	@echo "  migrate          - Roda as migrações do Django"
	@echo "  makemigrations   - Cria novas migrações"
	@echo "  createsuperuser  - Cria um superusuário"
	@echo "  shell            - Abre shell do Django"
	@echo "  collectstatic    - Coleta arquivos estáticos"
	@echo "  test             - Executa os testes com pytest"
	@echo "  test-watch       - Executa os testes com watch mode (pytest-watch)"
	@echo "  coverage         - Executa os testes com cobertura"
	@echo "  coverage-html    - Executa testes com relatório HTML de cobertura"
	@echo "  build            - Faz build da imagem"
	@echo "  bash             - Entra no bash do backend"
	@echo "  ps               - Lista os containers"
	@echo "  prune            - Remove volumes e redes não utilizados"
