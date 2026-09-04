#!/usr/bin/env python3
"""
Сборка машиночитаемого слоя базы знаний из данных репозитория сайта.

ЗАЧЕМ ЛОКАЛЬНО, А НЕ В GITHUB ACTIONS. Репозиторий сайта приватный —
Actions его не видит. Прежний сканер ходил по живому сайту и 27.07.2026
обнулил все датасеты: после переезда с Tilda `sitemap-store.xml` отдал 404,
парсер получил ноль товаров и молча закоммитил пустые файлы, отчитавшись
«success» три недели подряд. Сканировать сайт нельзя и по другой причине:
nginx держит 20 запросов/с с адреса, fail2ban банит, а лимит соединений
задевает живых посетителей.

Поэтому источник — файлы репозитория сайта, только на чтение:
  catalog.generated.json          605 композиций: артикул, тип, раздел, снимки
  product-copy/products.<lang>.json  описания на 8 языках, согласованы владельцем
  awards.ts                       22 награды (дампится через node --experimental-strip-types)
  instock.generated.json          элементы в наличии

ПРАВИЛА ВЛАДЕЛЬЦА, зашитые в вывод: не называть материалы и размеры
конкретных изделий, не публиковать цены. Поэтому в Product-узлах нет
material, size и offers, а в карточках — таблиц характеристик.

Запуск:  python scripts/build_from_site.py [--site "V:/new site Vargov Design/web"]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

KB = Path(__file__).resolve().parent.parent
DEFAULT_SITE = Path("V:/new site Vargov Design/web")

LOCALES = ["ru", "en", "de", "it", "fr", "es", "vi", "ar"]
SITE_URL = "https://vargov.ru"
ORG_ID = f"{SITE_URL}#organization"

# Ключ раздела -> (подпись RU, подпись EN, адрес RU, адрес EN)
CATEGORIES = {
    "lighting": ("Световые композиции", "Lighting compositions", "/lighting", "/en/lighting"),
    "decorative": ("Декоративные композиции", "Decorative compositions", "/decorative", "/en/decorative"),
    "floor-table-lamps": ("Торшеры и арт-объекты", "Floor lamps, sconces & tabletop objects", "/floor-table-lamps", "/en/floor-table-lamps"),
    "sculptural-decor": ("Скульптурные композиции", "Sculptural compositions & decor", "/sculptural-decor", "/en/sculptural-decor"),
}

CODE_RE = re.compile(r"LC\d{4}(?:-\d)?")
SENTENCE_END = re.compile(r"[.!?…؟](?=\s|$)", re.UNICODE)
SNIPPET_MAX, SNIPPET_MIN = 165, 100


def die(msg: str) -> None:
    sys.exit(f"ОСТАНОВ: {msg}")


# --------------------------------------------------------------------------- чтение


def load_site(site: Path) -> dict:
    data_dir = site / "src" / "lib" / "data"
    if not data_dir.is_dir():
        die(f"нет каталога данных сайта: {data_dir}")

    catalog = json.loads((data_dir / "catalog.generated.json").read_text(encoding="utf-8"))
    if not isinstance(catalog, list) or len(catalog) < 500:
        die(f"catalog.generated.json пуст или подозрительно мал: {len(catalog) if isinstance(catalog, list) else '?'}")

    copy: dict[str, dict] = {}
    for lang in LOCALES:
        f = data_dir / "product-copy" / f"products.{lang}.json"
        if not f.is_file():
            die(f"нет файла описаний: {f}")
        copy[lang] = json.loads(f.read_text(encoding="utf-8")).get("items", {})
        if len(copy[lang]) < 500:
            die(f"описаний на {lang} слишком мало: {len(copy[lang])}")

    instock: dict[str, list] = {}
    f = data_dir / "instock.generated.json"
    if f.is_file():
        for rec in json.loads(f.read_text(encoding="utf-8")):
            instock.setdefault(rec["code"], []).append(rec)

    return {"catalog": catalog, "copy": copy, "instock": instock, "awards": dump_awards(site)}


def dump_awards(site: Path) -> list:
    """awards.ts — TypeScript; исполняем его самим Node вместо разбора текста."""
    out = KB / "scan" / "awards.dump.json"
    out.parent.mkdir(exist_ok=True)
    script = (
        "import('./src/lib/data/awards.ts').then(m=>{"
        "require('fs').writeFileSync(process.argv[1],"
        "JSON.stringify({count:m.awardsCount(),awards:m.AWARDS_DETAILED}));});"
    )
    r = subprocess.run(
        ["node", "--experimental-strip-types", "-e", script, str(out)],
        cwd=site, capture_output=True, text=True, timeout=120,
    )
    if r.returncode != 0 or not out.is_file():
        die(f"не удалось выгрузить awards.ts: {r.stderr[:400]}")
    dump = json.loads(out.read_text(encoding="utf-8"))
    print(f"  награды: {dump['count']} в {len(dump['awards'])} программах")
    return dump["awards"]


# --------------------------------------------------------------------------- сборка


def snippet(text: str) -> str:
    """Короткое описание — та же логика, что у copySnippet на сайте."""
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= SNIPPET_MAX:
        return text
    cut = 0
    for m in SENTENCE_END.finditer(text):
        end = m.start() + 1
        if end > SNIPPET_MAX:
            break
        cut = end
    if cut >= SNIPPET_MIN:
        return text[:cut].strip()
    head = text[: SNIPPET_MAX - 1]
    space = head.rfind(" ")
    return (head[:space] if space > SNIPPET_MIN else head).strip() + "…"


def awards_for(code: str, awards: list) -> list[dict]:
    """Награды артикула: код назван в строке достижения либо перечислен в codes.
    Поздравления жюри (commendation) — документы, а не призы: пропускаем."""
    out = []
    for program in awards:
        for item in program["items"]:
            if item.get("commendation"):
                continue
            named = code in CODE_RE.findall(item.get("ru", ""))
            in_series = code in (item.get("codes") or [])
            if named or in_series:
                out.append({
                    "program": program["name"],
                    "year": item["year"],
                    "level_en": item["en"],
                    "level_ru": item["ru"],
                    "href": item.get("href"),
                    "series": not named and in_series,
                })
    return out


def urls_for(slug: str) -> dict[str, str]:
    return {
        lang: f"{SITE_URL}/catalog/{slug}" if lang == "ru" else f"{SITE_URL}/{lang}/catalog/{slug}"
        for lang in LOCALES
    }


def build_records(site_data: dict) -> list[dict]:
    catalog, copy, instock, awards = (
        site_data["catalog"], site_data["copy"], site_data["instock"], site_data["awards"],
    )
    records = []
    for p in catalog:
        code, slug = p["code"], p["slug"]
        cat = p["category"]
        if cat not in CATEGORIES:
            die(f"неизвестный раздел {cat!r} у {code} — добавьте его в CATEGORIES")
        ru_label, en_label, _, _ = CATEGORIES[cat]

        per_lang = {lang: copy[lang].get(code) for lang in LOCALES}
        gallery = [f"{SITE_URL}{g}" if g.startswith("/") else g
                   for g in dict.fromkeys([p["image"], *p.get("gallery", [])])]

        rec = {
            "code": code,
            "slug": slug,
            "category": cat,
            "category_label": {"ru": ru_label, "en": en_label},
            "type": {l: (c or {}).get("type") for l, c in per_lang.items()},
            "urls": urls_for(slug),
            "image": gallery[0] if gallery else None,
            "gallery": gallery,
            "gallery_total": p.get("galleryTotal", len(gallery)),
            "model3d": p.get("model3d") or None,
            "award_winning": bool((per_lang["ru"] or {}).get("awardWinning")),
            "awards": awards_for(code, awards),
            "in_stock_elements": [
                {"size": r.get("size"), "material_en": (r.get("material") or {}).get("en"),
                 "color_en": (r.get("color") or {}).get("en"), "qty": r.get("qty")}
                for r in instock.get(code, [])
            ],
            "description": {}, "where_it_works": {}, "style": {},
            "made_to_order": {}, "snippet": {},
        }
        for lang, c in per_lang.items():
            if not c:
                continue
            body = "\n\n".join(c.get("paragraphs") or [])
            rec["description"][lang] = body
            rec["where_it_works"][lang] = c.get("whereItWorks")
            rec["style"][lang] = c.get("style")
            rec["made_to_order"][lang] = c.get("madeToOrder")
            if body:
                rec["snippet"][lang] = snippet(body)
        records.append(rec)
    return records


# --------------------------------------------------------------------------- запись


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def product_page(rec: dict, lang: str) -> str:
    ru = lang == "ru"
    label = rec["category_label"]["ru" if ru else "en"]
    kind = rec["type"].get(lang) or rec["type"].get("en") or ""
    L = {
        "cat": "Раздел" if ru else "Category",
        "art": "Артикул" if ru else "Article code",
        "page": "Карточка" if ru else "Product page",
        "desc": "Описание" if ru else "Description",
        "where": "Где уместна" if ru else "Where it works",
        "style": "Стилистика" if ru else "Style",
        "order": "Изготовление" if ru else "Made to order",
        "aw": "Награды" if ru else "Awards",
        "img": "Снимки" if ru else "Images",
        "m3d": "3D-модель" if ru else "3D model",
        "stock": "Элементы в наличии" if ru else "Elements in stock",
        "series": "за серию" if ru else "for the series",
    }
    out = [f"# {kind} {rec['code']}".strip(), ""]
    out += [
        f"- {L['cat']}: {label}",
        f"- {L['art']}: {rec['code']}",
        f"- {L['page']}: {rec['urls'][lang]}",
    ]
    if rec["model3d"]:
        out.append(f"- {L['m3d']}: {rec['model3d']}")
    out.append("")

    if rec["description"].get(lang):
        out += [f"## {L['desc']}", "", rec["description"][lang], ""]
    if rec["where_it_works"].get(lang):
        out += [f"## {L['where']}", "", rec["where_it_works"][lang], ""]
    if rec["style"].get(lang):
        out += [f"## {L['style']}", "", rec["style"][lang], ""]
    if rec["made_to_order"].get(lang):
        out += [f"## {L['order']}", "", rec["made_to_order"][lang], ""]

    if rec["awards"]:
        out += [f"## {L['aw']}", ""]
        for a in rec["awards"]:
            line = f"- {a['program']} {a['year']} — {a['level_en'] if not ru else a['level_ru']}"
            if a["series"]:
                line += f" ({L['series']})"
            if a["href"]:
                line += f" — {a['href']}"
            out.append(line)
        out.append("")

    if rec["in_stock_elements"]:
        out += [f"## {L['stock']}", ""]
        for e in rec["in_stock_elements"]:
            bits = [b for b in (e["size"], e["color_en"], e["material_en"]) if b]
            out.append(f"- {', '.join(bits)} — {e['qty']}")
        out.append("")

    if rec["gallery"]:
        out += [f"## {L['img']}", ""]
        out += [f"{i}. {u}" for i, u in enumerate(rec["gallery"], 1)]
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def product_node(rec: dict) -> dict:
    """Product для schema.org. Без offers, material и размеров — правила владельца."""
    node = {
        "@type": "Product",
        "@id": f"{SITE_URL}/catalog/{rec['slug']}#product",
        "name": f"{rec['type'].get('en') or ''} {rec['code']}".strip(),
        "sku": rec["code"],
        "url": rec["urls"]["en"],
        "sameAs": [u for l, u in rec["urls"].items() if l != "en"],
        "image": rec["gallery"],
        "category": rec["category_label"]["en"],
        "brand": {"@id": ORG_ID},
        "manufacturer": {"@id": ORG_ID},
        "inLanguage": "en",
    }
    if rec["snippet"].get("en"):
        node["description"] = rec["snippet"]["en"]
    if rec["awards"]:
        node["award"] = [f"{a['program']} {a['year']} — {a['level_en']}" for a in rec["awards"]]
    return node


def en_view(rec: dict) -> dict:
    """Тот же товар, но одноязычно: английские тексты вместо словарей."""
    return {
        "code": rec["code"], "slug": rec["slug"], "category": rec["category"],
        "category_label": rec["category_label"]["en"], "type": rec["type"].get("en"),
        "url": rec["urls"]["en"], "urls": rec["urls"], "image": rec["image"],
        "gallery": rec["gallery"], "gallery_total": rec["gallery_total"],
        "model3d": rec["model3d"], "award_winning": rec["award_winning"],
        "awards": [{"program": a["program"], "year": a["year"], "level": a["level_en"],
                    "href": a["href"], "series": a["series"]} for a in rec["awards"]],
        "in_stock_elements": rec["in_stock_elements"],
        "description": rec["description"].get("en"),
        "where_it_works": rec["where_it_works"].get("en"),
        "style": rec["style"].get("en"),
        "made_to_order": rec["made_to_order"].get("en"),
        "snippet": rec["snippet"].get("en"),
    }


def write_datasets(recs: list[dict], base: Path, english: bool) -> None:
    rows = [en_view(r) for r in recs] if english else recs
    write(base / "products.json", json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    write(base / "products.jsonl",
          "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))

    with (base / "products.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["code", "category", "type_en", "url_en", "url_ru", "image",
                    "gallery_count", "award_winning", "awards", "snippet_en", "description_en"])
        for r in recs:
            w.writerow([
                r["code"], r["category"], r["type"].get("en") or "",
                r["urls"]["en"], r["urls"]["ru"], r["image"] or "",
                len(r["gallery"]), "yes" if r["award_winning"] else "",
                "; ".join(f"{a['program']} {a['year']} — {a['level_en']}" for a in r["awards"]),
                r["snippet"].get("en") or "", (r["description"].get("en") or "").replace("\n", " "),
            ])

    ru = not english
    by_cat: dict[str, list] = {}
    for r in recs:
        by_cat.setdefault(r["category"], []).append(r)
    head = "# Vargov Design — каталог\n" if ru else "# Vargov Design — catalogue\n"
    lines = [head, f"{'Всего композиций' if ru else 'Compositions'}: {len(recs)}\n",
             f"| {'Раздел' if ru else 'Section'} | {'Позиций' if ru else 'Items'} |", "|---|---|"]
    for cat, items in sorted(by_cat.items(), key=lambda kv: -len(kv[1])):
        lines.append(f"| {CATEGORIES[cat][0 if ru else 1]} | {len(items)} |")
    lines += ["", f"## {'Полный список' if ru else 'Full list'}", "",
              f"| {'Артикул' if ru else 'Code'} | {'Тип' if ru else 'Type'} | URL | {'Награды' if ru else 'Awards'} |",
              "|---|---|---|---|"]
    for r in sorted(recs, key=lambda x: x["code"]):
        lines.append(
            f"| {r['code']} | {r['type'].get('ru' if ru else 'en') or ''} "
            f"| {r['urls']['ru' if ru else 'en']} | {len(r['awards']) or ''} |"
        )
    write(base / "products.md", "\n".join(lines) + "\n")


def write_collections(recs: list[dict], base: Path, english: bool) -> None:
    ru = not english
    by_cat: dict[str, list] = {}
    for r in recs:
        by_cat.setdefault(r["category"], []).append(r)
    for cat, items in by_cat.items():
        ru_label, en_label, ru_href, en_href = CATEGORIES[cat]
        label = ru_label if ru else en_label
        href = SITE_URL + (ru_href if ru else en_href)
        lines = [f"# {label}", "", f"{'Раздел на сайте' if ru else 'Section'}: {href}", "",
                 f"{'Позиций' if ru else 'Items'}: {len(items)}", "",
                 f"## {'Состав' if ru else 'Contents'}", ""]
        for r in sorted(items, key=lambda x: x["code"]):
            rel = f"../products/{cat}/{r['code']}.md"
            lines.append(f"- [{r['code']}]({rel}) — {r['type'].get('ru' if ru else 'en') or ''} — {r['urls']['ru' if ru else 'en']}")
        write(base / f"{cat}.md", "\n".join(lines) + "\n")


def prune_stale(recs: list[dict]) -> list[str]:
    """Удаляем карточки эпохи Tilda: чужие разделы и артикулы вне 605."""
    live = {r["code"] for r in recs}
    removed = []
    for root in (KB / "products", KB / "en" / "products"):
        if not root.is_dir():
            continue
        for cat_dir in sorted(root.iterdir()):
            if not cat_dir.is_dir():
                continue
            if cat_dir.name not in CATEGORIES:
                removed.append(str(cat_dir.relative_to(KB)) + "/ (раздел эпохи Tilda)")
                shutil.rmtree(cat_dir)
                continue
            for md in sorted(cat_dir.glob("*.md")):
                if md.stem not in live:
                    removed.append(str(md.relative_to(KB)))
                    md.unlink()
    for dead in (KB / "vargov-schema-by-path.json", KB / "scan" / "products.jsonl",
                 KB / "scan" / "product_urls.txt", KB / "scan" / "failed_urls.txt"):
        if dead.exists():
            removed.append(str(dead.relative_to(KB)) + " (артефакт старого сканера)")
            dead.unlink()
    return removed


# --------------------------------------------------------------------------- main


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--site", type=Path, default=DEFAULT_SITE)
    args = ap.parse_args()

    print(f"Источник: {args.site}")
    site_data = load_site(args.site)
    recs = build_records(site_data)
    print(f"  композиций: {len(recs)}")

    for base, english in ((KB / "datasets", False), (KB / "en" / "datasets", True)):
        write_datasets(recs, base, english)
    for base, english in ((KB / "collections", False), (KB / "en" / "collections", True)):
        write_collections(recs, base, english)

    for r in recs:
        write(KB / "products" / r["category"] / f"{r['code']}.md", product_page(r, "ru"))
        write(KB / "en" / "products" / r["category"] / f"{r['code']}.md", product_page(r, "en"))

    graph = {"@context": "https://schema.org", "@graph": [product_node(r) for r in recs]}
    for p in (KB / "references" / "schema-products.jsonld", KB / "references" / "catalog.jsonld"):
        write(p, json.dumps(graph, ensure_ascii=False, indent=2) + "\n")

    write(KB / "vargov-products.json",
          json.dumps([en_view(r) for r in recs], ensure_ascii=False, indent=2) + "\n")

    removed = prune_stale(recs)
    write(KB / "scan" / "removed-stale.txt",
          "Удалено при пересборке (карточки и артефакты эпохи Tilda):\n\n" + "\n".join(removed) + "\n")

    # --- самопроверка -------------------------------------------------------
    problems = []
    if len(recs) < 500:
        problems.append(f"композиций всего {len(recs)}")
    gaps = {l: sum(1 for r in recs if not r["description"].get(l)) for l in LOCALES}
    for lang, n in gaps.items():
        if n:
            problems.append(f"нет описания на {lang}: {n}")
    for cat in CATEGORIES:
        n_ru = len(list((KB / "products" / cat).glob("*.md")))
        n_en = len(list((KB / "en" / "products" / cat).glob("*.md")))
        if n_ru != n_en:
            problems.append(f"{cat}: карточек RU {n_ru} против EN {n_en}")
    bad = [k for n in graph["@graph"] for k in ("offers", "price", "material", "size") if k in n]
    if bad:
        problems.append(f"в JSON-LD запрещённые поля: {sorted(set(bad))}")
    stale = subprocess.run(
        ["grep", "-rl", "-e", "tildacdn", "-e", "_vargovdesign_ru", "-e", "tproduct",
         "datasets", "en", "products", "collections", "references", "llms.txt", "llms-full.txt"],
        cwd=KB, capture_output=True, text=True,
    ).stdout.strip()
    if stale:
        problems.append("остались тильдовские адреса в: " + stale.replace("\n", ", ")[:300])

    print(f"  карточек: {len(recs) * 2} (RU+EN), узлов JSON-LD: {len(graph['@graph'])}")
    print(f"  наград привязано: {sum(len(r['awards']) for r in recs)}")
    print(f"  удалено устаревшего: {len(removed)}")
    if problems:
        print("\nПРОБЛЕМЫ:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("\nГотово, проверки пройдены.")


if __name__ == "__main__":
    main()
