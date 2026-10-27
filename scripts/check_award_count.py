#!/usr/bin/env python3
"""
Сторож числа наград в ТЕКСТАХ базы знаний.

ЗАЧЕМ. Граф базы (references/*.jsonld, датасеты) пересобирается из фида сайта и
сверяется с ним check_feed_parity.py. А число наград в llms-файлах, README,
пресс-ките и прочих текстах вписано словами и живёт само по себе: 13.09.2026
после появления 24-й награды llms.txt и llms-full.txt остались с числом 23 —
и это первый файл, который читают ИИ-обходчики. 19.10.2026 ровно так же молча
разошлись hasCertification и sameAs, и нашла их ночная сверка, а не человек.

КАК. Эталон — число записей `award` у Organization в references/organization.jsonld;
его пишет ночная сверка из фида сайта, то есть из `awardsCount()` первоисточника.
Ниже — явный перечень мест, где число должно быть текущим. Исторические упоминания
(«на 03.10.2026 было 25», «22, 23, 24 — устаревшие») сюда НЕ входят намеренно:
сторож знает свой объём и не угадывает по контексту.

ЕСЛИ ЯКОРЬ НЕ НАЙДЕН — это тоже ошибка: значит текст переписали, а сторож ослеп
и дальше молчал бы на любом числе.

Запуск: python scripts/check_award_count.py   (код 1 при расхождении)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KB = Path(__file__).resolve().parent.parent

# (файл, регулярное выражение с одной группой — числом)
ANCHORS: list[tuple[str, str]] = [
    ("llms.txt", r"(\d+) достижений на международных премиях"),
    ("llms.txt", r"Награды — (\d+), в 16 программах"),
    ("llms.txt", r"awards-verified\.md\) — (\d+) наград со ссылками"),
    ("en/llms.txt", r"(\d+) awards from international juries\."),
    ("en/llms.txt", r"(\d+) awards across 16 programmes"),
    ("en/llms.txt", r"awards-verified\.md\) — (\d+) awards with links"),
    ("zh/llms.txt", r"(\d+) 项国际评委会奖项"),
    ("zh/llms.txt", r"16 个奖项计划共 (\d+) 项奖项"),
    ("zh/llms.txt", r"awards-verified\.md\) — (\d+) 项奖项"),
    # llms-full.txt собирается из llms.txt и en/llms.txt дословно — проверяем обе половины.
    ("llms-full.txt", r"(\d+) достижений на международных премиях"),
    ("llms-full.txt", r"(\d+) awards from international juries\."),
    ("README.md", r"Organization \(бренд, (\d+) наград"),
    ("README.md", r"дословно из `awards\.ts`: (\d+) наград"),
    ("en/README.md", r"(\d+) awards from international juries"),
    ("knowledge/brand.md", r"## Награды — (\d+)"),
    ("knowledge/brand.md", r"`awardsCount\(\)` = (\d+);"),
    ("knowledge/awards-verified.md", r"`awardsCount\(\)` = \*\*(\d+)\*\*"),
    ("knowledge/awards-verified.md", r"^## (\d+) наград"),
    ("knowledge/awards-verified.md", r"- наград \*\*(\d+)\*\*;"),
    ("knowledge/awards-verified.md", r"Итого (\d+)\."),
    ("knowledge/awards-verified.md", r"\*\*на \d\d\.\d\d\.\d{4} это (\d+)\*\*"),
    ("knowledge/pr-kit.md", r"Источник — `awards\.ts` сайта, (\d+) наград в 16 программах"),
    ("knowledge/pr-kit.md", r"## Число наград: (\d+),"),
    ("knowledge/pr-kit.md", r"- Награды: (\d+) достижений"),
    ("knowledge/threads-brand-facts.md", r"> (\d+) awards from international juries across 16 programmes"),
    ("knowledge/threads-brand-facts.md", r"(\d+) достижений на международных"),
    ("datasets/hf-README.md", r"True for \d+ records: (\d+) awards"),
]


def expected() -> int:
    data = json.loads((KB / "references" / "organization.jsonld").read_text(encoding="utf-8"))
    nodes = data.get("@graph", [data])
    org = next((n for n in nodes if n.get("@type") == "Organization"), None)
    if org is None:
        sys.exit("ОСТАНОВ: в references/organization.jsonld нет узла Organization")
    n = len(org.get("award", []))
    if n < 20:
        sys.exit(f"ОСТАНОВ: у Organization {n} наград — похоже на обнулённый файл, сверять не с чем")
    return n


def main() -> int:
    want = expected()
    bad: list[str] = []
    for rel, pattern in ANCHORS:
        path = KB / rel
        if not path.is_file():
            bad.append(f"{rel}: файла нет")
            continue
        text = path.read_text(encoding="utf-8")
        found = re.findall(pattern, text, re.MULTILINE)
        if not found:
            bad.append(f"{rel}: место не найдено по шаблону {pattern!r} — текст переписали, "
                       f"сторож ослеп; поправьте ANCHORS")
            continue
        wrong = sorted({v for v in found if int(v) != want})
        if wrong:
            bad.append(f"{rel}: {pattern!r} → {', '.join(wrong)}, а наград {want}")

    print(f"эталон (organization.jsonld): {want} наград; мест под присмотром: {len(ANCHORS)}")
    if bad:
        print("\nРАСХОЖДЕНИЯ:")
        for b in bad:
            print(" -", b)
        print("\nЧисло правится руками во всех местах сразу; эталон приходит из фида сайта "
              "(awardsCount()) ночной сверкой.")
        return 1
    print("Число наград в текстах совпадает с графом.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
