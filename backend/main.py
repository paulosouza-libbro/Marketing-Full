"""
Libbro Marketing App — Ponto de entrada principal

Uso:
    python main.py --briefing "Quero divulgar o conto X no YouTube" --conto "nome-do-conto"
"""

import argparse
from crewai import Crew, Process
from langchain_openai import ChatOpenAI

from agents.diretor import create_diretor
from agents.pesquisador import create_pesquisador
from agents.estrategista import create_estrategista
from agents.copywriter import create_copywriter
from agents.designer import create_designer
from agents.produtor_video import create_produtor_video
from agents.seo_youtube import create_seo_youtube
from agents.social_media import create_social_media
from agents.analista import create_analista
from tasks.tasks import (
    task_briefing_analysis,
    task_market_research,
    task_content_strategy,
    task_copy_creation,
    task_visual_creation,
    task_seo_optimization,
)
from config.settings import OPENAI_API_KEY, ASSETS_PATH

import os
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY or ""


def run_campaign(briefing: str, conto: str):
    print(f"\n🚀 Libbro Marketing App")
    print(f"📋 Briefing: {briefing}")
    print(f"📖 Conto: {conto}")
    print("=" * 60)

    # LLM padrão
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

    # Instancia agentes
    diretor = create_diretor(llm)
    pesquisador = create_pesquisador(llm)
    estrategista = create_estrategista(llm)
    copywriter = create_copywriter(llm)
    designer = create_designer(llm)
    seo = create_seo_youtube(llm)

    # Define tarefas (Fase 1 — MVP)
    t_briefing = task_briefing_analysis(diretor, briefing, conto)
    t_pesquisa = task_market_research(pesquisador, conto, briefing)
    t_estrategia = task_content_strategy(estrategista, "{t_pesquisa output}", conto)
    t_copy = task_copy_creation(copywriter, "{t_estrategia output}", conto, "vídeo YouTube")
    t_visual = task_visual_creation(designer, conto, "thumbnail YouTube", ASSETS_PATH)
    t_seo = task_seo_optimization(seo, "{título}", "{descrição}", [])

    # Monta a crew
    crew = Crew(
        agents=[diretor, pesquisador, estrategista, copywriter, designer, seo],
        tasks=[t_briefing, t_pesquisa, t_estrategia, t_copy, t_visual, t_seo],
        process=Process.sequential,
        verbose=True,
    )

    print("\n▶️  Iniciando a equipe...\n")
    result = crew.kickoff()

    print("\n" + "=" * 60)
    print("✅ CAMPANHA CRIADA — AGUARDANDO APROVAÇÃO")
    print("=" * 60)
    print("\n⚠️  Todo conteúdo criado precisa de aprovação antes de publicar.")
    print("   Acesse o dashboard para revisar e aprovar.\n")
    print(result)

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Libbro Marketing App")
    parser.add_argument("--briefing", required=True, help="Briefing da campanha")
    parser.add_argument("--conto", required=True, help="Slug do conto (ex: o-gato-curioso)")
    args = parser.parse_args()

    run_campaign(args.briefing, args.conto)
