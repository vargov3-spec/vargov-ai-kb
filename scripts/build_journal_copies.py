# -*- coding: utf-8 -*-
"""Печатает копии журнала из пакета integration/journal.json.

    python scripts/build_journal_copies.py            # переписать копии по пакету
    python scripts/build_journal_copies.py --check    # только сверить; расхождение -> код выхода 1

Пакет integration/journal.json — единственный источник текстов «Прямой речи» (его же читает
scripts/build-journal.mjs сайта). Копии в базе руками НЕ правятся — только этим скриптом,
иначе они расходятся с пакетом (находки аудита 03.10.2026 A120, A335):

  content/journal/<lang>/<slug>.md      — по файлу на статью и язык; статьи с
                                          articleMeta[slug].retired = true не печатаются,
                                          md без статьи в пакете удаляются;
  datasets/journal/<slug>.json          — для каждого уже лежащего датасета обновляются
                                          поля articles и articleMeta; свои поля файла
                                          (cover, accent, slug) не трогаются.

Формат md: «# заголовок», строка рубрики/даты/слага, лид, блоки через пустую строку;
блок li — с «- ». Перевод строки LF, в конце md — один перевод строки; датасет — JSON
с отступом 1 и без перевода строки в конце (как было до скрипта).
После правки пакета: пересчитать meta.checksum, запустить этот скрипт, затем --check.
"""
import argparse, glob, json, os, sys

ap = argparse.ArgumentParser()
ap.add_argument("--check", action="store_true", help="ничего не писать, только сверить")
ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                help="корень базы знаний (по умолчанию — каталог над scripts/)")
args = ap.parse_args()
KB = args.root

pkg = json.load(open(os.path.join(KB, "integration", "journal.json"), encoding="utf-8"))
A, META = pkg["articles"], pkg.get("articleMeta", {})
LANGS = pkg["meta"]["locales"]
if list(A) != list(META):
    sys.exit("пакет: состав articles и articleMeta различается")
PRINT = [s for s in A if not META[s].get("retired")]


def render(slug, a):
    m = a["metaLabels"]
    parts = ["# " + a["title"], f"{m['category']}: {a['category']} · {m['date']}: {a['date']} · Slug: {slug}", a["lead"]]
    for b in a["body"]:
        parts.append(("- " + b["text"]) if b["type"] == "li" else b["text"])
    return ("\n\n".join(parts) + "\n").encode("utf-8")


def read(p):
    return open(p, "rb").read().replace(b"\r\n", b"\n") if os.path.exists(p) else None


diff = []  # (действие, путь)
for slug in PRINT:
    for lang in LANGS:
        p = os.path.join(KB, "content", "journal", lang, slug + ".md")
        new = render(slug, A[slug][lang])
        old = read(p)
        if old != new:
            diff.append(("создать" if old is None else "переписать", p))
            if not args.check:
                os.makedirs(os.path.dirname(p), exist_ok=True)
                open(p, "wb").write(new)

for lang in LANGS:
    for p in glob.glob(os.path.join(KB, "content", "journal", lang, "*.md")):
        if os.path.splitext(os.path.basename(p))[0] not in PRINT:
            diff.append(("удалить", p))
            if not args.check:
                os.remove(p)

for p in sorted(glob.glob(os.path.join(KB, "datasets", "journal", "*.json"))):
    d = json.load(open(p, encoding="utf-8"))
    slug = d.get("slug") or os.path.splitext(os.path.basename(p))[0]
    if slug not in A:
        diff.append(("нет статьи в пакете для датасета", p))
        continue
    d["articles"] = A[slug]
    d["articleMeta"] = META[slug]
    new = json.dumps(d, ensure_ascii=False, indent=1).encode("utf-8")
    if read(p) != new:
        diff.append(("переписать", p))
        if not args.check:
            open(p, "wb").write(new)

if not args.check:  # после записи копии обязаны совпасть с пакетом
    for lang in LANGS:
        have = sorted(os.path.splitext(os.path.basename(p))[0]
                      for p in glob.glob(os.path.join(KB, "content", "journal", lang, "*.md")))
        if have != sorted(PRINT):
            sys.exit(f"content/journal/{lang}: {len(have)} md при {len(PRINT)} статьях к печати")

for what, p in diff:
    print(f"  {what}: {os.path.relpath(p, KB)}")
broken = [d for d in diff if d[0].startswith("нет статьи")]
mode = "сверка" if args.check else "печать"
print(f"{mode}: пакет {pkg['meta']['checksum']}, статей {len(A)} (к печати {len(PRINT)}) x {len(LANGS)} языков; "
      f"{'расхождений' if args.check else 'изменений'}: {len(diff)}")
sys.exit(1 if (args.check and diff) or broken else 0)
