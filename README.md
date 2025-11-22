# 💰 API de Gestão Financeira Pessoal

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-5.0+-green)

Uma API RESTful desenvolvida para auxiliar no controle de finanças pessoais. O sistema permite o registro de receitas e despesas, gera relatórios mensais de saldo e oferece exportação de dados em formatos CSV e PDF.

Este projeto foi construído com foco em boas práticas de desenvolvimento backend, organização de código e documentação automática.

## 🚀 Funcionalidades Principais

- **CRUD de Transações:** Cadastro, listagem, atualização e remoção de Receitas e Despesas.
- **Cálculo de Saldo:** Endpoint dedicado que consolida os lançamentos do mês e retorna o saldo final.
- **Relatórios:**
  - Exportação de extrato em **CSV** (Planilhas).
  - Exportação de relatório em **PDF**.
- **Documentação Interativa:** Swagger UI (OpenAPI) configurado.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- **Framework Principal:** Django
- **API:** Django REST Framework (DRF)
- **Documentação:** Drf-spectacular (Swagger)
- **Geração de PDF:** ReportLab
- **Banco de Dados:** SQLite (Desenvolvimento)

## 📦 Como rodar o projeto localmente

Siga os passos abaixo para executar a API na sua máquina:

### 1. Clone o repositório
```bash
git clone [https://github.com/ViniGBPl/API_gestao_financeira.git](https://github.com/ViniGBPl/API_gestao_financeira.git)
cd API_gestao_financeira
```

### 2. Crie e ative o ambiente virtual

#### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux/Mac
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute as migrações e inicie o servidor

````bash
python manage.py migrate
python manage.py runserver
`````
























