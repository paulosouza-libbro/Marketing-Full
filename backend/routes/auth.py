"""
Autenticação simples com JWT — credenciais via variáveis de ambiente.
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET", "libbro-secret-change-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_DAYS = 30

ADMIN_USER = os.getenv("ADMIN_USER", "paulo")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "libbro2024")


class LoginRequest(BaseModel):
    usuario: str
    senha: str


def criar_token(usuario: str) -> str:
    expire = datetime.utcnow() + timedelta(days=TOKEN_EXPIRE_DAYS)
    return jwt.encode({"sub": usuario, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")
        if not usuario:
            raise HTTPException(status_code=401, detail="Token inválido")
        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")


@router.post("/login")
def login(body: LoginRequest):
    if body.usuario != ADMIN_USER or body.senha != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")
    token = criar_token(body.usuario)
    return {"token": token, "usuario": body.usuario, "expira_em_dias": TOKEN_EXPIRE_DAYS}


@router.get("/me")
def me(usuario: str = Depends(verificar_token)):
    return {"usuario": usuario, "autenticado": True}
