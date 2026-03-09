import os
from crewai_tools import BaseTool


class YouTubeTrendsTool(BaseTool):
    name: str = "YouTube Trends Researcher"
    description: str = """
    Pesquisa tendências e palavras-chave no YouTube para um nicho específico.
    Input: nicho ou tema (ex: 'contos infantis', 'literatura brasileira')
    """

    def _run(self, nicho: str) -> str:
        # TODO: Integrar com YouTube Data API v3
        return f"""
        [YouTube Trends - {nicho}]
        ⚠️  Integração com YouTube Data API pendente.
        Configure YOUTUBE_API_KEY no .env para ativar esta ferramenta.

        Por enquanto, use suas capacidades de análise para sugerir
        palavras-chave baseadas no nicho: {nicho}
        """


class WebSearchTool(BaseTool):
    name: str = "Web Search"
    description: str = """
    Pesquisa na web por tendências, concorrentes e referências de marketing.
    Input: query de pesquisa
    """

    def _run(self, query: str) -> str:
        # TODO: Integrar com Brave Search API ou similar
        return f"""
        [Web Search - {query}]
        ⚠️  Integração com Search API pendente.
        Configure SEARCH_API_KEY no .env para ativar esta ferramenta.
        """
