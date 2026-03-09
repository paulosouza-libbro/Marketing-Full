"""
Publicação no YouTube — YouTube Data API v3
APROVAÇÃO HUMANA OBRIGATÓRIA antes de qualquer publicação.
"""

import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CREDENTIALS_FILE = Path(os.getenv("YOUTUBE_CREDENTIALS_FILE", "config/youtube_credentials.json"))
TOKEN_FILE = Path("config/youtube_token.json")


class YouTubePublisher:

    def __init__(self):
        self.youtube = None
        self._autenticar()

    def _autenticar(self):
        try:
            creds = None
            if TOKEN_FILE.exists():
                creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

            if not creds or not creds.valid:
                if not CREDENTIALS_FILE.exists():
                    print("⚠️  YouTube credentials não configuradas. Configure YOUTUBE_CREDENTIALS_FILE.")
                    return
                flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
                creds = flow.run_local_server(port=0)
                TOKEN_FILE.write_text(creds.to_json())

            self.youtube = build("youtube", "v3", credentials=creds)
        except Exception as e:
            print(f"⚠️  Erro na autenticação YouTube: {e}")

    def publicar_video(
        self,
        video_path: str,
        titulo: str,
        descricao: str,
        tags: list,
        thumbnail_path: str = None,
        privacidade: str = "private",  # sempre private por padrão — aprovação muda para public
    ) -> dict:
        """
        Faz upload de vídeo no YouTube.
        privacidade: "private" | "unlisted" | "public"
        ATENÇÃO: só chamar após aprovação humana explícita.
        """
        if not self.youtube:
            return {"status": "error", "error": "YouTube não autenticado"}

        try:
            body = {
                "snippet": {
                    "title": titulo,
                    "description": descricao,
                    "tags": tags,
                    "categoryId": "22",  # People & Blogs
                },
                "status": {
                    "privacyStatus": privacidade,
                    "selfDeclaredMadeForKids": False,
                },
            }

            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
            request = self.youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media,
            )

            response = None
            while response is None:
                status, response = request.next_chunk()

            video_id = response.get("id")

            # Upload da thumbnail
            if thumbnail_path and video_id:
                self._set_thumbnail(video_id, thumbnail_path)

            return {
                "status": "ok",
                "video_id": video_id,
                "url": f"https://youtube.com/watch?v={video_id}",
                "privacidade": privacidade,
            }

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _set_thumbnail(self, video_id: str, thumbnail_path: str):
        try:
            self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path),
            ).execute()
        except Exception as e:
            print(f"⚠️  Erro ao definir thumbnail: {e}")

    def agendar_publicacao(self, video_id: str, publish_at: str) -> dict:
        """
        Agenda publicação de vídeo já enviado.
        publish_at: datetime em ISO 8601 (ex: "2025-03-15T15:00:00Z")
        """
        if not self.youtube:
            return {"status": "error", "error": "YouTube não autenticado"}
        try:
            self.youtube.videos().update(
                part="status",
                body={
                    "id": video_id,
                    "status": {
                        "privacyStatus": "private",
                        "publishAt": publish_at,
                    },
                },
            ).execute()
            return {"status": "ok", "agendado_para": publish_at}
        except Exception as e:
            return {"status": "error", "error": str(e)}
