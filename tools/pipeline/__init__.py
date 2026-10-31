"""Pipeline für Edit-Aufträge vom Handy und aus der Web-App."""

from __future__ import annotations


def build_edit_order(thema: str, stil: str = "aggressive", laenge: int = 15) -> dict:
    """TODO-CLAUDE: Recherche -> Material -> Analyse -> Auto-Edit -> Posting-Paket in einer Pipeline verbinden."""
    return {
        "thema": thema,
        "stil": stil,
        "laenge": laenge,
        "status": "bereit",
        "beschreibung": f"Edit-Auftrag für {thema}",
    }
