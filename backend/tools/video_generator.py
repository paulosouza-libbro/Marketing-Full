"""
Geração de vídeo — Runway ML + Pika Labs
"""

import os
import time
import httpx
from pathlib import Path
from datetime import datetime


class VideoGenerator:

    def __init__(self):
        self.runway_key = os.getenv("RUNWAY_API_KEY")
        self.pika_key = os.getenv("PIKA_API_KEY")
        self.output_dir = Path(os.getenv("ASSETS_PATH", "../assets")) / "gerados" / "videos"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def gerar_runway(self, prompt: str, image_url: str = None, duration: int = 4) -> dict:
        """
        Gera vídeo com Runway ML Gen-3.
        image_url: imagem de referência (opcional, para img-to-video)
        duration: duração em segundos (4 ou 8)
        """
        if not self.runway_key:
            return {"status": "error", "error": "RUNWAY_API_KEY não configurada"}

        try:
            headers = {
                "Authorization": f"Bearer {self.runway_key}",
                "Content-Type": "application/json",
                "X-Runway-Version": "2024-11-06",
            }

            payload = {
                "promptText": prompt,
                "model": "gen3a_turbo",
                "duration": duration,
                "ratio": "1280:720",
            }

            if image_url:
                payload["promptImage"] = image_url

            # Cria o job
            response = httpx.post(
                "https://api.dev.runwayml.com/v1/image_to_video",
                headers=headers,
                json=payload,
                timeout=30,
            )

            if response.status_code not in [200, 201]:
                return {"status": "error", "error": response.text}

            task_id = response.json().get("id")

            # Polling do resultado
            return self._poll_runway_task(task_id, headers)

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _poll_runway_task(self, task_id: str, headers: dict, max_attempts: int = 30) -> dict:
        for _ in range(max_attempts):
            time.sleep(10)
            try:
                response = httpx.get(
                    f"https://api.dev.runwayml.com/v1/tasks/{task_id}",
                    headers=headers,
                    timeout=15,
                )
                data = response.json()
                status = data.get("status")

                if status == "SUCCEEDED":
                    video_url = data.get("output", [None])[0]
                    filename = f"runway_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
                    filepath = self.output_dir / filename
                    self._download_video(video_url, filepath)
                    return {"status": "ok", "url": video_url, "local": str(filepath), "model": "runway-gen3"}

                elif status == "FAILED":
                    return {"status": "error", "error": data.get("failure", "Geração falhou")}

            except Exception as e:
                return {"status": "error", "error": str(e)}

        return {"status": "error", "error": "Timeout — vídeo demorou demais para gerar"}

    def _download_video(self, url: str, path: Path):
        try:
            response = httpx.get(url, timeout=120, follow_redirects=True)
            path.write_bytes(response.content)
        except Exception:
            pass

    def criar_storyboard(self, roteiro: str, cenas: list) -> dict:
        """
        Cria estrutura de storyboard a partir de roteiro e lista de cenas.
        cenas: [{"descricao": str, "duracao": int, "tipo": str}]
        """
        storyboard = {
            "roteiro": roteiro,
            "total_cenas": len(cenas),
            "duracao_total": sum(c.get("duracao", 4) for c in cenas),
            "cenas": [
                {
                    "numero": i + 1,
                    "descricao": c["descricao"],
                    "duracao": c.get("duracao", 4),
                    "tipo": c.get("tipo", "gerado"),  # gerado | animado | texto
                    "prompt_video": f"Cinematic scene: {c['descricao']}, smooth camera movement, professional lighting",
                    "status": "pendente",
                }
                for i, c in enumerate(cenas)
            ],
        }
        return storyboard
