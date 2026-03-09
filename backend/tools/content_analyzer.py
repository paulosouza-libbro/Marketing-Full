"""
Análise de performance — YouTube Analytics + GA4
"""

import os
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


class YouTubeAnalyzer:

    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = None
        self.analytics = None
        self._conectar()

    def _conectar(self):
        try:
            token_file = "config/youtube_token.json"
            if os.path.exists(token_file):
                creds = Credentials.from_authorized_user_file(token_file)
                self.youtube = build("youtube", "v3", credentials=creds)
                self.analytics = build("youtubeAnalytics", "v2", credentials=creds)
        except Exception as e:
            print(f"⚠️  YouTube Analytics não conectado: {e}")

    def metricas_video(self, video_id: str, dias: int = 30) -> dict:
        """
        Retorna métricas de um vídeo específico.
        """
        if not self.analytics:
            return {"status": "error", "error": "YouTube Analytics não autenticado"}

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d")

        try:
            response = self.analytics.reports().query(
                ids="channel==MINE",
                startDate=start_date,
                endDate=end_date,
                metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes,comments",
                dimensions="video",
                filters=f"video=={video_id}",
            ).execute()

            rows = response.get("rows", [])
            if not rows:
                return {"status": "ok", "video_id": video_id, "dados": {}}

            row = rows[0]
            return {
                "status": "ok",
                "video_id": video_id,
                "periodo": f"{start_date} → {end_date}",
                "dados": {
                    "views": row[1],
                    "watch_time_min": row[2],
                    "avg_view_duration_s": row[3],
                    "avg_view_percentage": row[4],
                    "subscribers_gained": row[5],
                    "likes": row[6],
                    "comments": row[7],
                },
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def metricas_canal(self, dias: int = 30) -> dict:
        """
        Retorna métricas gerais do canal.
        """
        if not self.analytics:
            return {"status": "error", "error": "YouTube Analytics não autenticado"}

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d")

        try:
            response = self.analytics.reports().query(
                ids="channel==MINE",
                startDate=start_date,
                endDate=end_date,
                metrics="views,estimatedMinutesWatched,subscribersGained,subscribersLost",
            ).execute()

            rows = response.get("rows", [])
            if not rows:
                return {"status": "ok", "dados": {}}

            row = rows[0]
            return {
                "status": "ok",
                "periodo": f"{start_date} → {end_date}",
                "dados": {
                    "views_totais": row[0],
                    "watch_time_total_min": row[1],
                    "inscritos_ganhos": row[2],
                    "inscritos_perdidos": row[3],
                    "saldo_inscritos": row[2] - row[3],
                },
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def top_videos(self, limite: int = 10) -> list:
        """
        Retorna os vídeos com melhor performance.
        """
        if not self.analytics:
            return []
        try:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

            response = self.analytics.reports().query(
                ids="channel==MINE",
                startDate=start_date,
                endDate=end_date,
                metrics="views,estimatedMinutesWatched,averageViewPercentage",
                dimensions="video",
                sort="-views",
                maxResults=limite,
            ).execute()

            return [
                {"video_id": row[0], "views": row[1], "watch_time": row[2], "avg_view_pct": row[3]}
                for row in response.get("rows", [])
            ]
        except Exception:
            return []
