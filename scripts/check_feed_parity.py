# -*- coding: utf-8 -*-
"""Сверка графа базы с живым фидом сайта — по строкам, а не по числам.

Зачем строки. Числа сравнивать нельзя: 1 и 1.0 в Python равны, а в JSON это
разные документы; банковское округление Python против Math.round в JS даёт
расхождение в сотых, которое при численном сравнении с допуском не видно.
Поэтому обе стороны приводятся к канонической строке (как JSON.stringify) и
сравниваются посимвольно — совет агента сайта от 06.09.2026.

Один запрос к vargov.ru, сжатый (gzip): 1,1 МБ превращаются примерно в 140 КБ. Сайт запрещено сканировать, поэтому здесь
ровно один адрес и никаких обходов.

Запуск: python scripts/check_feed_parity.py [--feed URL]
Код возврата 1, если есть расхождения.
"""
from __future__ import annotations

import argparse
import json
import gzip
import sys
import urllib.request
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
    """Один запрос средствами Python, без curl.

    07.09.2026 curl из этой оболочки перестал доходить куда бы то ни было —
    висел и на vargov.ru, и на github.com, тогда как PowerShell и git ходили
    нормально. Диагноз «площадка недоступна» по одному только curl больше не
    ставим: инструмент отказал раньше сети.
    """
    req = urllib.request.Request(url, headers={
        "User-Agent": "vargov-ai-kb parity check",
        "Accept-Encoding": "gzip",     # фид 1,1 МБ, сжатый — около 140 КБ
    })
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            raw = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
    except Exception as e:                       # noqa: BLE001 — причина в тексте
        sys.exit(f"не удалось получить фид: {type(e).__name__}: {e}")
    return json.loads(raw.decode("utf-8"))


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
    link_form = type_form = 0
    for c in both:
        a, b = mine[c].get("subjectOf"), site[c].get("subjectOf")
        if canon(a) == canon(b):
            continue
        if not a or not b:
            print(f"{'subjectOf':>20}: у {c} узел 3D-модели есть только с одной стороны")
            problems += 1
            continue
        # У базы subjectOf — список: карточка-представитель плюс CollectionPage
        # со всеми моделями артикула (их у 85 % артикулов несколько). У сайта —
        # один узел со списком по тегу. Сверяем узел 3DModel с узлом сайта.
        def is_list(node) -> bool:
            """Узел ведёт на аккаунтный список моделей, а не на карточку."""
            return "/users/vargov/models?tag=" in (node.get("url") or "")

        nodes_mine = a if isinstance(a, list) else [a]
        nodes_site = b if isinstance(b, list) else [b]
        # Сравниваем по СМЫСЛУ адреса, а не по @type: сайт публикует список
        # моделей под типом 3DModel, база — под CollectionPage. Это расхождение
        # схемы, а не данных; отмечаем отдельным счётчиком и говорим о нём вслух.
        mine_card = next((x for x in nodes_mine if not is_list(x)), None)
        site_card = next((x for x in nodes_site if not is_list(x)), None)
        mine_list = next((x for x in nodes_mine if is_list(x)), None)
        site_list = next((x for x in nodes_site if is_list(x)), None)
        if mine_list and site_list and mine_list.get("@type") != site_list.get("@type"):
            type_form += 1
        if (mine_card is None) != (site_card is None) and not (mine_list and site_list):
            print(f"{'subjectOf':>20}: у {c} нет узла 3D-модели с одной из сторон")
            problems += 1
            continue
        if mine_card and site_card and mine_card.get("name") != site_card.get("name"):
            print(f"{'subjectOf':>20}: расхождение по существу у {c}")
            problems += 1
        else:
            link_form += 1
    print(f"{'subjectOf':>20}: ок" + (f" (вид ссылки различается намеренно у {link_form} артикулов: "
          f"у базы прямые карточки, у сайта аккаунтные списки)" if link_form else ""))
    if type_form:
        print(f"{'':>20}  внимание: у {type_form} артикулов сайт помечает список моделей типом 3DModel — "
              "узел обещает модель, а ведёт на перечень; в базе это CollectionPage")

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
