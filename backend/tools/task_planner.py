"""
TaskPlanner — usa o Diretor (LLM) para gerar tasks de uma campanha a partir do briefing.
"""
import json
import os
from openai import OpenAI


SYSTEM_PROMPT = """Você é o Diretor de Campanha da Libbro — produtora de conteúdo literário
premium para crianças de 3 a 8 anos. Você lê um briefing e gera as tasks necessárias.

AGENTES DISPONÍVEIS:
- pesquisador_conto: pesquisa origens, versões e curiosidades do conto
- copywriter: títulos, descrições, roteiros, legendas, posts
- designer: thumbnails, posts visuais, artes
- seo_youtube: tags, palavras-chave, horário ideal, SEO
- social_media: adaptação de conteúdo para redes sociais
- produtor_video: montagem de vídeo
- analista: métricas e relatórios

ESCOPO DO MARKETING:
O vídeo (animação, narração, trilha, edição) é produzido pela FÁBRICA — outra área da empresa.
O marketing NUNCA cria roteiro, narração, animação ou edição de vídeo.
O marketing é responsável por: thumbnail, título, descrição, SEO, publicação, posts em redes sociais, e-mail marketing.

REGRAS:
- Tasks de canais diferentes rodam em PARALELO
- Subtasks dentro de uma task são SEQUENCIAIS
- Conteúdo que vai ao ar SEMPRE tem requer_aprovacao: true
- Pesquisa e análise têm requer_aprovacao: false
- Sempre inclua uma subtask de pesquisador_conto antes do copywriter quando houver copy
- NUNCA crie tasks de roteiro de vídeo, narração, animação ou edição

Retorne SOMENTE um JSON válido no formato:
{
  "tasks": [
    {
      "titulo": "string",
      "descricao": "string",
      "subtasks": [
        {
          "titulo": "string",
          "descricao": "string (instrução clara para o agente)",
          "agente": "string (id do agente)",
          "requer_aprovacao": true|false
        }
      ]
    }
  ]
}"""


def planejar_tasks(briefing: str, conto: str, canais: list) -> list:
    """
    Usa o LLM para gerar tasks a partir do briefing.
    Retorna lista de dicts prontos para criar Task objects.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    canais_str = ", ".join(canais)
    user_prompt = f"""
Campanha para o conto: {conto}
Canais: {canais_str}

Briefing:
{briefing}

Gere todas as tasks necessárias para executar esta campanha.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )

    result = json.loads(response.choices[0].message.content)
    return result.get("tasks", [])
