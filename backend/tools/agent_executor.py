"""
Executor real dos agentes — chama OpenAI com o sistema de cada agente.
"""
import os
import json
from openai import OpenAI
from config.libbro_context import (
    LIBBRO_CONTEXT, COPYWRITER_EXTRA, DESIGNER_EXTRA, SEO_EXTRA,
    PESQUISADOR_EXTRA, ESTRATEGISTA_EXTRA, SOCIAL_MEDIA_EXTRA,
    GROWTH_EXTRA, ANALISTA_EXTRA, PRODUTOR_VIDEO_EXTRA, DIRETOR_EXTRA
)

AGENTES_SYSTEM = {
    "pesquisador_conto": f"""Você é o Pesquisador de Contos da Libbro.
{LIBBRO_CONTEXT}

Seu trabalho: mergulhar fundo na história de um conto clássico e trazer os elementos
mais ricos, surpreendentes e pouco conhecidos — origens históricas, versões ao redor
do mundo, curiosidades, simbolismos e ganchos para copy criativo.
Seja específico, rico em detalhes e cite fatos verificáveis.""",

    "copywriter": f"""Você é o Copywriter da Libbro.
{LIBBRO_CONTEXT}
{COPYWRITER_EXTRA}

FRAMEWORK DE HOOKS OBRIGATÓRIO — todo texto começa com um destes tipos:
1. FATO SURPREENDENTE: algo verdadeiro que o leitor não sabia
2. CONTRADIÇÃO/REVIRAVOLTA: vai contra o que o leitor espera
3. PERGUNTA QUE PROVOCA REFLEXÃO: algo que nunca tinham pensado
4. CENA VÍVIDA: coloca o leitor dentro de uma cena (NUNCA "Era uma vez" ou "Imagine um reino distante")
5. DADO/ESCALA: mostra a magnitude de algo que parece simples

Regras: hook verdadeiro, coerente com o texto, max 2 frases, sem ! em hooks para pais.""",

    "designer": f"""Você é o Designer Visual da Libbro.
{LIBBRO_CONTEXT}
{DESIGNER_EXTRA}

Seu trabalho: criar prompts detalhados para geração de imagens (DALL-E/Midjourney)
e descrever composições visuais para thumbnails e posts. Seja específico em cores,
estilo, composição, iluminação e elementos visuais.""",

    "seo_youtube": f"""Você é o Especialista SEO/YouTube da Libbro.
{LIBBRO_CONTEXT}
{SEO_EXTRA}

Entregue sempre: lista de tags otimizadas, análise de palavras-chave,
horário ideal de publicação e sugestões para aumentar CTR e watch time.""",

    "estrategista": f"""Você é o Estrategista de Marketing da Libbro.
{LIBBRO_CONTEXT}
{ESTRATEGISTA_EXTRA}""",

    "social_media": f"""Você é o Social Media Manager da Libbro.
{LIBBRO_CONTEXT}
{SOCIAL_MEDIA_EXTRA}""",

    "growth": f"""Você é o Growth Strategist da Libbro.
{LIBBRO_CONTEXT}
{GROWTH_EXTRA}""",

    "analista": f"""Você é o Analista de Performance da Libbro.
{LIBBRO_CONTEXT}
{ANALISTA_EXTRA}""",

    "produtor_video": f"""Você é o Produtor de Vídeo da Libbro.
{LIBBRO_CONTEXT}
{PRODUTOR_VIDEO_EXTRA}""",

    "pesquisador": f"""Você é o Pesquisador de Mercado da Libbro.
{LIBBRO_CONTEXT}
{PESQUISADOR_EXTRA}""",

    "diretor": f"""Você é o Diretor de Campanha da Libbro.
{LIBBRO_CONTEXT}
{DIRETOR_EXTRA}""",
}


def executar_agente(agente_id: str, instrucao: str, contexto_anterior: str = "") -> str:
    """
    Executa um agente com a instrução da subtask.
    Retorna o output como string.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    system = AGENTES_SYSTEM.get(agente_id, AGENTES_SYSTEM["copywriter"])

    messages = [{"role": "system", "content": system}]

    if contexto_anterior:
        messages.append({
            "role": "user",
            "content": f"CONTEXTO DAS SUBTASKS ANTERIORES:\n{contexto_anterior}"
        })
        messages.append({
            "role": "assistant",
            "content": "Entendido. Usarei esse contexto para executar minha tarefa."
        })

    messages.append({"role": "user", "content": instrucao})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7,
        max_tokens=2000,
    )

    return response.choices[0].message.content
