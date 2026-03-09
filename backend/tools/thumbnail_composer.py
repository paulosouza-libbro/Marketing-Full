"""
Composição de thumbnails — adiciona logo do conto sobre a imagem gerada
"""

import os
from pathlib import Path
from PIL import Image, ImageFilter
from datetime import datetime


class ThumbnailComposer:

    YOUTUBE_SIZE = (1280, 720)

    def __init__(self):
        self.assets_path = Path(os.getenv("ASSETS_PATH", "../assets"))
        self.output_dir = self.assets_path / "gerados" / "thumbnails"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def compor_thumbnail(
        self,
        imagem_base_path: str,
        conto_slug: str,
        posicao_logo: str = "bottom-right",  # top-left | top-right | bottom-left | bottom-right | bottom-center
        logo_escala: float = 0.40,           # % da largura da thumbnail
        margem: int = 30,
    ) -> dict:
        """
        Compõe thumbnail final: imagem base + logo do conto.
        Salva em /assets/gerados/thumbnails/
        """
        try:
            # Carrega imagem base
            base = Image.open(imagem_base_path).convert("RGBA")
            base = base.resize(self.YOUTUBE_SIZE, Image.LANCZOS)

            # Carrega logo do conto
            logo_path = self.assets_path / "ilustracoes-contos" / conto_slug / f"logo-{conto_slug}.png"
            if not logo_path.exists():
                return {"status": "error", "error": f"Logo não encontrada em {logo_path}"}

            logo = Image.open(logo_path).convert("RGBA")

            # Redimensiona logo proporcionalmente
            logo_w = int(self.YOUTUBE_SIZE[0] * logo_escala)
            logo_h = int(logo.height * (logo_w / logo.width))
            logo = logo.resize((logo_w, logo_h), Image.LANCZOS)

            # Posiciona logo
            x, y = self._calcular_posicao(posicao_logo, logo_w, logo_h, margem)

            # Suaviza bordas da logo com leve sombra
            logo_sombra = self._criar_sombra(logo)
            base.paste(logo_sombra, (x + 4, y + 4), logo_sombra)
            base.paste(logo, (x, y), logo)

            # Salva resultado final
            filename = f"thumb_{conto_slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = self.output_dir / filename
            base_rgb = base.convert("RGB")
            base_rgb.save(filepath, "PNG", quality=95)

            return {
                "status": "ok",
                "local": str(filepath),
                "tamanho": f"{self.YOUTUBE_SIZE[0]}x{self.YOUTUBE_SIZE[1]}",
                "logo_posicao": posicao_logo,
                "conto": conto_slug,
            }

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _calcular_posicao(self, posicao: str, logo_w: int, logo_h: int, margem: int):
        W, H = self.YOUTUBE_SIZE
        posicoes = {
            "top-left":      (margem, margem),
            "top-right":     (W - logo_w - margem, margem),
            "bottom-left":   (margem, H - logo_h - margem),
            "bottom-right":  (W - logo_w - margem, H - logo_h - margem),
            "bottom-center": ((W - logo_w) // 2, H - logo_h - margem),
            "top-center":    ((W - logo_w) // 2, margem),
        }
        return posicoes.get(posicao, posicoes["bottom-right"])

    def _criar_sombra(self, logo: Image.Image) -> Image.Image:
        sombra = Image.new("RGBA", logo.size, (0, 0, 0, 0))
        r, g, b, a = logo.split()
        sombra_alpha = a.point(lambda p: int(p * 0.5))
        sombra_preta = Image.new("RGBA", logo.size, (0, 0, 0, 255))
        sombra.paste(sombra_preta, mask=sombra_alpha)
        return sombra.filter(ImageFilter.GaussianBlur(radius=6))
