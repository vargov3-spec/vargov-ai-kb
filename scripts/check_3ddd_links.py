# -*- coding: utf-8 -*-
"""Проверка ссылок на свои 3D-модели: живы ли слаги из выгрузки аккаунта.

Зачем. Слаги на 3ddd переименовываются, а выгрузка аккаунта у конфигуратора
пересобирается вручную. При массовом переименовании первой ломается его
разметка /sku/: там остаются старые адреса и 404. Массовое переименование
задевает десятки карточек сразу, поэтому даже выборка в 25 адресов ловит его
почти наверняка.

Откуда запускать. С машины владельца 3ddd.ru и 3dsky.org НЕ открываются —
код 000, таймаут на любом адресе (проверено 06.09.2026 двумя агентами
независимо; дело в канале машины). С VPS конфигуратора обе площадки отвечают
за 0,15 с. По договорённости от 06.09.2026 обход ведёт агент конфигуратора
оттуда, раз в месяц и после каждого обновления выгрузки.

Три причины кода 000, которые нельзя путать (случай агента конфигуратора,
06.09.2026: 250 нулей подряд оказались не баном площадки, а символом \\r в
конце каждого адреса — список готовили на Windows):
  1) канал не доходит до площадки;
  2) адреса битые — пробел, перевод строки, \\r;
  3) площадка действительно молчит.
Поэтому: адреса чистятся от пробельных символов, перед обходом делается
одиночная проба, и если она не прошла — обход не запускается вовсе. Код 000
никогда не попадает в счётчик битых ссылок.

    python scripts/check_3ddd_links.py            # выборка 25
    python scripts/check_3ddd_links.py --all      # все, с паузой
"""
from __future__ import annotations

import argparse
import json
import random
import re
import subprocess
import time
from pathlib import Path

KB = Path(__file__).resolve().parent.parent
UA = "vargov-ai-kb link check (own account cards)"
URL_OK = re.compile(r"^https://(3ddd\.ru|3dsky\.org)/3dmodels/show/[\w-]+$")


def status(url: str, timeout: int = 20) -> str:
    """Код ответа строкой; 000 — запрос не дошёл (сеть, DNS, таймаут)."""
    r = subprocess.run(
        ["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}", "-I", "-L",
         "--max-time", str(timeout), "-A", UA, url],
        capture_output=True, text=True,
    )
    return (r.stdout or "000").strip()


def links_from_graph() -> list[tuple[str, str]]:
    graph = json.loads((KB / "references" / "catalog.jsonld").read_text(encoding="utf-8"))["@graph"]
    out: list[tuple[str, str]] = []
    for node in graph:
        if node.get("@type") != "Product":
            continue
        for sub in node.get("subjectOf") or []:
            # Только 3DModel. CollectionPage (аккаунтный список по тегу) в обход
            # НЕ берём намеренно: он отвечает 200 всегда, даже когда моделей по
            # тегу не осталось, и дал бы ложное «всё живо» ровно в том случае,
            # который и надо ловить. Пустой тег виден только через API аккаунта
            # (POST /api/models, user_slug + tag) — это делает агент конфигуратора.
            if isinstance(sub, dict) and sub.get("@type") == "3DModel" and sub.get("sameAs"):
                # \r, пробелы и переводы строк уезжают в конец адреса и делают
                # его нерезолвимым — чистим до запроса, а не гадаем по коду 000.
                out.append((node["sku"], sub["sameAs"].strip()))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="проверить все ссылки, не выборку")
    ap.add_argument("--sample", type=int, default=25)
    ap.add_argument("--pause", type=float, default=1.5)
    ap.add_argument("--seed", type=int, default=None, help="фиксировать выборку")
    args = ap.parse_args()

    links = links_from_graph()
    print(f"карточек с 3D-моделью: {len(links)}")

    malformed = [(sku, url) for sku, url in links if not URL_OK.match(url)]
    if malformed:
        print(f"адреса неправильной формы: {len(malformed)} → {malformed[:3]}")
        print("Это ошибка данных, а не площадки: чинить реестр, а не обходить сеть.")
        return 3

    if not args.all:
        links = random.Random(args.seed).sample(links, min(args.sample, len(links)))
        print(f"проверяем выборку: {len(links)}")

    # Проба: один заведомо правильный адрес. Не прошла — обход бессмыслен.
    probe_sku, probe_url = links[0]
    probe = status(probe_url)
    if probe == "000":
        print(f"\nПроба не дошла ({probe_sku}): площадка недоступна с этой машины.")
        print("Это НЕ значит, что ссылки мертвы. Запускать оттуда, где 3ddd.ru "
              "открывается (VPS конфигуратора), либо просить проверку у агента "
              "конфигуратора — у него работает API аккаунта.")
        return 2
    print(f"проба {probe_sku}: {probe} — площадка отвечает, идём дальше")

    dead: list[tuple[str, str, str]] = []
    no_answer = 0
    for i, (sku, url) in enumerate(links, 1):
        code = probe if i == 1 else status(url)
        if code == "000":
            no_answer += 1
        elif code not in ("200", "301", "302"):
            dead.append((sku, url, code))
            print(f"  [{code}] {sku} → {url}")
        if i < len(links):
            time.sleep(args.pause)

    print(f"\nпроверено {len(links)}: живых {len(links) - len(dead) - no_answer}, "
          f"не дошли {no_answer}, битых {len(dead)}")
    if dead:
        print("Похоже на переименование слагов — попросить у конфигуратора свежую")
        print("выгрузку аккаунта (POST /api/models, user_slug=vargov) и пересобрать базу.")
        return 1
    if no_answer:
        print("Часть запросов не дошла — результат неполный, повторить позже.")
        return 2
    print("Выгрузка аккаунта актуальна.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
