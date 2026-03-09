"""
Geração de voz — ElevenLabs
"""

import os
import httpx
from pathlib import Path
from datetime import datetime


ELEVENLABS_API = "https://api.elevenlabs.io/v1"


class VoiceGenerator:

    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.output_dir = Path(os.getenv("ASSETS_PATH", "../assets")) / "gerados" / "audio"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Voz padrão — pode ser trocada por uma voz customizada da Libbro
        self.default_voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

    def gerar_narração(self, texto: str, voice_id: str = None, stability: float = 0.5, similarity: float = 0.75) -> dict:
        """
        Gera narração em áudio a partir de texto.
        """
        if not self.api_key:
            return {"status": "error", "error": "ELEVENLABS_API_KEY não configurada"}

        vid = voice_id or self.default_voice_id

        try:
            response = httpx.post(
                f"{ELEVENLABS_API}/text-to-speech/{vid}",
                headers={
                    "xi-api-key": self.api_key,
                    "Content-Type": "application/json",
                },
                json={
                    "text": texto,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": stability,
                        "similarity_boost": similarity,
                    },
                },
                timeout=60,
            )

            if response.status_code == 200:
                filename = f"narr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                filepath = self.output_dir / filename
                filepath.write_bytes(response.content)
                return {
                    "status": "ok",
                    "local": str(filepath),
                    "duracao_estimada": len(texto.split()) / 2.5,  # ~2.5 palavras/segundo
                    "model": "eleven_multilingual_v2",
                }
            else:
                return {"status": "error", "error": response.text}

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def listar_vozes(self) -> list:
        """
        Lista vozes disponíveis na conta ElevenLabs.
        """
        if not self.api_key:
            return []
        try:
            response = httpx.get(
                f"{ELEVENLABS_API}/voices",
                headers={"xi-api-key": self.api_key},
                timeout=15,
            )
            voices = response.json().get("voices", [])
            return [{"id": v["voice_id"], "nome": v["name"], "categoria": v.get("category")} for v in voices]
        except Exception:
            return []
