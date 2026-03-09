import os
import json
from pathlib import Path
from crewai_tools import BaseTool
import openai


class BrandAssetReaderTool(BaseTool):
    name: str = "Brand Asset Reader"
    description: str = """
    Lê os assets de marca de um conto específico da Libbro.
    Use para obter o estilo visual, paleta de cores e referências
    antes de criar qualquer material visual.
    Input: nome do conto (slug)
    """

    def _run(self, conto_slug: str) -> str:
        assets_path = os.getenv("ASSETS_PATH", "../assets")
        conto_path = Path(assets_path) / "ilustracoes-contos" / conto_slug

        if not conto_path.exists():
            return f"Conto '{conto_slug}' não encontrado em {conto_path}. Contos disponíveis: {self._list_contos(assets_path)}"

        result = {}

        # Lê estilo.md
        estilo_file = conto_path / "estilo.md"
        if estilo_file.exists():
            result["estilo"] = estilo_file.read_text()

        # Lista referências
        refs_path = conto_path / "referencias"
        if refs_path.exists():
            result["referencias"] = [f.name for f in refs_path.iterdir() if f.is_file()]

        # Lista personagens
        personagens_path = conto_path / "personagens"
        if personagens_path.exists():
            result["personagens"] = [f.name for f in personagens_path.iterdir() if f.is_file()]

        return json.dumps(result, ensure_ascii=False, indent=2)

    def _list_contos(self, assets_path: str) -> str:
        contos_path = Path(assets_path) / "ilustracoes-contos"
        if not contos_path.exists():
            return "nenhum"
        return ", ".join([d.name for d in contos_path.iterdir() if d.is_dir()])


class ImageGeneratorTool(BaseTool):
    name: str = "Image Generator"
    description: str = """
    Gera imagens usando DALL-E 3 com base em um prompt detalhado.
    Input: JSON com 'prompt' (string) e 'size' (1024x1024, 1792x1024, ou 1024x1792)
    Retorna: URL da imagem gerada
    """

    def _run(self, input_json: str) -> str:
        try:
            data = json.loads(input_json)
            prompt = data.get("prompt", "")
            size = data.get("size", "1792x1024")

            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="hd",
                n=1,
            )
            return f"Imagem gerada: {response.data[0].url}\nPrompt revisado: {response.data[0].revised_prompt}"
        except Exception as e:
            return f"Erro ao gerar imagem: {str(e)}"


class BrandGuideReaderTool(BaseTool):
    name: str = "Brand Guide Reader"
    description: str = """
    Lê o guia de identidade visual da Libbro.
    Use antes de criar qualquer material visual para garantir
    consistência com a marca.
    """

    def _run(self, _: str = "") -> str:
        assets_path = os.getenv("ASSETS_PATH", "../assets")
        guide_path = Path(assets_path) / "identidade-visual" / "guia-de-marca.md"

        if not guide_path.exists():
            return "Guia de marca ainda não configurado. Acesse o dashboard para fazer upload."

        return guide_path.read_text()
