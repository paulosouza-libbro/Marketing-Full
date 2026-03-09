"""
Geração de imagens — Freepik AI Image Generator
"""

import os
import httpx
from pathlib import Path
from datetime import datetime


FREEPIK_API = "https://api.freepik.com/v1"


class FreepikGenerator:

    def __init__(self):
        self.api_key = os.getenv("FREEPIK_API_KEY")
        self.output_dir = Path(os.getenv("ASSETS_PATH", "../assets")) / "gerados" / "imagens"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def gerar_imagem(self, prompt: str, style: str = "photo", ratio: str = "16:9") -> dict:
        """
        Gera imagem com Freepik AI.
        style: photo | digital-art | illustration | anime | 3d
        ratio: 1:1 | 16:9 | 9:16 | 4:3
        """
        if not self.api_key:
            return {"status": "error", "error": "FREEPIK_API_KEY não configurada"}

        try:
            response = httpx.post(
                f"{FREEPIK_API}/ai/text-to-image",
                headers={
                    "x-freepik-api-key": self.api_key,
                    "Content-Type": "application/json",
                    "Accept-Language": "pt-BR",
                },
                json={
                    "prompt": prompt,
                    "num_images": 1,
                    "image": {
                        "size": self._ratio_to_size(ratio),
                    },
                    "styling": {
                        "style": style,
                    },
                },
                timeout=60,
            )

            if response.status_code in [200, 201]:
                data = response.json()
                images = data.get("data", [])
                if images:
                    img_url = images[0].get("url") or images[0].get("base64")
                    filename = f"freepik_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    filepath = self.output_dir / filename

                    if img_url and img_url.startswith("http"):
                        self._download_image(img_url, filepath)
                        return {"status": "ok", "url": img_url, "local": str(filepath), "model": "freepik-ai"}
                    elif img_url:
                        import base64
                        filepath.write_bytes(base64.b64decode(img_url))
                        return {"status": "ok", "local": str(filepath), "model": "freepik-ai"}

            return {"status": "error", "error": f"HTTP {response.status_code}: {response.text[:200]}"}

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _ratio_to_size(self, ratio: str) -> dict:
        sizes = {
            "16:9": {"width": 1344, "height": 768},
            "9:16": {"width": 768, "height": 1344},
            "1:1":  {"width": 1024, "height": 1024},
            "4:3":  {"width": 1152, "height": 864},
        }
        return sizes.get(ratio, sizes["16:9"])

    def _download_image(self, url: str, path: Path):
        try:
            r = httpx.get(url, timeout=30, follow_redirects=True)
            path.write_bytes(r.content)
        except Exception:
            pass

    def buscar_assets(self, query: str, tipo: str = "photo", limite: int = 10) -> list:
        """
        Busca assets no acervo do Freepik.
        tipo: photo | vector | psd
        """
        if not self.api_key:
            return []
        try:
            response = httpx.get(
                f"{FREEPIK_API}/resources",
                headers={"x-freepik-api-key": self.api_key},
                params={"locale": "pt_BR", "page": 1, "limit": limite, "filters[content_type]": tipo, "term": query},
                timeout=15,
            )
            if response.status_code == 200:
                return response.json().get("data", [])
            return []
        except Exception:
            return []
