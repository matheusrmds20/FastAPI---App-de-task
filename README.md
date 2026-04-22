# FastAPI Auth API (JWT + CLI)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Pydantic](https://img.shields.io/badge/pydantic-%23E92063.svg?style=for-the-badge&logo=pydantic&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

## Projeto backend em FastAPI com autenticação JWT, banco de dados relacional e um CLI em Python que consome a API. Este projeto foi feito com foco em aprendizado prático e em demonstrar competências esperadas para estágio/júnior backend.

## ✨ Funcionalidades

Cadastro e login de usuários

Hash de senha com bcrypt

Autenticação com JWT (access token)

Rotas protegidas

Persistência de token no cliente (CLI)

Consumo real da API via terminal

## 🛠️ Tecnologias

Python 3.11+

FastAPI

SQLAlchemy

Pydantic

JWT (python-jose)

Requests (CLI)

## Estrutura do projeto

```text
FastAPI/
├── main.py
├── database.py
├── models_db.py
├── schemas.py
├── auth.py
├── routes/
│   └── auth.py
└── requirements.txt

cli/
└── main.py

```

## Como rodar o projeto

### 1️⃣ Clonar o repositório
```text
git clone <repo-url>
cd backend
```
### 2️⃣ Criar ambiente virtual
```text
python -m venv venv
source venv/bin/activate # Windows: venv\\Scripts\\activate
```
### 3️⃣ Instalar dependências
```text
pip install -r requirements.txt
```
### 4️⃣ Rodar a API
```text
uvicorn main:app --reload
```
### acesse:
```text
Swagger: http://localhost:8000/docs
```

## Usando o CLI
```text
cd cli
python main.py
```
## Autenticação JWT

Access Token gerado no login

Enviado no header:
```text
Authorization: Bearer <token>
```
Token possui tempo de expiração

Ao expirar, é necessário novo login
