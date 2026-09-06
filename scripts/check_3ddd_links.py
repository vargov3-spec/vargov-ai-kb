# -*- coding: utf-8 -*-
"""Проверка ссылок на свои 3D-модели: живы ли слаги из выгрузки аккаунта.

Зачем. Слаги на 3ddd переименовываются, а выгрузка аккаунта у конфигуратора
пересобирается вручную (последняя — 01.09.2026). При массовом переименовании
первым ломается он: в разметке /sku/ останутся старые адреса и 404, и заметить
это некому. Поэтому базе достаточно выборочной проверки: массовое
переименование задевает десятки карточек сразу, и выборка в 25 адресов ловит
его почти наверняка.

Вежливость к чужому сайту: по одному запросу с паузой, HEAD, свой User-Agent.
Полный обход (--all, 603 адреса) запускать только по поводу.

    python scripts/check_3ddd_links.py            # выборка 25
    python scripts/check_3ddd_links.py --all      # все, с паузой
"""
from __future__ import annotations

import argparse
import json
import random
import subprocess
import time
from pathlib import Path

KB = Path(__file__).resolve().parent.parent
UA = "vargov-ai-kb link check (own account cards)"


def status(url: str, timeout: int = 20) -> str:
    r = subprocess.run(
        ["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}", "-I", "-L",
         "--max-time", str(timeout), "-A", UA, url],
        capture_output=True, text=True,
    )
    return (r.stdout or "000").strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="проверить все ссылки, не выборку")
    ap.add_argument("--sample", type=int, default=25)
    ap.add_argument("--pause", type=float, default=1.5)
    ap.add_argument("--seed", type=int, default=None, help="фиксировать выборку")
    args = ap.parse_args()

    graph = json.loads((KB / "references" / "catalog.jsonld").read_text(encoding="utf-8"))["@graph"]
    links = [(n["sku"], n["subjectOf"]["sameAs"]) for n in graph
             if n.get("@type") == "Product" and n.get("subjectOf")]
    print(f"карточек с 3D-моделью: {len(links)}")

    if not args.all:
        rnd = random.Random(args.seed)
        links = rnd.sample(links, min(args.sample, len(links)))
        print(f"проверяем выборку: {len(links)}")

    dead = []
    for i, (sku, url) in enumerate(links, 1):
        code = status(url)
        if code not in ("200", "301", "302"):
            dead.append((sku, url, code))
            print(f"  [{code}] {sku} → {url}")
        if i < len(links):
            time.sleep(args.pause)

    if dead:
        print(f"\nМёртвых адресов: {len(dead)} из {len(links)}.")
        print("Похоже на переименование слагов — попросить у конфигуратора свежую")
        print("выгрузку аккаунта (POST /api/models, user_slug=vargov) и пересобрать базу.")
        return 1
    print(f"\nВсе {len(links)} адресов живы: выгрузка аккаунта актуальна.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
