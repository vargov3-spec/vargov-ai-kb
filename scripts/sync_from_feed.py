#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ночная сверка базы знаний с первоисточником — фидом сайта.

ЧТО ДЕЛАЕТ. Один раз скачивает https://vargov.ru/catalog.jsonld и
https://vargov.ru/llms.txt (два запроса, не чаще раза в сутки — сервер общий) и
переносит в базу знаний ТОЛЬКО то, чем владеет фид:

  references/catalog.jsonld       — у каждого Product поля фида (описание-сниппет,
                                    снимки, награды, параметры элементов, сертификат,
                                    3D-модели, адреса) заменяются полями из фида;
                                    новые артикулы добавляются; узлы Organization/
                                    Person в графе получают награды и sameAs фида
  references/organization.jsonld  — те же награды и sameAs у Organization
  en/datasets/*                   — английский сниппет и галерея по каждому артикулу
  references/vargov.ru-llms.txt   — дословная копия llms.txt сайта с датой снятия

ЧЕГО НЕ ДЕЛАЕТ. Тексты на восьми языках (описание, «где уместна», стилистика) в
фиде отсутствуют — они живут в приватном репозитории сайта и пересобираются
локально (scripts/build_from_site.py). Если фид разошёлся с датасетами по составу
артикулов или по английским сниппетам, сценарий пишет scan/feed-drift.md и
завершается кодом 3 — workflow заводит issue, и локальная пересборка делается
руками. Это не сбой, а сигнал.

ЗАЩИТА ОТ 27.07.2026 (тогда сборщик закоммитил пустые файлы): при любой ошибке
загрузки, при невалидном JSON, при < 500 Product в фиде или отсутствии
Organization ничего не пишется и сценарий падает с кодом 1. Файлы никогда не
удаляются, артикулы из базы не выбрасываются (только добавляются).

Запуск: python scripts/sync_from_feed.py [--feed-file path] [--llms-file path] [--dry-run]
Коды выхода: 0 — сверено (с изменениями или без), 1 — источник недоступен/подозрителен,
3 — есть расхождения, требующие локальной пересборки (изменения фида при этом записаны).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.request
from pathlib import Path

KB = Path(__file__).resolve().parent.parent
FEED_URL = "https://vargov.ru/catalog.jsonld"
LLMS_URL = "https://vargov.ru/llms.txt"
UA = "vargov-ai-kb nightly sync (+https://github.com/vargov3-spec/vargov-ai-kb)"
MIN_PRODUCTS = 500
# Поля Product, которыми владеет фид. Всё остальное в узле базы остаётся как есть.
FEED_OWNED = ("name", "sku", "url", "sameAs", "image", "category", "description",
              "award", "additionalProperty", "hasCertification", "subjectOf",
              "brand", "manufacturer", "inLanguage")


def fetch(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        if r.status != 200:
            raise RuntimeError(f"{url}: HTTP {r.status}")
        return r.read()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, obj: dict, dry: bool) -> bool:
    text = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    if not dry:
        path.write_text(text, encoding="utf-8", newline="\n")
    return True


def write_text(path: Path, text: str, dry: bool) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    if not dry:
        path.write_text(text, encoding="utf-8", newline="\n")
    return True


def by_type(graph: list[dict], t: str) -> list[dict]:
    return [n for n in graph if n.get("@type") == t]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--feed-file", type=Path, help="локальная копия фида вместо загрузки (для проверки)")
    ap.add_argument("--llms-file", type=Path, help="локальная копия llms.txt вместо загрузки")
    ap.add_argument("--dry-run", action="store_true", help="ничего не записывать, только отчитаться")
    a = ap.parse_args()
    dry = a.dry_run
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # 1. Источник. Любая беда здесь — выход 1 без записи.
    try:
        feed_raw = a.feed_file.read_bytes() if a.feed_file else fetch(FEED_URL)
        llms_raw = a.llms_file.read_bytes() if a.llms_file else fetch(LLMS_URL)
    except Exception as e:  # noqa: BLE001
        print(f"ИСТОЧНИК НЕДОСТУПЕН: {e}", file=sys.stderr)
        return 1
    try:
        feed = json.loads(feed_raw.decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"ФИД НЕ РАЗБИРАЕТСЯ КАК JSON: {e}", file=sys.stderr)
        return 1
    graph = feed.get("@graph") or []
    products = by_type(graph, "Product")
    orgs = by_type(graph, "Organization")
    if len(products) < MIN_PRODUCTS or not orgs:
        print(f"ФИД ПОДОЗРИТЕЛЕН: Product {len(products)}, Organization {len(orgs)} — ничего не пишу",
              file=sys.stderr)
        return 1
    llms_text = llms_raw.decode("utf-8")
    if "vargov" not in llms_text.lower() or len(llms_text) < 1000:
        print(f"llms.txt ПОДОЗРИТЕЛЕН: {len(llms_text)} символов — ничего не пишу", file=sys.stderr)
        return 1
    print(f"фид: {len(graph)} узлов, Product {len(products)}; llms.txt {len(llms_text)} символов")

    changed: list[str] = []
    drift: list[str] = []

    # 2. Граф базы: поля фида в каждом Product, новые артикулы — добавить.
    cat_path = KB / "references" / "catalog.jsonld"
    kb_graph_doc = load_json(cat_path)
    kb_graph = kb_graph_doc["@graph"]
    kb_by_id = {n.get("@id"): n for n in kb_graph if n.get("@id")}
    added = 0
    for p in products:
        node = kb_by_id.get(p.get("@id"))
        if node is None:
            kb_graph.append(p)
            kb_by_id[p["@id"]] = p
            added += 1
            continue
        for k in FEED_OWNED:
            if k in p:
                node[k] = p[k]
            elif k in node:
                del node[k]
    feed_org = orgs[0]

    def merge_org(node: dict) -> None:
        # Награды — как в фиде (он их источник). sameAs — объединение: фид первым,
        # затем адреса, которые есть только в базе (например, ссылка на сам
        # репозиторий), чтобы ночная сверка не выбрасывала их молча.
        if "award" in feed_org:
            node["award"] = feed_org["award"]
        if "sameAs" in feed_org:
            seen: list[str] = []
            for u in list(feed_org["sameAs"]) + list(node.get("sameAs") or []):
                if u not in seen:
                    seen.append(u)
            node["sameAs"] = seen

    for node in by_type(kb_graph, "Organization"):
        merge_org(node)
    for node in by_type(kb_graph, "Person"):
        fp = by_type(graph, "Person")
        if fp and "award" in fp[0]:
            node["award"] = fp[0]["award"]
    if dump_json(cat_path, kb_graph_doc, dry):
        changed.append(f"references/catalog.jsonld (новых артикулов {added})")
    feed_skus = {p.get("sku") for p in products}
    kb_skus = {n.get("sku") for n in by_type(kb_graph, "Product")}
    if kb_skus - feed_skus:
        drift.append(f"в базе есть артикулы, которых нет в фиде: {sorted(kb_skus - feed_skus)[:10]}")

    # 3. Карточка организации.
    org_path = KB / "references" / "organization.jsonld"
    org_doc = load_json(org_path)
    for node in by_type(org_doc["@graph"], "Organization"):
        merge_org(node)
    if dump_json(org_path, org_doc, dry):
        changed.append("references/organization.jsonld")

    # 4. Английские датасеты: сниппет и галерея по артикулу; расхождения по составу — сигнал.
    en_path = KB / "en" / "datasets" / "products.json"
    en_rows = load_json(en_path)
    feed_by_sku = {p.get("sku"): p for p in products}
    en_skus = {r["code"] for r in en_rows}
    if feed_skus - en_skus:
        drift.append(f"в фиде новые артикулы, которых нет в датасетах: {sorted(feed_skus - en_skus)[:10]}")
    snippet_diff = 0
    for r in en_rows:
        p = feed_by_sku.get(r["code"])
        if not p:
            continue
        if p.get("description") and p["description"] != r.get("snippet"):
            snippet_diff += 1
            r["snippet"] = p["description"]
        imgs = p.get("image") or []
        if isinstance(imgs, list) and imgs:
            r["gallery"] = imgs
            r["image"] = imgs[0]
            r["gallery_total"] = len(imgs)
    if dump_json(en_path, en_rows, dry):
        changed.append(f"en/datasets/products.json (сниппетов обновлено {snippet_diff})")
    jsonl = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in en_rows)
    if write_text(KB / "en" / "datasets" / "products.jsonl", jsonl, dry):
        changed.append("en/datasets/products.jsonl")
    if snippet_diff:
        drift.append(f"английские сниппеты изменились у {snippet_diff} артикулов — тексты на остальных "
                     f"языках в базе могли устареть, нужна локальная пересборка")

    # 5. Копия llms.txt сайта.
    mirror = (f"# Дословная копия https://vargov.ru/llms.txt, снята {today} ночной сверкой "
              f"(scripts/sync_from_feed.py). Первоисточник — сайт.\n\n" + llms_text)
    if write_text(KB / "references" / "vargov.ru-llms.txt", mirror, dry):
        changed.append("references/vargov.ru-llms.txt")

    # 6. Отчёт.
    scan = KB / "scan"
    scan.mkdir(exist_ok=True)
    report = [f"# Сверка с фидом vargov.ru — {today}", "",
              f"Фид: {len(products)} Product, {len(graph)} узлов; llms.txt {len(llms_text)} символов.", ""]
    report += ["Изменено:"] + [f"- {c}" for c in changed] if changed else ["Изменений нет."]
    if drift:
        report += ["", "**Нужна локальная пересборка (python scripts/build_from_site.py):**"]
        report += [f"- {d}" for d in drift]
    write_text(scan / "feed-drift.md", "\n".join(report) + "\n", dry)
    print("\n".join(report))
    return 3 if drift else 0


if __name__ == "__main__":
    sys.exit(main())
