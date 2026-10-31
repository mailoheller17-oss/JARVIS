"""Sehen-Tools für Videoanalyse mit Fallbacks."""

from __future__ import annotations


def analyse_video(video_path: str, api_key: str | None = None) -> dict:
    """TODO-CLAUDE: Gemini-Upload plus Fallback mit ffmpeg, OpenCV und PySceneDetect implementieren."""
    return {"video": video_path, "bewertung": 7, "highlights": [], "warnungen": []}
