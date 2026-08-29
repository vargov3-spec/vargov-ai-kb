# -*- coding: utf-8 -*-
"""Разведка перед перестройкой заголовков: что вообще можно вытащить из каталога.

Заголовок пина должен состоять из слов, которые люди набирают в поиске.
У нас есть тип изделия (он уже размечен), но нужны ещё два ингредиента:
помещение («в гостиную», «над лестницей») и форма («каскад», «кольцо»).
Прежде чем строить на них заголовки, надо померить, у скольких моделей они
вообще определяются — иначе получится схема, работающая на пяти процентах.

Совпадение только по границам слов: наивная подстрока ловит «сот» из «сотни»
и «лист» из «листва», давая 600 ложных попаданий из 605.
"""
import collections
import io
import json
import re
from pathlib import Path

CAT = Path("data/site-catalog.json")

# Помещение засчитываем от двух упоминаний: шаблонное перечисление применений
# («подходит для гостиных, холлов, ресторанов») встречается почти везде и
# ничего не говорит о конкретной модели.
SPACES = [
    (re.compile(r"лестниц|марш[еа]|пролёт", re.I), "над лестницей", "for a Staircase"),
    (re.compile(r"двусветн|двойной высот|высок[ими]+ потолк", re.I), "в двусветную гостиную", "for a Double-Height Room"),
    (re.compile(r"обеденн|над столом|столов[ойая]", re.I), "над обеденным столом", "for a Dining Table"),
    (re.compile(r"гостин", re.I), "в гостиную", "for a Living Room"),
    (re.compile(r"лобби|отел[ея]|холл", re.I), "для лобби", "for a Hotel Lobby"),
    (re.compile(r"ресторан|бар[ае]?\b", re.I), "для ресторана", "for a Restaurant"),
    (re.compile(r"спальн", re.I), "в спальню", "for a Bedroom"),
    (re.compile(r"ванн|санузл", re.I), "в ванную", "for a Bathroom"),
    (re.compile(r"кабинет|переговорн|офис", re.I), "в кабинет", "for an Office"),
]
SPACE_MIN_HITS = 2

# Формы — то, что реально набирают: «cascade chandelier», «bubble chandelier».
# Ключ — регулярка по основе слова, чтобы ловить падежи, но не чужие слова.
FORMS = [
    (re.compile(r"\bкаскад\w*", re.I), "каскад", "Cascade"),
    (re.compile(r"\bкольц\w*|\bобруч\w*", re.I), "кольцо", "Ring"),
    (re.compile(r"\bсфер\w*|\bшар(?:\w{0,3})\b", re.I), "сферы", "Spheres"),
    (re.compile(r"\bпузыр\w*", re.I), "пузыри", "Bubbles"),
    (re.compile(r"\bдиск\w*", re.I), "диски", "Discs"),
    (re.compile(r"\bветв\w*|\bветк\w*", re.I), "ветви", "Branches"),
    (re.compile(r"\bволн\w*", re.I), "волна", "Wave"),
    (re.compile(r"\bспирал\w*", re.I), "спираль", "Spiral"),
    (re.compile(r"\bярус\w*", re.I), "ярусы", "Tiers"),
    (re.compile(r"\bкапл\w*|\bкапел\w*", re.I), "капли", "Drops"),
    (re.compile(r"\bоблак\w*|\bоблач\w*", re.I), "облако", "Cloud"),
    (re.compile(r"\bгроздь\w*|\bгрозд\w*", re.I), "гроздь", "Cluster"),
    (re.compile(r"\bперьев\w*|\bперо\b|\bперья\w*", re.I), "перья", "Feathers"),
    (re.compile(r"\bкупол\w*", re.I), "купол", "Dome"),
    (re.compile(r"\bдуг[аиуой]\b|\bдуг\w*", re.I), "дуга", "Arc"),
    (re.compile(r"\bсетк\w*|\bрешётк\w*", re.I), "сетка", "Mesh"),
    (re.compile(r"\bпластин\w*", re.I), "пластины", "Plates"),
    (re.compile(r"\bстержн\w*|\bстерж\w*", re.I), "стержни", "Rods"),
    (re.compile(r"\bлепестк\w*|\bлепест\w*", re.I), "лепестки", "Petals"),
    (re.compile(r"\bлист[ья]\w*|\bлиств\w*", re.I), "листья", "Leaves"),
]


def detect(rx_list, blob, min_hits=1):
    for rx, ru, en in rx_list:
        if len(rx.findall(blob)) >= min_hits:
            return ru, en
    return "", ""


def main():
    cat = json.loads(CAT.read_text(encoding="utf-8"))
    have_space = have_form = 0
    space_c, form_c = collections.Counter(), collections.Counter()
    samples = []

    for sku, rec in sorted(cat.items()):
        blob = " ".join(str(rec.get(f) or "") for f in
                        ("nameRu", "descrRu", "descrFullRu"))
        s_ru, s_en = detect(SPACES, blob, SPACE_MIN_HITS)
        f_ru, f_en = detect(FORMS, blob)
        if s_ru:
            have_space += 1
            space_c[s_ru] += 1
        if f_ru:
            have_form += 1
            form_c[f_ru] += 1
        if len(samples) < 12 and (s_ru or f_ru):
            samples.append((sku, rec.get("categoryRu", ""), s_ru, f_ru))

    n = len(cat)
    out = io.open("probe-search.txt", "w", encoding="utf-8")
    out.write("Всего SKU: %d\n\n" % n)
    out.write("ПОМЕЩЕНИЕ определилось у %d (%.0f%%)\n" % (have_space, 100 * have_space / n))
    for k, v in space_c.most_common():
        out.write("   %-26s %4d\n" % (k, v))
    out.write("\nФОРМА определилась у %d (%.0f%%)\n" % (have_form, 100 * have_form / n))
    for k, v in form_c.most_common():
        out.write("   %-16s %4d\n" % (k, v))
    both = sum(1 for sku, rec in cat.items()
               if detect(SPACES, " ".join(str(rec.get(f) or "") for f in
                                          ("nameRu", "descrRu", "descrFullRu")), SPACE_MIN_HITS)[0]
               and detect(FORMS, " ".join(str(rec.get(f) or "") for f in
                                          ("nameRu", "descrRu", "descrFullRu")))[0])
    out.write("\nОБА признака: %d (%.0f%%)\n" % (both, 100 * both / n))
    out.write("\nПРИМЕРЫ:\n")
    for sku, cat_ru, s, f in samples:
        out.write("   %s  %-26s помещение=%-22s форма=%s\n" % (sku, cat_ru[:26], s or "—", f or "—"))
    out.close()
    print(Path("probe-search.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
