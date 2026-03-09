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
    allow_origins=["http://localhost:3000", "https://*.railway.app", "https://*.vercel.app"],
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
from routes.imagem import router as imagem_router
app.include_router(imagem_router)


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
