"""
Modelos de Task e Subtask para campanhas da Libbro.

Arquitetura:
  Campanha
    └── Tasks (rodam em PARALELO entre si)
          └── Subtasks (rodam em SEQUÊNCIA dentro de cada task)
                └── Cada subtask pode exigir aprovação humana antes de liberar a próxima
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
import uuid


AgentId = Literal[
    "diretor", "pesquisador_conto", "estrategista",
    "copywriter", "designer", "produtor_video",
    "seo_youtube", "social_media", "growth", "analista"
]

SubtaskStatus = Literal[
    "pendente",
    "executando",
    "aguardando_aprovacao",
    "aprovada",
    "rejeitada",
    "concluida",
    "erro",
]

TaskStatus = Literal[
    "pendente",
    "executando",
    "aguardando_aprovacao",
    "concluida",
    "erro",
]


class SubtaskCreate(BaseModel):
    titulo: str
    descricao: str
    agente: str
    requer_aprovacao: bool = True
    instrucoes_extras: Optional[str] = None


class Subtask(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    titulo: str
    descricao: str
    agente: str
    requer_aprovacao: bool = True
    instrucoes_extras: Optional[str] = None
    status: str = "pendente"
    output: Optional[str] = None
    output_arquivos: List[str] = []
    feedback_rejeicao: Optional[str] = None
    criado_em: str = Field(default_factory=lambda: datetime.now().isoformat())
    iniciado_em: Optional[str] = None
    concluido_em: Optional[str] = None


class TaskCreate(BaseModel):
    titulo: str
    descricao: str
    subtasks: List[SubtaskCreate]


class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    campanha_id: str
    titulo: str
    descricao: str
    subtasks: List[Subtask] = []
    status: str = "pendente"
    inicio: str = "automatico"  # "automatico" | "manual"
    criado_em: str = Field(default_factory=lambda: datetime.now().isoformat())
    atualizado_em: str = Field(default_factory=lambda: datetime.now().isoformat())


class TaskAddRequest(BaseModel):
    titulo: str
    descricao: str
    subtasks: List[SubtaskCreate]
    inicio: str = "automatico"  # "automatico" | "manual"


class SubtaskApproval(BaseModel):
    action: str  # "approve" | "reject"
    feedback: Optional[str] = None
