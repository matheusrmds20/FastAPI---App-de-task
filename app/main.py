from fastapi import FastAPI
from .database.database import engine
from .models.task import Base
from routes.tasks import router_task
from routes.auth import router_auth
import asyncio
from fastapi.responses import StreamingResponse
from app.core.config import settings

# Print temporário para conferir se as configurações subiram
print("--- DEBUG SETTINGS ---")
print(f"SECRET_KEY carregada: {settings.SECRET_KEY}")
print(f"ALGORITHM carregado: {settings.ALGORITHM}")
print("----------------------")

#Executa a criacao do banco de dados | execurar uma vez
Base.metadata.create_all(bind=engine)

#Rodar a API
app = FastAPI()

# Inclusao das rotas
app.include_router(router_auth)
app.include_router(router_task)


# Rota raiz
@app.get("/")
def root():
    return {"status": "ok"}



