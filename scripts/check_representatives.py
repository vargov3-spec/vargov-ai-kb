# -*- coding: utf-8 -*-
"""Проверка представителей: помечена ли выбранная карточка тегом своего артикула.

Зачем. В графе у артикула стоит одна карточка-представитель из тысяч в аккаунте.
Ошибиться легко: выгрузка своих карточек собирается ПО ТЕГУ и берёт первую из
выдачи, а тег базового артикула отдаёт и карточки вариантов. Так LC0406-1 вёл на
карточку LC0406, а LC0199 (торшер) — на декоративную перегородку.

Чем проверяем. references/3ddd-liveness.json — снимок ответов API по каждому
представителю (жив ли адрес и какие теги стоят НА карточке), снят агентом сайта
с его сервера; и references/3ddd-slug-tags.json — перепись агента сайта «слаг →
артикулы, под чьими тегами карточка найдена». Площадка не нужна: с машины
владельца 3ddd.ru всё равно недоступен.

Три оговорки, без которых проверка врёт (все проверены на живых данных):
  1) отсутствие слага в переписи НЕ значит, что карточки нет в аккаунте: в неё
     попали лишь карточки с тегом артикула каталога, 4064 из 5047;
  2) один слаг может стоять под несколькими артикулами — таких 79;
  3) у восьми артикулов тег пуст, их карточки помечены базовым артикулом; это
     известно и ошибкой не считается.

Спор «тег против реестра владельца» проверкой не решается — там смотрят
картинку: превью карточки против обложки изделия в каталоге.

    python scripts/check_representatives.py
"""
from __future__ import annotations

import json
from pathlib import Path

KB = Path(__file__).resolve().parent.parent


def main() -> int:
    idx = json.loads((KB / "references" / "3ddd-slug-tags.json").read_text(encoding="utf-8"))["items"]
    live_file = KB / "references" / "3ddd-liveness.json"
    live = json.loads(live_file.read_text(encoding="utf-8"))["items"] if live_file.is_file() else {}
    models = json.loads((KB / "references" / "3ddd-models.json").read_text(encoding="utf-8"))["items"]
    corr = json.loads((KB / "references" / "3ddd-corrections.json").read_text(encoding="utf-8"))
    empty, known = set(corr["empty_tags"]), set(corr.get("tag_wins", [])) | set(corr["slug_overrides"])

    unmarked, base_tag, absent = [], [], []
    for code, slug in sorted(models.items()):
        tags = idx.get(slug)
        if tags is None:
            absent.append((code, slug))
        elif code not in tags:
            (base_tag if code.split("-")[0] in tags else unmarked).append((code, slug, tags))

    # Живость. Проверить её отсюда нельзя — площадка с машины владельца не
    # открывается, — поэтому читаем снимок, снятый агентом сайта с его сервера.
    # Код ответа СТРАНИЦЫ для этого не годится: 3ddd отдаёт 200 на любой адрес.
    dead = [c for c, s in live.items() if c in models and s.get("status") != 200]
    stale = [c for c in models if c not in live]
    print(f"представителей: {len(models)}")
    if live:
        print(f"  живость (снимок {len(live)} адресов): мёртвых {len(dead)}" +
              (f" → {dead}" if dead else "") +
              (f", вне снимка {len(stale)} → {stale}" if stale else ""))
    else:
        print("  живость не проверена: нет references/3ddd-liveness.json")
    print(f"  помечены своим артикулом: {len(models) - len(unmarked) - len(base_tag) - len(absent)}")
    print(f"  помечены базовым артикулом: {len(base_tag)}" +
          (" — все с пустым тегом, известно" if all(c in empty for c, _, _ in base_tag) else ""))
    for c, s, _ in base_tag:
        if c not in empty:
            print(f"    ВНИМАНИЕ {c}: {s} — тег базового, а тег артикула не пуст")
    print(f"  нет в переписи: {len(absent)} — {[c for c, _ in absent]}")
    print("    (карточка без артикульного тега в перепись не попадает; это не значит, что её нет)")

    problems = [(c, s, t) for c, s, t in unmarked if c not in known]
    if dead:
        print(f"\nмёртвых адресов: {len(dead)} — заменить представителя")
        return 1
    if problems:
        print(f"\nпомечены ЧУЖИМ артикулом и не разобраны: {len(problems)}")
        for c, s, t in problems:
            print(f"  {c}: {s} → теги {t}")
        print("Сверить превью карточки с обложкой изделия — тег мог быть поставлен по составу.")
        return 1
    print("\nПроверка пройдена: чужих карточек среди представителей нет.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
