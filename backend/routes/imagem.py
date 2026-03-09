"""Rotas de geração de imagem"""
from fastapi import APIRouter
from pathlib import Path
import os

router = APIRouter(prefix="", tags=["imagens"])

@router.post("/gerar/imagem/freepik")
async def gerar_imagem_freepik(body: dict):
    from tools.freepik_generator import FreepikGenerator
    from tools.image_generator import ImageGenerator

    gen = FreepikGenerator()
    conto = body.get("conto", "")
    prompt_base = body.get("prompt", "")

    if conto:
        assets = Path("../assets/ilustracoes-contos") / conto / "estilo.md"
        if assets.exists():
            img_gen = ImageGenerator()
            prompt = img_gen.construir_prompt_conto(assets.read_text(), prompt_base, body.get("formato", "thumbnail"))
        else:
            prompt = prompt_base
    else:
        prompt = prompt_base

    return gen.gerar_imagem(prompt, body.get("style", "illustration"), body.get("ratio", "16:9"))


@router.get("/freepik/buscar")
async def buscar_freepik(q: str, tipo: str = "photo", limite: int = 10):
    from tools.freepik_generator import FreepikGenerator
    return FreepikGenerator().buscar_assets(q, tipo, limite)
