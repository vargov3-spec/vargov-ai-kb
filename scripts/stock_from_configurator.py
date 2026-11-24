#!/usr/bin/env python3
"""
Точечно обновить «Элементы в наличии» в базе знаний по stock-sizes.json конфигуратора.

ЗАЧЕМ ОТДЕЛЬНО ОТ build_from_site.py. Полная пересборка трогает все 605 карточек и
датасеты целиком (описания, снимки, награды) — а их между пересборками правит ночная
сверка с фидом (sync_from_feed.py). Здесь меняется только наличие:
  products/<раздел>/<артикул>.md, en/products/<раздел>/<артикул>.md — раздел наличия;
  datasets/products.json(l), en/datasets/products.json(l) — поле in_stock_elements.
Разметка раздела и поля — те же функции, что в build_from_site.py (stock_section,
stock_dataset), так что полная пересборка даст тот же текст.

Размер — подписью конфигуратора, не записью склада (владелец 24.11.2026, см.
STOCK_SIZES в build_from_site.py).

Запуск:
  python -I scripts/stock_from_configurator.py --check   # только показать, что изменится
  python -I scripts/stock_from_configurator.py           # записать
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_from_site as B  # noqa: E402

KB = B.KB
SECTION = {"ru": "Элементы в наличии", "en": "Elements in stock"}
IMAGES = {"ru": "Снимки", "en": "Images"}


def cards(lang: str) -> dict[str, Path]:
    base = KB / "products" if lang == "ru" else KB / "en" / "products"
    return {p.stem: p for p in base.glob("*/*.md")}


def rewrite_card(text: str, code: str, lang: str) -> str:
    head = f"## {SECTION[lang]}"
    # Убрать прежний раздел: от заголовка до следующего «## » или конца файла.
    text = re.sub(rf"(?ms)^{re.escape(head)}\n.*?(?=^## |\Z)", "", text)
    new = B.stock_section(B.STOCK, code, lang)
    if not new:
        return text.rstrip() + "\n"
    block = "\n".join(new) + "\n"
    img = re.search(rf"(?m)^## {re.escape(IMAGES[lang])}\n", text)
    if img:  # build_from_site ставит наличие прямо перед снимками
        return text[:img.start()] + block + text[img.start():]
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", type=Path, default=B.STOCK_SIZES)
    ap.add_argument("--check", action="store_true", help="ничего не писать, только показать")
    args = ap.parse_args()

    raw = json.loads(args.src.read_text(encoding="utf-8"))
    stock = B.load_stock(args.src)
    print(f"Источник: {args.src}\n  собран {raw.get('builtAt')}, склад на "
          f"{raw.get('stockUpdatedAt')}; позиций {sum(map(len, stock.values()))}, артикулов {len(stock)}")

    changed: list[str] = []
    for lang in ("ru", "en"):
        have = cards(lang)
        orphan = sorted(set(stock) - set(have))
        if orphan:
            print(f"  ! {lang}: на складе, но карточки нет: {', '.join(orphan)}")
        for code, path in sorted(have.items()):
            old = path.read_text(encoding="utf-8")
            new = rewrite_card(old, code, lang)
            if new != old:
                changed.append(str(path.relative_to(KB)).replace("\\", "/"))
                if not args.check:
                    B.write(path, new)

    for base in (KB / "datasets", KB / "en" / "datasets"):
        pj, pl = base / "products.json", base / "products.jsonl"
        rows = json.loads(pj.read_text(encoding="utf-8"))
        n = 0
        for r in rows:
            v = B.stock_dataset(stock, r["code"])
            if r.get("in_stock_elements") != v:
                r["in_stock_elements"] = v
                n += 1
        if n:
            changed += [str(p.relative_to(KB)).replace("\\", "/") + f" ({n} записей)" for p in (pj, pl)]
            if not args.check:
                B.write(pj, json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
                B.write(pl, "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))

    print(f"{'Изменится' if args.check else 'Изменено'} файлов: {len(changed)}")
    for c in changed:
        print("  ", c)


if __name__ == "__main__":
    main()
