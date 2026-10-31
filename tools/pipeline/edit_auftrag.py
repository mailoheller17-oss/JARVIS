"""Einfacher Startpunkt für Edit-Aufträge."""

from __future__ import annotations

import argparse

from tools.pipeline import build_edit_order


def main() -> None:
    parser = argparse.ArgumentParser(description="Jarvis Edit-Auftrag")
    parser.add_argument("--thema", required=True)
    parser.add_argument("--stil", default="aggressive")
    parser.add_argument("--laenge", type=int, default=15)
    args = parser.parse_args()

    result = build_edit_order(args.thema, args.stil, args.laenge)
    print(result)


if __name__ == "__main__":
    main()
