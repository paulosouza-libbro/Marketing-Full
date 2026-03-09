"""
Geração de imagens — DALL-E 3 + Stable Diffusion
"""

import os
import httpx
import base64
from pathlib import Path
from datetime import datetime
import openai


class ImageGenerator:

    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.stability_key = os.getenv("STABILITY_API_KEY")
        self.output_dir = Path(os.getenv("ASSETS_PATH", "../assets")) / "gerados" / "imagens"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def gerar_dalle(self, prompt: str, size: str = "1792x1024", quality: str = "hd") -> dict:
        """
        Gera imagem com DALL-E 3.
        size: "1024x1024" | "1792x1024" | "1024x1792"
        """
        try:
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                n=1,
                response_format="url",
            )
            url = response.data[0].url
            revised_prompt = response.data[0].revised_prompt

            # Salva localmente
            filename = f"dalle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self._download_image(url, self.output_dir / filename)

            return {
                "status": "ok",
                "url": url,
                "local": str(self.output_dir / filename),
                "revised_prompt": revised_prompt,
                "model": "dall-e-3",
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def gerar_stability(self, prompt: str, negative_prompt: str = "", width: int = 1344, height: int = 768) -> dict:
        """
        Gera imagem com Stable Diffusion (Stability AI).
        """
        if not self.stability_key:
            return {"status": "error", "error": "STABILITY_API_KEY não configurada"}

        try:
            response = httpx.post(
                "https://api.stability.ai/v2beta/stable-image/generate/ultra",
                headers={
                    "authorization": f"Bearer {self.stability_key}",
                    "accept": "image/*",
                },
                data={
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "aspect_ratio": "16:9",
                    "output_format": "png",
                },
                timeout=60,
            )

            if response.status_code == 200:
                filename = f"stability_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                filepath = self.output_dir / filename
                filepath.write_bytes(response.content)
                return {
                    "status": "ok",
                    "local": str(filepath),
                    "model": "stable-diffusion-ultra",
                }
            else:
                return {"status": "error", "error": response.text}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _download_image(self, url: str, path: Path):
        try:
            response = httpx.get(url, timeout=30)
            path.write_bytes(response.content)
        except Exception:
            pass

    def construir_prompt_conto(self, estilo_md: str, descricao_cena: str, formato: str = "thumbnail") -> str:
        """
        Constrói prompt otimizado baseado no estilo do conto.
        """
        formato_specs = {
            "thumbnail": "YouTube thumbnail, 16:9, high contrast, eye-catching",
            "post_instagram": "Instagram post, square 1:1, vibrant colors",
            "story": "Instagram story, vertical 9:16, mobile-optimized",
            "banner": "wide banner, 16:9, cinematic composition",
        }

        spec = formato_specs.get(formato, "digital illustration")

        # Extrai elementos chave do estilo.md
        prompt = f"""
{descricao_cena}

Style guidelines from brand: {estilo_md[:500]}

Format: {spec}
Quality: highly detailed, professional digital art, 8k resolution
"""
        return prompt.strip()
