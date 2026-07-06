"""
Builds the Russian-language knowledge base (products/, collections/,
datasets/, references/) plus the two root-level files consumed by the
live vargov.ru integration (vargov-products.json, vargov-schema-by-path.json)
from scan/products.jsonl produced by scrape_products.py.
"""
import json, os, csv, re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIR = ROOT / "scan"
PRODUCTS_JSONL = SCAN_DIR / "products.jsonl"

CAT_MAP = {
    "lighting_compositions_vargovdesign_ru": ("lighting-compositions", "Световые композиции", "Lighting compositions"),
    "decorative_compositions_vargovdesign_ru": ("decorative-compositions", "Декоративные композиции", "Decorative compositions"),
    "decor_and_sculptural_compositions_vargovdesign_ru": ("sculptural-decor", "Скульптурные композиции, декор", "Sculptural compositions & decor"),
    "floorlamps_and_tablelamps_vargovdesign_ru": ("floor-table-lamps", "Торшеры, бра, настольные арт-объекты", "Floor lamps, sconces & tabletop art objects"),
    "official_showroom_vargovdesign": ("showroom-items", "Товары шоурума", "Showroom items"),
    "elements_in_stock": ("stock-elements", "Элементы в наличии", "Elements in stock"),
}


def load_products():
    seen = {}
    with open(PRODUCTS_JSONL, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            seen[d["url"]] = d
    return list(seen.values())


def safe_id(p):
    if p.get("sku"):
        return re.sub(r"[^A-Za-z0-9_-]", "_", p["sku"])
    return str(p.get("uid") or "unknown")


def build():
    products = load_products()
    print("Loaded", len(products), "unique products")

    for p in products:
        slug, ru, en = CAT_MAP.get(p["category"], (p["category"], p["category"], p["category"]))
        p["category_slug"] = slug
        p["category_ru"] = ru
        p["category_en"] = en

    by_cat = {}
    for p in products:
        by_cat.setdefault(p["category_slug"], []).append(p)

    # products/<category>/<id>.md
    prod_dir = ROOT / "products"
    for slug, items in by_cat.items():
        cat_dir = prod_dir / slug
        cat_dir.mkdir(parents=True, exist_ok=True)
        for p in items:
            pid = safe_id(p)
            title = p.get("title") or p["category_ru"]
            desc = p.get("description") or ""
            gallery = p.get("gallery") or []
            price = p.get("price") or ""
            lines = [
                f"# {title} ({p.get('sku') or pid})", "",
                f"- Категория: {p['category_ru']} ({p['category_en']})",
                f"- Артикул (SKU): {p.get('sku') or 'не указан'}",
                f"- Источник: {p['url']}",
                f"- Цена: {price}" if price else "- Цена: по запросу (не публикуется на сайте)",
                "", "## Описание (как на сайте)",
                desc if desc else "_Описание на сайте не заполнено._", "",
            ]
            if gallery:
                lines.append("## Изображения")
                lines += [f"{i}. {img}" for i, img in enumerate(gallery, 1)]
                lines.append("")
            lines += [
                "## Примечание",
                "Технические характеристики (материалы, размеры, цвет, температура света) на сайте для данной позиции не опубликованы отдельно — уточняются у бренда индивидуально по запросу.",
            ]
            (cat_dir / f"{pid}.md").write_text("\n".join(lines), encoding="utf-8")

    # collections/<category>.md
    coll_dir = ROOT / "collections"
    coll_dir.mkdir(exist_ok=True)
    for slug, items in by_cat.items():
        ru = items[0]["category_ru"]
        en = items[0]["category_en"]
        src_cat = items[0]["category"]
        lines = [f"# {ru} / {en}", "",
                 f"Источник категории: https://vargov.ru/{src_cat}", "",
                 f"Товаров в коллекции: {len(items)}", "", "## Список товаров"]
        for p in sorted(items, key=lambda x: x.get("sku") or ""):
            pid = safe_id(p)
            lines.append(f"- [{p.get('sku') or pid}](../products/{slug}/{pid}.md) — {p['url']}")
        (coll_dir / f"{slug}.md").write_text("\n".join(lines), encoding="utf-8")

    # datasets/
    ds_dir = ROOT / "datasets"
    ds_dir.mkdir(exist_ok=True)
    (ds_dir / "products.json").write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")
    with open(ds_dir / "products.jsonl", "w", encoding="utf-8") as f:
        for p in products:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    with open(ds_dir / "products.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sku", "uid", "category_slug", "category_ru", "title", "url", "price", "image_count", "first_image", "description"])
        for p in products:
            w.writerow([p.get("sku") or "", p.get("uid") or "", p["category_slug"], p["category_ru"],
                        p.get("title") or "", p["url"], p.get("price") or "",
                        len(p.get("gallery") or []), (p.get("gallery") or [""])[0],
                        (p.get("description") or "")[:500]])
    with open(ds_dir / "products.md", "w", encoding="utf-8") as f:
        f.write("# Vargov Design — сводная таблица товаров\n\n")
        f.write(f"Всего товаров собрано: {len(products)}\n\n| Категория | Кол-во |\n|---|---|\n")
        for slug, items in sorted(by_cat.items(), key=lambda x: -len(x[1])):
            f.write(f"| {items[0]['category_ru']} | {len(items)} |\n")
        f.write("\n## Полный список\n\n| SKU | Категория | URL |\n|---|---|---|\n")
        for p in sorted(products, key=lambda x: (x["category_slug"], x.get("sku") or "")):
            f.write(f"| {p.get('sku') or safe_id(p)} | {p['category_ru']} | {p['url']} |\n")

    # references/ + root files consumed by the live Tilda head-code script
    ref_dir = ROOT / "references"
    ref_dir.mkdir(exist_ok=True)
    graph = []
    by_path = {}
    for p in products:
        node = {
            "@type": "Product", "@id": p["url"], "url": p["url"],
            "name": p.get("title") or p["category_ru"], "sku": p.get("sku"),
            "category": p["category_en"], "description": (p.get("description") or "")[:1000] or None,
            "brand": {"@type": "Brand", "name": "Vargov Design"},
            "manufacturer": {"@type": "Organization", "name": "Vargov Design"},
            "image": p.get("gallery") or None,
            "offers": {"@type": "Offer", "priceCurrency": "USD",
                       "availability": "https://schema.org/PreOrder", "url": p["url"]},
        }
        node = {k: v for k, v in node.items() if v is not None}
        graph.append(node)
        by_path[urlparse(p["url"]).path] = node

    (ref_dir / "schema-products.jsonld").write_text(
        json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2),
        encoding="utf-8")

    # root files (what llms.txt and the Tilda head script actually fetch)
    (ROOT / "vargov-products.json").write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "vargov-schema-by-path.json").write_text(
        json.dumps(by_path, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    stats = {"total_products": len(products), "by_category": {s: len(i) for s, i in by_cat.items()}}
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    return products


if __name__ == "__main__":
    build()
