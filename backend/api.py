"""
Libbro Marketing App — API REST (FastAPI)
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
import json
from pathlib import Path

app = FastAPI(
    title="Libbro Marketing API",
    description="API da Agência de Marketing Autônoma da Libbro",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://marketing-full.vercel.app"],
    allow_origin_regex=r"https://.*\.railway\.app|https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Storage simples em JSON (substituir por PostgreSQL em produção) ───────────

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def load_json(filename: str) -> list:
    path = DATA_DIR / filename
    if not path.exists():
        return []
    return json.loads(path.read_text())

def save_json(filename: str, data: list):
    (DATA_DIR / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str))

# ─── Models ───────────────────────────────────────────────────────────────────

class BriefingRequest(BaseModel):
    briefing: str
    conto: str
    canais: List[str] = ["youtube"]

class ApprovalAction(BaseModel):
    action: str  # "approve" | "reject"
    feedback: Optional[str] = None

class ContoCreate(BaseModel):
    slug: str
    nome: str
    estilo: str

# ─── Rotas: Health ─────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "ok", "app": "Libbro Marketing API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# ─── Rotas: Campanhas ──────────────────────────────────────────────────────────

@app.get("/campanhas")
def listar_campanhas():
    return load_json("campanhas.json")

@app.post("/campanhas")
async def criar_campanha(body: BriefingRequest, background_tasks: BackgroundTasks):
    campanha_id = str(uuid.uuid4())[:8]
    campanha = {
        "id": campanha_id,
        "briefing": body.briefing,
        "conto": body.conto,
        "canais": body.canais,
        "status": "processando",
        "criado_em": datetime.now().isoformat(),
        "atualizado_em": datetime.now().isoformat(),
        "etapas": [
            {"nome": "Briefing", "status": "pendente"},
            {"nome": "Pesquisa", "status": "pendente"},
            {"nome": "Estratégia", "status": "pendente"},
            {"nome": "Copy", "status": "pendente"},
            {"nome": "Visual", "status": "pendente"},
            {"nome": "SEO", "status": "pendente"},
            {"nome": "Aprovação", "status": "pendente"},
        ],
    }
    campanhas = load_json("campanhas.json")
    campanhas.append(campanha)
    save_json("campanhas.json", campanhas)

    # Dispara os agentes em background
    background_tasks.add_task(executar_agentes, campanha_id, body.briefing, body.conto, body.canais)

    return {"id": campanha_id, "status": "processando", "mensagem": "Agentes iniciados — acompanhe em /campanhas/" + campanha_id}

@app.get("/campanhas/{campanha_id}")
def detalhe_campanha(campanha_id: str):
    campanhas = load_json("campanhas.json")
    campanha = next((c for c in campanhas if c["id"] == campanha_id), None)
    if not campanha:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")
    return campanha

# ─── Rotas: Aprovações ─────────────────────────────────────────────────────────

@app.get("/aprovacoes")
def listar_aprovacoes():
    return load_json("aprovacoes.json")

@app.post("/aprovacoes/{item_id}")
def aprovar_ou_rejeitar(item_id: str, body: ApprovalAction):
    aprovacoes = load_json("aprovacoes.json")
    item = next((a for a in aprovacoes if a["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    item["status"] = "aprovado" if body.action == "approve" else "rejeitado"
    item["feedback"] = body.feedback
    item["revisado_em"] = datetime.now().isoformat()
    save_json("aprovacoes.json", aprovacoes)

    if body.action == "approve":
        # TODO: Disparar publicação automática
        return {"status": "aprovado", "mensagem": "Conteúdo aprovado — publicação agendada"}
    else:
        return {"status": "rejeitado", "mensagem": "Conteúdo rejeitado — agentes notificados para revisão"}

# ─── Rotas: Assets / Contos ────────────────────────────────────────────────────

@app.get("/contos")
def listar_contos():
    assets_path = Path("../assets/ilustracoes-contos")
    if not assets_path.exists():
        return []
    contos = []
    for d in assets_path.iterdir():
        if d.is_dir():
            estilo_file = d / "estilo.md"
            contos.append({
                "slug": d.name,
                "nome": d.name.replace("-", " ").title(),
                "tem_estilo": estilo_file.exists(),
                "referencias": len(list((d / "referencias").glob("*"))) if (d / "referencias").exists() else 0,
                "personagens": len(list((d / "personagens").glob("*"))) if (d / "personagens").exists() else 0,
            })
    return contos

@app.post("/contos")
def criar_conto(body: ContoCreate):
    base = Path("../assets/ilustracoes-contos") / body.slug
    if base.exists():
        raise HTTPException(status_code=400, detail="Conto já existe")
    (base / "referencias").mkdir(parents=True)
    (base / "personagens").mkdir(parents=True)
    (base / "estilo.md").write_text(f"# Estilo Visual — {body.nome}\n\n{body.estilo}")
    return {"slug": body.slug, "nome": body.nome, "status": "criado"}

@app.get("/contos/{slug}")
def detalhe_conto(slug: str):
    base = Path("../assets/ilustracoes-contos") / slug
    if not base.exists():
        raise HTTPException(status_code=404, detail="Conto não encontrado")
    estilo_file = base / "estilo.md"
    return {
        "slug": slug,
        "nome": slug.replace("-", " ").title(),
        "estilo": estilo_file.read_text() if estilo_file.exists() else "",
        "referencias": [f.name for f in (base / "referencias").glob("*")] if (base / "referencias").exists() else [],
        "personagens": [f.name for f in (base / "personagens").glob("*")] if (base / "personagens").exists() else [],
    }

# ─── Rotas: Agentes ────────────────────────────────────────────────────────────

@app.get("/agentes")
def listar_agentes():
    return [
        {"id": "diretor", "nome": "Diretor", "icon": "🎯", "status": "idle"},
        {"id": "pesquisador", "nome": "Pesquisador", "icon": "🔍", "status": "idle"},
        {"id": "estrategista", "nome": "Estrategista", "icon": "🗺️", "status": "idle"},
        {"id": "copywriter", "nome": "Copywriter", "icon": "✍️", "status": "idle"},
        {"id": "designer", "nome": "Designer", "icon": "🎨", "status": "idle"},
        {"id": "produtor_video", "nome": "Produtor de Vídeo", "icon": "🎬", "status": "idle"},
        {"id": "seo_youtube", "nome": "SEO/YouTube", "icon": "📈", "status": "idle"},
        {"id": "social_media", "nome": "Social Media", "icon": "📱", "status": "idle"},
        {"id": "growth", "nome": "Growth", "icon": "⚡", "status": "idle"},
        {"id": "analista", "nome": "Analista", "icon": "📊", "status": "idle"},
    ]

# ─── Background: execução dos agentes ─────────────────────────────────────────

async def executar_agentes(campanha_id: str, briefing: str, conto: str, canais: list):
    """
    Executa a crew de agentes em background.
    Por ora faz update de status — integração com CrewAI vai aqui.
    """
    import asyncio

    campanhas = load_json("campanhas.json")
    campanha = next((c for c in campanhas if c["id"] == campanha_id), None)
    if not campanha:
        return

    etapas = ["Briefing", "Pesquisa", "Estratégia", "Copy", "Visual", "SEO"]
    for i, etapa in enumerate(etapas):
        await asyncio.sleep(2)  # Simula processamento
        campanha["etapas"][i]["status"] = "concluido"
        campanha["atualizado_em"] = datetime.now().isoformat()
        save_json("campanhas.json", campanhas)

    # Cria item de aprovação
    aprovacoes = load_json("aprovacoes.json")
    aprovacoes.append({
        "id": str(uuid.uuid4())[:8],
        "campanha_id": campanha_id,
        "conto": conto,
        "canais": canais,
        "status": "aguardando",
        "criado_em": datetime.now().isoformat(),
        "conteudo": {
            "titulo": f"[Gerado pelos agentes] Campanha do conto {conto}",
            "copy": "Copy gerada pelos agentes — integração CrewAI pendente",
            "imagens": [],
            "seo": {},
        },
    })
    save_json("aprovacoes.json", aprovacoes)

    campanha["status"] = "aguardando_aprovacao"
    campanha["etapas"][6]["status"] = "aguardando"
    campanha["atualizado_em"] = datetime.now().isoformat()
    save_json("campanhas.json", campanhas)


# ─── Rotas: Integrações de IA ──────────────────────────────────────────────────

@app.post("/gerar/imagem")
async def gerar_imagem(body: dict):
    """
    Gera imagem com DALL-E 3 ou Stable Diffusion.
    body: { "prompt": str, "conto": str, "formato": str, "modelo": "dalle|stability" }
    """
    from tools.image_generator import ImageGenerator
    from pathlib import Path

    gen = ImageGenerator()
    conto = body.get("conto", "")
    formato = body.get("formato", "thumbnail")
    modelo = body.get("modelo", "dalle")
    prompt_base = body.get("prompt", "")

    # Enriquece prompt com estilo do conto
    if conto:
        assets = Path("../assets/ilustracoes-contos") / conto / "estilo.md"
        estilo = assets.read_text() if assets.exists() else ""
        prompt = gen.construir_prompt_conto(estilo, prompt_base, formato)
    else:
        prompt = prompt_base

    if modelo == "stability":
        return gen.gerar_stability(prompt)
    else:
        size_map = {"thumbnail": "1792x1024", "post_instagram": "1024x1024", "story": "1024x1792"}
        return gen.gerar_dalle(prompt, size=size_map.get(formato, "1792x1024"))


@app.post("/gerar/audio")
async def gerar_audio(body: dict):
    """
    Gera narração com ElevenLabs.
    body: { "texto": str, "voice_id": str (opcional) }
    """
    from tools.voice_generator import VoiceGenerator
    gen = VoiceGenerator()
    return gen.gerar_narração(body.get("texto", ""), body.get("voice_id"))


@app.get("/vozes")
async def listar_vozes():
    from tools.voice_generator import VoiceGenerator
    return VoiceGenerator().listar_vozes()


@app.post("/gerar/video")
async def gerar_video(body: dict):
    """
    Gera vídeo com Runway ML.
    body: { "prompt": str, "image_url": str (opcional), "duracao": int }
    """
    from tools.video_generator import VideoGenerator
    gen = VideoGenerator()
    return gen.gerar_runway(body.get("prompt", ""), body.get("image_url"), body.get("duracao", 4))


@app.get("/analytics/canal")
async def analytics_canal(dias: int = 30):
    from tools.content_analyzer import YouTubeAnalyzer


# Import de rotas adicionais
from routes.auth import router as auth_router
from routes.imagem import router as imagem_router
app.include_router(auth_router)
app.include_router(imagem_router)

from routes.assets import router as assets_router
app.include_router(assets_router)

from routes.meta import router as meta_router
app.include_router(meta_router)


# ─── Composição de thumbnail ────────────────────────────────────────────────

@app.post("/thumbnail/compor")
async def compor_thumbnail(body: dict):
    """
    Adiciona logo do conto sobre uma imagem base e gera a thumbnail final.
    body: { "imagem_path": str, "conto": str, "posicao_logo": str, "logo_escala": float }
    """
    from tools.thumbnail_composer import ThumbnailComposer
    composer = ThumbnailComposer()
    return composer.compor_thumbnail(
        imagem_base_path=body.get("imagem_path"),
        conto_slug=body.get("conto"),
        posicao_logo=body.get("posicao_logo", "bottom-right"),
        logo_escala=body.get("logo_escala", 0.40),
    )


@app.post("/thumbnail/gerar-completa")
async def gerar_thumbnail_completa(body: dict):
    """
    Fluxo completo: gera imagem com DALL-E + adiciona logo do conto automaticamente.
    body: { "prompt": str, "conto": str, "posicao_logo": str }
    """
    from tools.image_generator import ImageGenerator
    from tools.thumbnail_composer import ThumbnailComposer
    from pathlib import Path

    # 1. Gera imagem base
    gen = ImageGenerator()
    conto = body.get("conto", "")
    assets = Path("../assets/ilustracoes-contos") / conto / "estilo.md"
    estilo = assets.read_text() if assets.exists() else ""
    prompt = gen.construir_prompt_conto(estilo, body.get("prompt", ""), "thumbnail")
    resultado = gen.gerar_dalle(prompt, size="1792x1024")

    if resultado.get("status") != "ok":
        return resultado

    # 2. Compõe com logo
    composer = ThumbnailComposer()
    thumbnail = composer.compor_thumbnail(
        imagem_base_path=resultado["local"],
        conto_slug=conto,
        posicao_logo=body.get("posicao_logo", "bottom-right"),
    )

    return {
        "status": "ok",
        "imagem_base": resultado["url"],
        "thumbnail_final": thumbnail.get("local"),
        "conto": conto,
    }


# ─── Rotas: Tasks ──────────────────────────────────────────────────────────────

from models.task import Task, TaskAddRequest, Subtask, SubtaskApproval

@app.post("/campanhas/{campanha_id}/tasks/gerar")
async def gerar_tasks_da_campanha(campanha_id: str, background_tasks: BackgroundTasks):
    """
    O Diretor lê o briefing da campanha e gera automaticamente todas as tasks.
    Pode ser chamado ao criar a campanha ou a qualquer momento depois.
    """
    campanhas = load_json("campanhas.json")
    campanha = next((c for c in campanhas if c["id"] == campanha_id), None)
    if not campanha:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")

    from tools.task_planner import planejar_tasks
    tasks_data = planejar_tasks(campanha["briefing"], campanha["conto"], campanha["canais"])

    todas_tasks = load_json("tasks.json")

    novas = []
    for td in tasks_data:
        subtasks = [
            Subtask(
                titulo=s["titulo"],
                descricao=s["descricao"],
                agente=s["agente"],
                requer_aprovacao=s.get("requer_aprovacao", True),
            ).model_dump()
            for s in td.get("subtasks", [])
        ]
        task = Task(
            campanha_id=campanha_id,
            titulo=td["titulo"],
            descricao=td["descricao"],
            subtasks=subtasks,
            inicio=td.get("inicio", "automatico"),
        ).model_dump()
        todas_tasks.append(task)
        novas.append(task)

    save_json("tasks.json", todas_tasks)

    # Dispara execução das tasks em background
    background_tasks.add_task(executar_tasks, campanha_id)

    return {"geradas": len(novas), "tasks": novas}


@app.get("/campanhas/{campanha_id}/tasks")
def listar_tasks_da_campanha(campanha_id: str):
    todas = load_json("tasks.json")
    return [t for t in todas if t["campanha_id"] == campanha_id]


@app.post("/campanhas/{campanha_id}/tasks")
async def adicionar_task(campanha_id: str, body: TaskAddRequest, background_tasks: BackgroundTasks):
    """Adiciona uma task manualmente a uma campanha existente."""
    campanhas = load_json("campanhas.json")
    campanha = next((c for c in campanhas if c["id"] == campanha_id), None)
    if not campanha:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")

    subtasks = [
        Subtask(
            titulo=s.titulo,
            descricao=s.descricao,
            agente=s.agente,
            requer_aprovacao=s.requer_aprovacao,
            instrucoes_extras=s.instrucoes_extras,
        ).model_dump()
        for s in body.subtasks
    ]

    task = Task(
        campanha_id=campanha_id,
        titulo=body.titulo,
        descricao=body.descricao,
        subtasks=subtasks,
        inicio=body.inicio,
    ).model_dump()

    todas = load_json("tasks.json")
    todas.append(task)
    save_json("tasks.json", todas)

    background_tasks.add_task(executar_tasks, campanha_id)

    return task


@app.post("/campanhas/{campanha_id}/tasks/{task_id}/iniciar")
async def iniciar_task(campanha_id: str, task_id: str, background_tasks: BackgroundTasks):
    """Inicia manualmente uma task que estava aguardando."""
    todas = load_json("tasks.json")
    task = next((t for t in todas if t["id"] == task_id and t["campanha_id"] == campanha_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task não encontrada")
    if task["status"] != "pendente":
        raise HTTPException(status_code=400, detail=f"Task não está pendente (status: {task['status']})")

    if task["subtasks"]:
        primeira = task["subtasks"][0]
        primeira["status"] = "executando"
        primeira["iniciado_em"] = datetime.now().isoformat()
        task["status"] = "executando"
        task["atualizado_em"] = datetime.now().isoformat()
        save_json("tasks.json", todas)
        background_tasks.add_task(executar_subtask, campanha_id, task_id, primeira["id"])

    return {"status": "iniciada", "task_id": task_id}


@app.delete("/campanhas/{campanha_id}/tasks/{task_id}")
def remover_task(campanha_id: str, task_id: str):
    todas = load_json("tasks.json")
    antes = len(todas)
    todas = [t for t in todas if not (t["campanha_id"] == campanha_id and t["id"] == task_id)]
    if len(todas) == antes:
        raise HTTPException(status_code=404, detail="Task não encontrada")
    save_json("tasks.json", todas)
    return {"status": "removida"}


@app.post("/campanhas/{campanha_id}/tasks/{task_id}/subtasks/{subtask_id}/aprovar")
async def aprovar_subtask(
    campanha_id: str, task_id: str, subtask_id: str,
    body: SubtaskApproval, background_tasks: BackgroundTasks
):
    """
    Aprova ou rejeita uma subtask. Se aprovada, dispara a próxima subtask automaticamente.
    """
    todas = load_json("tasks.json")
    task = next((t for t in todas if t["id"] == task_id and t["campanha_id"] == campanha_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task não encontrada")

    subtask = next((s for s in task["subtasks"] if s["id"] == subtask_id), None)
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask não encontrada")

    if subtask["status"] != "aguardando_aprovacao":
        raise HTTPException(status_code=400, detail=f"Subtask não está aguardando aprovação (status: {subtask['status']})")

    now = datetime.now().isoformat()

    if body.action == "approve":
        subtask["status"] = "aprovada"
        subtask["concluido_em"] = now

        # Encontra próxima subtask pendente
        idx = task["subtasks"].index(subtask)
        proxima = None
        for s in task["subtasks"][idx + 1:]:
            if s["status"] == "pendente":
                proxima = s
                break

        if proxima:
            proxima["status"] = "executando"
            proxima["iniciado_em"] = now
            task["status"] = "executando"
            background_tasks.add_task(executar_subtask, campanha_id, task_id, proxima["id"])
        else:
            # Todas subtasks concluídas
            task["status"] = "concluida"
            task["atualizado_em"] = now

    else:  # reject
        subtask["status"] = "rejeitada"
        subtask["feedback_rejeicao"] = body.feedback
        task["status"] = "aguardando_aprovacao"

    task["atualizado_em"] = now
    save_json("tasks.json", todas)

    return {
        "status": subtask["status"],
        "proxima_subtask": proxima["titulo"] if body.action == "approve" and proxima else None,
    }


# ─── Background: execução de tasks e subtasks ──────────────────────────────────

async def executar_tasks(campanha_id: str):
    """Inicia a primeira subtask de cada task com inicio=automatico (rodam em paralelo)."""
    import asyncio
    todas = load_json("tasks.json")
    tasks_da_campanha = [t for t in todas if t["campanha_id"] == campanha_id and t["status"] == "pendente" and t.get("inicio", "automatico") == "automatico"]

    agendadas = []
    for task in tasks_da_campanha:
        if task["subtasks"]:
            primeira = task["subtasks"][0]
            primeira["status"] = "executando"
            primeira["iniciado_em"] = datetime.now().isoformat()
            task["status"] = "executando"
            task["atualizado_em"] = datetime.now().isoformat()
            agendadas.append((campanha_id, task["id"], primeira["id"]))

    save_json("tasks.json", todas)

    # Executa todas as primeiras subtasks em paralelo
    await asyncio.gather(*[executar_subtask(c, t, s) for c, t, s in agendadas])


async def executar_subtask(campanha_id: str, task_id: str, subtask_id: str):
    """
    Executa uma subtask usando o agente responsável via OpenAI.
    Passa o contexto das subtasks anteriores concluídas da mesma task.
    """
    import asyncio
    from tools.agent_executor import executar_agente

    todas = load_json("tasks.json")
    task = next((t for t in todas if t["id"] == task_id), None)
    if not task:
        return

    subtask = next((s for s in task["subtasks"] if s["id"] == subtask_id), None)
    if not subtask:
        return

    now = datetime.now().isoformat()

    try:
        # Monta contexto das subtasks anteriores concluídas
        idx = next(i for i, s in enumerate(task["subtasks"]) if s["id"] == subtask_id)
        contexto_anterior = ""
        for s in task["subtasks"][:idx]:
            if s.get("output") and s["status"] in ("concluida", "aprovada"):
                titulo = s['titulo']
                agente = s['agente']
                output = s['output']
                contexto_anterior += f"### {titulo} ({agente}):\n{output}\n\n"

        # Monta instrução completa
        instrucao = subtask["descricao"]
        if subtask.get("instrucoes_extras"):
            extras = subtask["instrucoes_extras"]
            instrucao += f"\n\nInstruções adicionais: {extras}"

        # Executa o agente de verdade
        output = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: executar_agente(subtask["agente"], instrucao, contexto_anterior)
        )
        subtask["output"] = output

    except Exception as e:
        subtask["status"] = "erro"
        subtask["output"] = f"Erro na execução: {str(e)}"
        task["status"] = "erro"
        task["atualizado_em"] = now
        save_json("tasks.json", todas)
        return

    if subtask["requer_aprovacao"]:
        subtask["status"] = "aguardando_aprovacao"
        task["status"] = "aguardando_aprovacao"
    else:
        subtask["status"] = "concluida"
        subtask["concluido_em"] = now

        # Dispara próxima subtask automaticamente
        for s in task["subtasks"][idx + 1:]:
            if s["status"] == "pendente":
                s["status"] = "executando"
                s["iniciado_em"] = now
                save_json("tasks.json", todas)
                await executar_subtask(campanha_id, task_id, s["id"])
                return

        if all(s["status"] in ("concluida", "aprovada") for s in task["subtasks"]):
            task["status"] = "concluida"

    task["atualizado_em"] = now
    save_json("tasks.json", todas)
