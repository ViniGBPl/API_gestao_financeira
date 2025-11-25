# 💰 API de Gestão Financeira

![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)
![CI/CD](https://img.shields.io/github/actions/workflow/status/ViniGBPl/API_gestao_financeira/ci_cd.yml?label=CI%2FCD&logo=github)
![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)
![Django](https://img.shields.io/badge/Django-5.0+-092E20?logo=django)

Uma API RESTful completa e containerizada para controle de finanças pessoais. O sistema permite o registro de receitas e despesas, gera relatórios mensais consolidados e oferece exportação de dados (CSV/PDF), tudo documentado automaticamente via Swagger.

Este projeto demonstra um ciclo completo de **DevOps** e Engenharia de Software, incluindo testes automatizados, banco de dados relacional robusto e pipelines de entrega contínua.

## 🚀 Funcionalidades Principais

- **CRUD Completo:** Gestão de Receitas e Despesas com validações de negócio.
- **Dashboard Financeiro:** Endpoint dedicado (`/saldo_mensal`) que utiliza agregação de dados no banco para performance.
- **Relatórios Dinâmicos:**
  - Extrato em **CSV** (Planilhas).
  - Relatório gerencial em **PDF** (Gerado com ReportLab).
- **Documentação Interativa:** Interface Swagger UI/OpenAPI automática.
- **Filtros Avançados:** Busca por descrição, filtro por tipo/data e ordenação dinâmica.

## 🛠️ Stack Tecnológica & Engenharia

- **Linguagem:** Python 3.12
- **Framework:** Django & Django REST Framework
- **Banco de Dados:** PostgreSQL 15 (Substituindo o SQLite para produção)
- **Infraestrutura:** Docker & Docker Compose (Multi-stage build)
- **CI/CD:** GitHub Actions (Pipeline de Testes e Deploy no Docker Hub)
- **Testes:** Unittest/APITestCase (Cobertura de models, views e regras de negócio)

## 📦 Como rodar o projeto

A forma recomendada de executar o projeto é utilizando **Docker**, garantindo que o ambiente seja idêntico ao de desenvolvimento e produção.

### Pré-requisitos
- Docker e Docker Compose instalados.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/ViniGBPl/API_gestao_financeira.git](https://github.com/ViniGBPl/API_gestao_financeira.git)
   cd API_gestao_financeira
   ```
2. **Suba o ambiente (Aplicação + Banco de Dados):**
    ```bash
    docker-compose up -d --build
    ```
  Isso irá baixar a imagem do Postgres, construir a imagem da API e configurar a rede automaticamente.

3. **Aplique as migrações (Configuração inicial do Banco):**
    ```bash
   docker-compose exec web python manage.py migrate
    ```
4. **(Opcional) Crie um superusuário para o Admin:**
    ```bash
   docker-compose exec web python manage.py createsuperuser
    ```
## 🔗 Acessando a Aplicação
- API (Swagger UI): http://localhost:8000/api/schema/swagger-ui/

- Painel Admin: http://localhost:8000/admin/

## ✅ Testes e Qualidade

O projeto conta com uma suíte de testes automatizados que valida desde a criação de lançamentos até a geração de binários (PDFs). Para rodar os testes dentro do container:

  ```bash
  docker-compose exec web python manage.py test
  ```
## ⚙️ Estrutura de CI/CD

O projeto possui um workflow configurado no GitHub Actions que realiza:

1.**Integração Contínua (CI):** A cada push, o ambiente é recriado e todos os testes são executados.

2.**Entrega Contínua (CD):** Se os testes passarem na branch main, uma nova imagem Docker é construída e publicada automaticamente no Docker Hub.



