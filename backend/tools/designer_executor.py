"""
Executor especializado para o agente Designer.
Fluxo: gera prompt DALL-E via LLM → gera imagem → compõe logo → retorna resultado.
"""
import os
import json
from openai import OpenAI
from pathlib import Path
from config.libbro_context import LIBBRO_CONTEXT, DESIGNER_EXTRA

ASSETS_PATH = Path(os.getenv("ASSETS_PATH", "../assets"))

FORMATO_MAP = {
    "thumbnail": {"size": "1792x1024", "desc": "thumbnail YouTube 1280x720"},
    "post_instagram": {"size": "1024x1024", "desc": "post Instagram quadrado"},
    "story": {"size": "1024x1792", "desc": "story vertical 9:16"},
    "banner": {"size": "1792x1024", "desc": "banner horizontal"},
}

DESIGNER_SYSTEM = f"""Você é o Designer Visual da Libbro.
{LIBBRO_CONTEXT}
{DESIGNER_EXTRA}

Sua tarefa: receber uma instrução e gerar um prompt detalhado para DALL-E 3.

O prompt deve especificar:
- Estilo: aquarela digital clássica europeia, influência Arthur Rackham / Edmund Dulac
- Personagens: descrição física precisa (baseada no estilo do conto)
- Composição: posição dos elementos, enquadramento
- Iluminação: suave, etérea, mágica
- Paleta de cores: específica para o conto
- Atmosfera: encantada, premium, como livro ilustrado
- Formato: adequado ao destino (thumbnail YouTube, post Instagram, etc.)

NUNCA gere: cartoon, anime, flat design, estilo Disney, cores néon, personagens deformados.
Retorne APENAS o prompt em inglês, sem explicações adicionais."""


def detectar_formato(instrucao: str) -> str:
    instrucao_lower = instrucao.lower()
    if "thumbnail" in instrucao_lower or "youtube" in instrucao_lower:
        return "thumbnail"
    elif "story" in instrucao_lower or "stories" in instrucao_lower:
        return "story"
    elif "instagram" in instrucao_lower or "post" in instrucao_lower:
        return "post_instagram"
    return "thumbnail"


def executar_designer(instrucao: str, conto_slug: str, contexto_anterior: str = "") -> dict:
    """
    Executa o agente Designer completo:
    1. Gera prompt DALL-E via LLM
    2. Gera imagem com DALL-E 3
    3. Compõe logo do conto (se existir)
    4. Retorna dict com texto descritivo + URL da imagem gerada
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=120)

    formato = detectar_formato(instrucao)
    fmt = FORMATO_MAP[formato]

    # Carrega estilo do conto
    estilo_path = ASSETS_PATH / "ilustracoes-contos" / conto_slug / "estilo.md"
    estilo = estilo_path.read_text() if estilo_path.exists() else ""

    # PASSO 1: Gera prompt DALL-E via LLM
    messages = [{"role": "system", "content": DESIGNER_SYSTEM}]
    if contexto_anterior:
        messages.append({"role": "user", "content": f"CONTEXTO:\n{contexto_anterior}"})
        messages.append({"role": "assistant", "content": "Entendido."})

    prompt_request = f"""Instrução: {instrucao}

Estilo do conto {conto_slug}:
{estilo}

Formato destino: {fmt['desc']}
Gere o prompt DALL-E em inglês para esta imagem."""

    messages.append({"role": "user", "content": prompt_request})

    prompt_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7,
        max_tokens=600,
    )
    dalle_prompt = prompt_response.choices[0].message.content.strip()

    # PASSO 2: Gera imagem com DALL-E 3
    image_response = client.images.generate(
        model="dall-e-3",
        prompt=dalle_prompt,
        size=fmt["size"],
        quality="hd",
        n=1,
    )
    image_url = image_response.data[0].url

    # PASSO 3: Baixa e salva a imagem
    import httpx
    from datetime import datetime

    output_dir = ASSETS_PATH / "gerados" / "thumbnails"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_path = output_dir / f"{formato}_{conto_slug}_{timestamp}.png"

    img_bytes = httpx.get(image_url, timeout=30).content
    local_path.write_bytes(img_bytes)

    # PASSO 4: Compõe logo (se existir)
    logo_path = ASSETS_PATH / "ilustracoes-contos" / conto_slug / f"logo-{conto_slug}.png"
    thumbnail_final = str(local_path)

    if logo_path.exists() and formato == "thumbnail":
        from tools.thumbnail_composer import ThumbnailComposer
        composer = ThumbnailComposer()
        result = composer.compor_thumbnail(
            imagem_base_path=str(local_path),
            conto_slug=conto_slug,
            posicao_logo="bottom-center",
            logo_escala=0.44,
        )
        if result.get("status") == "ok":
            thumbnail_final = result["local"]

    return {
        "tipo": "imagem",
        "formato": formato,
        "prompt_usado": dalle_prompt,
        "imagem_url": image_url,
        "imagem_local": thumbnail_final,
        "logo_aplicada": logo_path.exists() and formato == "thumbnail",
        "descricao": f"Imagem gerada para {fmt['desc']} do conto {conto_slug}.",
    }
