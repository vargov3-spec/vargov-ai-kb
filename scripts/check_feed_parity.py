# -*- coding: utf-8 -*-
"""Сверка графа базы с живым фидом сайта — по строкам, а не по числам.

Зачем строки. Числа сравнивать нельзя: 1 и 1.0 в Python равны, а в JSON это
разные документы; банковское округление Python против Math.round в JS даёт
расхождение в сотых, которое при численном сравнении с допуском не видно.
Поэтому обе стороны приводятся к канонической строке (как JSON.stringify) и
сравниваются посимвольно — совет агента сайта от 06.09.2026.

Один запрос к vargov.ru, сжатый (--compressed): фид отдаётся brotli,
1,1 МБ превращаются в 137 КБ. Сайт запрещено сканировать, поэтому здесь
ровно один адрес и никаких обходов.

Запуск: python scripts/check_feed_parity.py [--feed URL]
Код возврата 1, если есть расхождения.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

KB = Path(__file__).resolve().parent.parent
FEED = "https://vargov.ru/catalog.jsonld"
FIELDS = ("additionalProperty", "award", "category", "brand", "manufacturer")

# subjectOf сверяем отдельно: вид ссылки на 3D-модель различается намеренно.
# У сайта на кнопке и в фиде стоит аккаунтный список ?tag= (устойчив к
# переименованию слага), у базы — прямая карточка /show/<slug> (у неё есть
# название, автор и превью, и для языковой модели она содержательнее).
# Расхождением считаем только разницу типа и названия узла.


def canon(value) -> str:
    """Каноническая строка узла: порядок ключей сохраняем — JSON.stringify тоже."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def fetch(url: str) -> dict:
    r = subprocess.run(
        ["curl", "-sS", "--compressed", "--max-time", "60", "-A", "vargov-ai-kb parity check", url],
        capture_output=True,
    )
    if r.returncode != 0:
        sys.exit(f"не удалось получить фид: {r.stderr.decode('utf-8', 'replace')[:300]}")
    return json.loads(r.stdout.decode("utf-8"))


def products(graph: list) -> dict:
    return {n["sku"]: n for n in graph if n.get("@type") == "Product" and n.get("sku")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--feed", default=FEED)
    args = ap.parse_args()

    mine = products(json.loads((KB / "references" / "catalog.jsonld").read_text(encoding="utf-8"))["@graph"])
    site = products(fetch(args.feed)["@graph"])

    print(f"артикулов: база {len(mine)}, сайт {len(site)}")
    only_mine = sorted(set(mine) - set(site))
    only_site = sorted(set(site) - set(mine))
    if only_mine:
        print(f"  только в базе: {len(only_mine)} → {only_mine[:5]}")
    if only_site:
        print(f"  только на сайте: {len(only_site)} → {only_site[:5]}")

    problems = 0
    both = sorted(set(mine) & set(site))
    link_form = 0
    for c in both:
        a, b = mine[c].get("subjectOf"), site[c].get("subjectOf")
        if canon(a) == canon(b):
            continue
        if not a or not b:
            print(f"{'subjectOf':>20}: у {c} узел 3D-модели есть только с одной стороны")
            problems += 1
            continue
        if a.get("@type") != b.get("@type") or a.get("name") != b.get("name"):
            print(f"{'subjectOf':>20}: расхождение по существу у {c}")
            problems += 1
        else:
            link_form += 1
    print(f"{'subjectOf':>20}: ок" + (f" (вид ссылки различается намеренно у {link_form} артикулов: "
          f"у базы прямые карточки, у сайта аккаунтные списки)" if link_form else ""))

    for field in FIELDS:
        diff = [c for c in sorted(set(mine) & set(site))
                if canon(mine[c].get(field)) != canon(site[c].get(field))]
        # различие только в порядке ключей отделяем от различия по существу
        order_only = [c for c in diff
                      if json.dumps(mine[c].get(field), ensure_ascii=False, sort_keys=True)
                      == json.dumps(site[c].get(field), ensure_ascii=False, sort_keys=True)]
        real = [c for c in diff if c not in order_only]
        status = "ок" if not diff else f"расхождений {len(real)}" + (f", порядок ключей {len(order_only)}" if order_only else "")
        print(f"{field:>20}: {status}" + (f" → {real[:3]}" if real else ""))
        problems += len(real)

    if only_mine or only_site or problems:
        print("\nСверка НЕ пройдена.")
        return 1
    print("\nСверка пройдена: граф базы совпадает с фидом сайта.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
