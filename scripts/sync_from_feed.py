#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ночная сверка базы знаний с первоисточником — фидом сайта.

ЧТО ДЕЛАЕТ. Один раз скачивает https://vargov.ru/catalog.jsonld и
https://vargov.ru/llms.txt (два запроса, не чаще раза в сутки — сервер общий) и
переносит в базу знаний ТОЛЬКО то, чем владеет фид (снимки и ссылки на 3D-модели
в базе богаче фида и остаются как есть):

  references/catalog.jsonld       — у каждого Product поля фида (описание-сниппет,
                                    снимки, награды, параметры элементов, сертификат,
                                    3D-модели, адреса) заменяются полями из фида;
                                    новые артикулы добавляются; узлы Organization/
                                    Person в графе получают награды и sameAs фида
  references/organization.jsonld  — те же награды и sameAs у Organization
  en/datasets/*                   — английский сниппет по каждому артикулу
  references/vargov.ru-llms.txt   — дословная копия llms.txt сайта с датой снятия

ЧЕГО НЕ ДЕЛАЕТ. Тексты на восьми языках (описание, «где уместна», стилистика) в
фиде отсутствуют — они живут в приватном репозитории сайта и пересобираются
локально (scripts/build_from_site.py). Если фид разошёлся с датасетами по составу
артикулов или по английским сниппетам, сценарий пишет scan/feed-drift.md и
завершается кодом 3 — workflow заводит issue, и локальная пересборка делается
руками. Это не сбой, а сигнал.

Поле `awards` у записи (строки «премия — степень» со ссылкой, из которых
печатается раздел «Награды» карточки) сверка тоже не ведёт — его собирает
только build_from_site.py из awards.ts сайта. Флаг `award_winning` приходит из
products.jsonl и обновляется ночью, поэтому 22.09.2026 у LC0312, LC0338, LC0340,
LC0341 и LC0543-2 флаг стоял, а раздела «Награды» в карточке не было: появилась
награда — нужна локальная пересборка.

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
import time
import urllib.request
from pathlib import Path

KB = Path(__file__).resolve().parent.parent
FEED_URL = "https://vargov.ru/catalog.jsonld"
LLMS_URL = "https://vargov.ru/llms.txt"
# Тексты карточек на восьми языках — публичный файл сайта с 17.09.2026 (ba3676a).
PRODUCTS_URL = "https://vargov.ru/datasets/products.jsonl"
UA = "vargov-ai-kb nightly sync (+https://github.com/vargov3-spec/vargov-ai-kb)"
MIN_PRODUCTS = 500
# Поля Product, которыми владеет фид. Всё остальное в узле базы остаётся как есть.
# image и subjectOf НЕ входят: в базе они богаче фида (полная галерея, Sketchfab и
# страница всех моделей артикула) — первый автопрогон 17.09.2026 их затёр, откачено.
FEED_OWNED = ("name", "sku", "url", "sameAs", "category", "description",
              "award", "additionalProperty", "hasCertification",
              "brand", "manufacturer", "inLanguage")


def fetch(url: str, timeout: int = 60, attempts: int = 3, pause: int = 90) -> bytes:
    """Один запрос; при сбое ещё до двух повторов с паузой. Сайт тянет сборку по
    крону каждые 5 минут, и прогон #7 (17.09.2026 14:28 UTC) попал в окно выкладки:
    источник «недоступен», хотя через семь минут отдавался. Пауза 90 с покрывает окно."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
    last: Exception | None = None
    for n in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                if r.status != 200:
                    raise RuntimeError(f"{url}: HTTP {r.status}")
                return r.read()
        except Exception as e:  # noqa: BLE001 — любой сетевой сбой: ждём и повторяем
            last = e
            if n < attempts:
                print(f"[сверка] {url}: попытка {n} не удалась ({e}); повтор через {pause} с", file=sys.stderr)
                time.sleep(pause)
    raise RuntimeError(f"{url}: {last}")


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
    ap.add_argument("--products-file", type=Path, help="локальная копия products.jsonl вместо загрузки")
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

    # 4. Тексты на восьми языках — из products.jsonl сайта (третий и последний
    #    запрос за ночь; файл выложен сайтом 17.09.2026, коммит ba3676a). Одна
    #    строка — артикул: code, slug, category, awardWinning, url{lang}, text{lang}
    #    = {type, paragraphs, whereItWorks, style[, madeToOrder]}; пустые поля
    #    опущены, а ключ, которого нет ни у кого, файл не несёт (см. carried). Тексты кладутся в канонические записи datasets/products.json,
    #    и из них тем же сборщиком печатаются все производные файлы: датасеты RU/EN,
    #    CSV, оглавления разделов и 605 × 2 страниц карточек. Пока файл не отдаётся
    #    (выкладка сайта идёт кроном), сценарий говорит об этом и тексты не трогает.
    ds_path = KB / "datasets" / "products.json"
    recs = load_json(ds_path)
    by_code = {r["code"]: r for r in recs}
    text_changed = 0
    try:
        rows_raw = (a.products_file.read_bytes() if a.products_file else fetch(PRODUCTS_URL)).decode("utf-8")
        rows = [json.loads(line) for line in rows_raw.splitlines() if line.strip()]
    except Exception as e:  # noqa: BLE001
        # Не расхождение, а недоступность источника: тексты остаются прежними,
        # issue не заводится — это попадёт только в сводку прогона.
        rows = []
        changed.append(f"(products.jsonl сайта не получен: {str(e)[:80]} — тексты на восьми языках не обновлялись)")
    if rows and (len(rows) < MIN_PRODUCTS or not all(r.get("code") and isinstance(r.get("text"), dict) for r in rows)):
        drift.append(f"products.jsonl подозрителен: строк {len(rows)} — тексты не обновлялись")
        rows = []
    if rows:
        sys.path.insert(0, str(KB / "scripts"))
        from build_from_site import (CATEGORIES, snippet, write_datasets,  # noqa: E402
                                     write_collections, product_page, write)
        site_codes = {r["code"] for r in rows}
        # Какие ключи файл вообще несёт. Ключ, которого нет ни у одной записи, файл
        # не экспортирует — это не «пусто у всех». Прогон 17.09.2026 (6ec9540) принял
        # отсутствующий madeToOrder за пустоту и стёр «Изготовление» у 605 артикулов
        # на восьми языках; откачено (00ac50a). Ключ, который есть хоть у кого-то, но
        # опущен у записи, — пустое значение у этой записи (так файл кодирует пустоту).
        carried = {k for r in rows for c in (r.get("text") or {}).values()
                   if isinstance(c, dict) for k in c}
        carried_row = {k for r in rows for k in r}
        if site_codes - set(by_code):
            drift.append(f"на сайте новые артикулы, которых нет в базе (нужна локальная пересборка — "
                         f"галерея и модели берутся из репозитория сайта): {sorted(site_codes - set(by_code))[:10]}")
        if set(by_code) - site_codes:
            drift.append(f"в базе артикулы, которых больше нет на сайте: {sorted(set(by_code) - site_codes)[:10]}")
        TEXT_FIELDS = ("type", "description", "where_it_works", "style", "made_to_order")

        def filled(rec: dict) -> set:
            return {(f, lang) for f in TEXT_FIELDS
                    for lang, v in (rec.get(f) or {}).items() if v}

        filled_before = {code: filled(rec) for code, rec in by_code.items()}
        for row in rows:
            rec = by_code.get(row["code"])
            if not rec:
                continue
            before = json.dumps(rec, ensure_ascii=False, sort_keys=True)
            cat = row.get("category") or rec["category"]
            if cat in CATEGORIES:
                rec["category"] = cat
                rec["category_label"] = {"ru": CATEGORIES[cat][0], "en": CATEGORIES[cat][1]}
            if isinstance(row.get("url"), dict) and row["url"]:
                rec["urls"] = row["url"]
            if "awardWinning" in carried_row:
                rec["award_winning"] = bool(row.get("awardWinning"))
            for lang, c in (row.get("text") or {}).items():
                if not isinstance(c, dict):
                    continue
                if "type" in carried:
                    rec["type"][lang] = c.get("type")
                if "paragraphs" in carried:
                    body = "\n\n".join(c.get("paragraphs") or [])
                    rec["description"][lang] = body
                    rec["snippet"][lang] = snippet(body) if body else None
                if "whereItWorks" in carried:
                    rec["where_it_works"][lang] = c.get("whereItWorks")
                if "style" in carried:
                    rec["style"][lang] = c.get("style")
                if "madeToOrder" in carried:
                    rec["made_to_order"][lang] = c.get("madeToOrder")
            if json.dumps(rec, ensure_ascii=False, sort_keys=True) != before:
                text_changed += 1
        # Страховка от массового опустошения: сайт может убрать текст у одного
        # артикула, но не у сотен разом. Если поле пропадает больше чем у 5 %
        # записей — это дефект источника или сценария (как 6ec9540), а не правка:
        # тексты не пишутся, прогон завершается кодом 3 с описанием.
        blanked = {code for code, rec in by_code.items() if filled_before[code] - filled(rec)}
        if len(blanked) > len(by_code) * 0.05:
            drift.append(f"сверка хотела опустошить текстовые поля у {len(blanked)} артикулов "
                         f"из {len(by_code)} (например {sorted(blanked)[:5]}) — отказ, тексты не тронуты")
            recs = load_json(ds_path)
            text_changed = 0
        # Флаг награды приходит из products.jsonl ночью, а строки наград (раздел
        # «Награды» карточки) собирает только локальный сборщик из awards.ts сайта.
        # Пока пересборки не было, снаружи это выглядит как недоделанная карточка —
        # поэтому такое расхождение поднимаем как drift (код 3 → issue), а не молчим.
        orphan = sorted(r["code"] for r in recs if r.get("award_winning") and not r.get("awards"))
        if orphan:
            drift.append(f"флаг награды есть, а строк наград нет у {len(orphan)} артикулов "
                         f"({', '.join(orphan[:8])}{'…' if len(orphan) > 8 else ''}) — "
                         f"нужна локальная пересборка build_from_site.py")
        if text_changed and not dry:
            write_datasets(recs, KB / "datasets", english=False)
            write_datasets(recs, KB / "en" / "datasets", english=True)
            write_collections(recs, KB / "collections", english=False)
            write_collections(recs, KB / "en" / "collections", english=True)
            for rec in recs:
                write(KB / "products" / rec["category"] / f"{rec['code']}.md", product_page(rec, "ru"))
                write(KB / "en" / "products" / rec["category"] / f"{rec['code']}.md", product_page(rec, "en"))
        if text_changed:
            changed.append(f"тексты на восьми языках обновлены у {text_changed} артикулов "
                           f"(datasets, en/datasets, collections, products — из products.jsonl сайта)")
        else:
            print("products.jsonl: тексты совпадают с базой, изменений нет")

    # 5. Копия llms.txt сайта.
    # Без отметки времени в шапке: иначе файл «менялся» бы каждую ночь и плодил
    # пустые коммиты. Дату снятия показывает история git.
    mirror = ("# Дословная копия https://vargov.ru/llms.txt, снимается ночной сверкой "
              "(scripts/sync_from_feed.py). Первоисточник — сайт.\n\n" + llms_text)
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
