# -*- coding: utf-8 -*-
"""Заголовки пинов от поискового запроса, а не от артикула.

Замер 29.08.2026 показал: за четыре месяца охват вырос в 66 раз, а доля
показов, доходящих до сайта, не сдвинулась — 0,09%% весь период. Верх воронки
расширили, проходимость не тронули. Заголовок и есть та проходимость: поиск
Pinterest текстовый, и «Композиция о взмахе» не совпадает ни с одним запросом
живого человека, тогда как «Люстра-каскад из стекла» совпадает.

Из чего собираем (проверено probeSearch.py на 605 моделях):
  тип      — размечен по названию, есть у всех;
  форма    — «каскад», «облако», «кольцо»: есть у 82%%, главный отличительный
             признак и одновременно живой поисковый запрос;
  цвет     — «золото», «дымчатое», «чёрное»: тоже ищут, дополняет форму;
  помещение— есть лишь у 19%%, поэтому не опора, а бонус, когда уверенно видно.

Материал в отличители не годится: у всех 600 моделей он буквально одинаковый
(«стекло, хрусталь, керамика, металл»), заголовки по нему схлопываются в дубли.

Артикул оставлен в хвосте: он занимает 22 символа из 100, но гарантирует
уникальность заголовка и нужен покупателю, который знает модель. Поисковые
слова при этом стоят впереди, где они и работают.
"""
from __future__ import annotations

import collections
import io
import json
import re
from pathlib import Path

CAT = Path("data/site-catalog.json")
TITLE_MAX = 100

# --- тип изделия -------------------------------------------------------------
# Источник — board-map.json, а не разбор названия: доски размечены по тому, как
# изделие вешается (подвес, стена, пол), и это единственная надёжная физическая
# классификация, которая у нас есть. Название на сайте говорит «декоративная
# композиция» — по такому запросу в Pinterest не ищут вообще никто.
BOARD_TYPE = {
    "Pendant Lighting & Chandeliers": ("Люстра", "Chandelier"),
    "Glass Art & Light Sculptures":   ("Световая скульптура", "Glass Light Sculpture"),
    "Wall Sconces & Wall Lighting":   ("Настенный светильник", "Wall Sconce"),
    "Floor & Table Lamps":            ("Торшер", "Floor Lamp"),
    "Hotel & Restaurant Lighting":    ("Люстра", "Chandelier"),
}
# На доске напольных лежат и торшеры, и настольные — различаем по названию.
TABLE_RX = re.compile(r"настольн", re.I)

# --- форма: главный отличитель и живой запрос --------------------------------
# Совпадение по границам слов: наивная подстрока ловит «сот» из «сотни».
# ru_attr — форма как определение к типу («люстра-каскад»).
FORMS = [
    (r"\bкаскад\w*", "каскад", "Cascade"),
    (r"\bпузыр\w*", "пузыри", "Bubble"),
    (r"\bоблак\w*|\bоблач\w*", "облако", "Cloud"),
    (r"\bкольц\w*|\bобруч\w*", "кольцо", "Ring"),
    (r"\bсфер\w*", "сферы", "Sphere"),
    (r"\bветв\w*|\bветк\w*", "ветви", "Branch"),
    (r"\bволн\w*", "волна", "Wave"),
    (r"\bспирал\w*", "спираль", "Spiral"),
    (r"\bярус\w*", "ярусы", "Tiered"),
    (r"\bкапл\w*|\bкапел\w*", "капли", "Droplet"),
    (r"\bдиск\w*", "диски", "Disc"),
    (r"\bгроздь\w*|\bгрозд\w*", "гроздь", "Cluster"),
    (r"\bсетк\w*|\bрешётк\w*", "сетка", "Mesh"),
    (r"\bперьев\w*|\bперья\w*|\bперо\b", "перья", "Feather"),
    (r"\bлепестк\w*", "лепестки", "Petal"),
    (r"\bпластин\w*", "пластины", "Plate"),
    (r"\bстержн\w*", "стержни", "Rod"),
    (r"\bлист[ья]\w*|\bлиств\w*", "листья", "Leaf"),
    (r"\bкупол\w*", "купол", "Dome"),
    (r"\bдуг[аиуой]\b|\bдугообразн\w*", "дуга", "Arc"),
    (r"\bкристалл\w*", "кристаллы", "Crystal"),
    (r"\bснежин\w*", "снежинки", "Snowflake"),
    (r"\bзвёзд\w*|\bзвезд\w*", "звёзды", "Star"),
    (r"\bлент[аыуойе]\w*", "ленты", "Ribbon"),
    (r"\bтрубк\w*|\bтруб[аыуой]\b", "трубки", "Tube"),
    (r"\bсосульк\w*", "сосульки", "Icicle"),
]
FORMS = [(re.compile(p, re.I), ru, en) for p, ru, en in FORMS]

# --- цвет и отделка: тоже поисковые слова ------------------------------------
# Русский вариант хранится готовой именной группой в среднем роде («золотое
# стекло»): она цепляется к слову «стекло», а не к типу, поэтому род типа
# («люстра» ж, «торшер» м) на согласование не влияет и склонять ничего не нужно.
# Латунь и медь — это металл, а не стекло, поэтому у них своя формулировка.
# Порядок: сначала редкое и характерное, потом общее — «прозрачное» есть почти
# везде и перехватило бы всё остальное.
TONES = [
    # Дымчатое семейство собрано широко: у этих вещей «серый дым», «графит» и
    # «стальные блики» описывают один и тот же оттенок, и по отдельности каждое
    # слово встречается реже, чем проходное «белый» из соседнего предложения.
    (r"\bдымчат\w*|\bдым\w*|\bграфит\w*|\bстальн\w*|\bсер[ыаоуи]\w*", "дымчатое стекло", "Smoked Glass"),
    (r"\bянтарн\w*", "янтарное стекло", "Amber Glass"),
    (r"\bмолочн\w*|\bопалов\w*", "молочное стекло", "Opal Glass"),
    (r"\bлатун\w*", "латунь и стекло", "Brass"),
    (r"\bмедн\w*|\bмед[ьи]\b", "медь и стекло", "Copper"),
    (r"\bзолот\w*|\bпозолот\w*", "золотое стекло", "Gold"),
    (r"\bчёрн\w*|\bчерн\w*", "чёрное стекло", "Black"),
    (r"\bбел\w*", "белое стекло", "White"),
    (r"\bпрозрачн\w*", "прозрачное стекло", "Clear Glass"),
]
TONES = [(re.compile(p, re.I), ru, en) for p, ru, en in TONES]

# --- помещение: бонус, а не опора --------------------------------------------
# Два упоминания минимум: шаблонное перечисление применений есть почти везде.
# «Ванная» намеренно исключена: у премиальных люстр совпадения оказались
# метафорами, а ошибочная метка отправит пин не той аудитории.
SPACES = [
    (r"лестниц|пролёт", "над лестницей", "for a Staircase"),
    (r"двусветн|двойной высот|высок\w* потолк", "в двусветную гостиную", "for a Double-Height Room"),
    (r"обеденн|над столом", "над обеденным столом", "for a Dining Table"),
    (r"лобби|отел[ея]", "для лобби отеля", "for a Hotel Lobby"),
    (r"ресторан", "для ресторана", "for a Restaurant"),
    (r"гостин", "в гостиную", "for a Living Room"),
    (r"кабинет|переговорн", "в кабинет", "for an Office"),
    (r"спальн", "в спальню", "for a Bedroom"),
]
SPACES = [(re.compile(p, re.I), ru, en) for p, ru, en in SPACES]
SPACE_MIN_HITS = 2

# --- углы: чем различать пины одной модели в разных волнах --------------------
# Русские углы — только несклоняемые обороты: они встают в строку после любого
# типа, не требуя согласования по роду («Люстра-каскад ручной работы»,
# «Торшер-спираль ручной работы»).
ANGLES_RU = ["ручной работы", "на заказ", "под проект"]
ANGLES_EN = ["Handmade", "Made-to-Order", "Bespoke", "Contemporary", "Custom", "Designer"]


def _first(rules, blob, min_hits=1):
    """Побеждает не первое правило по списку, а самое частое в описании.

    Порядок правил задаёт лишь приоритет при равенстве. Брать первое
    совпадение нельзя: в описании LC0036 «прозрачная, как ледяной брусок»
    один раз мелькает «белый», и заголовок получал «белое стекло» вместо
    прозрачного — мелкая, но неправда в витрине.
    """
    best, best_n = ("", ""), 0
    for rx, ru, en in rules:
        n = len(rx.findall(blob))
        if n >= min_hits and n > best_n:
            best, best_n = (ru, en), n
    return best


def ingredients(rec: dict, board: str) -> dict:
    # descrRu — это первые строки descrFullRu, и если склеить оба, слова из
    # начала описания считаются дважды. Из-за этого у LC0043 «белые точки»
    # (в зачине) перевешивали «дымчатые капли» (в конце), и вещь цвета графита
    # уходила в ленту как белая.
    blob = " ".join(str(rec.get(f) or "") for f in ("nameRu", "descrFullRu")) \
        or str(rec.get("descrRu") or "")
    t_ru, t_en = BOARD_TYPE.get(board, ("Люстра", "Chandelier"))
    if t_ru == "Торшер" and TABLE_RX.search(str(rec.get("nameRu") or "")):
        t_ru, t_en = "Настольный светильник", "Table Lamp"
    f_ru, f_en = _first(FORMS, blob)
    c_ru, c_en = _first(TONES, blob)
    s_ru, s_en = _first(SPACES, blob, SPACE_MIN_HITS)
    return dict(type_ru=t_ru, type_en=t_en, form_ru=f_ru, form_en=f_en,
                tone_ru=c_ru, tone_en=c_en, space_ru=s_ru, space_en=s_en)


def title_ru(ing: dict, sku: str, angle: int, wave2: bool = False) -> str:
    """«Люстра-каскад в двусветную гостиную — золотое стекло | Vargov Design LC0024».

    Порядок продиктован тем, как читают ленту: сначала предмет и его форма,
    потом место, и лишь затем материал. Хвост с артикулом отбрасывается
    последним — он нужен, но никогда не важнее поисковых слов впереди.
    """
    tail = " | Vargov Design " + sku
    head = ing["type_ru"] + ("-" + ing["form_ru"] if ing["form_ru"] else "")
    # Вторая волна той же модели заходит с другого угла, иначе Pinterest
    # засчитает её дублем первой.
    slot = ANGLES_RU[angle % len(ANGLES_RU)] if (wave2 or not ing["space_ru"]) else ing["space_ru"]
    parts = [head, slot, ("— " + ing["tone_ru"]) if ing["tone_ru"] else ""]
    while parts:
        s = " ".join(p for p in parts if p).strip(" —")
        if len(s) + len(tail) <= TITLE_MAX:
            return s + tail
        parts.pop()
    return (head + tail)[:TITLE_MAX]


def title_en(ing: dict, sku: str, angle: int, wave2: bool = False) -> str:
    """«Gold Cascade Chandelier for a Double-Height Room | Vargov Design LC0024»."""
    tail = " | Vargov Design " + sku
    space = "" if wave2 else ing["space_en"]
    lead = ANGLES_EN[angle % len(ANGLES_EN)] if (wave2 or not space) else ""
    tone = ing["tone_en"]
    # «Amber Glass Mesh Glass Light Sculpture» — Glass дважды в одной строке.
    # Материал несёт тип, значит из оттенка это слово убираем.
    if "Glass" in ing["type_en"] and tone.endswith(" Glass"):
        tone = tone[: -len(" Glass")]
    parts = [lead, tone, ing["form_en"], ing["type_en"], space]
    # ужимаем с хвоста, но тип не теряем никогда
    order = [4, 0, 1, 2]
    for drop in [[]] + [order[:i + 1] for i in range(len(order))]:
        cur = [p for i, p in enumerate(parts) if i not in drop and p]
        s = " ".join(cur)
        if len(s) + len(tail) <= TITLE_MAX:
            return s + tail
    return (ing["type_en"] + tail)[:TITLE_MAX]


def main():
    cat = json.loads(CAT.read_text(encoding="utf-8"))
    boards = json.loads(Path("data/board-map.json").read_text(encoding="utf-8"))
    generic = boards.get("__generic__", "Hotel & Restaurant Lighting")
    rows, stats = [], collections.Counter()
    for i, (sku, rec) in enumerate(sorted(cat.items())):
        board = boards.get(sku) or generic
        ing = ingredients(rec, board)
        stats["форма"] += bool(ing["form_ru"])
        stats["цвет"] += bool(ing["tone_ru"])
        stats["помещение"] += bool(ing["space_ru"])
        stats[ing["type_ru"]] += 1
        rows.append({
            "sku": sku,
            "board": board,
            "ru": title_ru(ing, sku, i),
            "en": title_en(ing, sku, i),
            "ru2": title_ru(ing, sku, i + 1, wave2=True),
            "en2": title_en(ing, sku, i + 1, wave2=True),
        })

    Path("data/search-titles.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")

    n = len(rows)
    out = io.open("search-titles-report.txt", "w", encoding="utf-8")
    out.write("Моделей: %d\n" % n)
    for k in ("форма", "цвет", "помещение"):
        out.write("  %-10s у %3d (%2.0f%%)\n" % (k, stats[k], 100 * stats[k] / n))

    for lang in ("ru", "en", "ru2", "en2"):
        vals = [r[lang] for r in rows]
        dup = [t for t, c in collections.Counter(vals).items() if c > 1]
        longest = max(len(v) for v in vals)
        out.write("\n%-4s уникальных %d/%d, дублей %d, макс. длина %d\n"
                  % (lang, len(set(vals)), n, len(dup), longest))
        if dup:
            out.write("     примеры дублей: %s\n" % "; ".join(dup[:3]))

    # пересечение волн: заголовок волны-2 не должен повторять волну-1
    cross = sum(1 for r in rows if r["ru"] == r["ru2"] or r["en"] == r["en2"])
    out.write("\nсовпадений волна-1 == волна-2: %d\n" % cross)

    out.write("\nПРИМЕРЫ (было -> стало)\n")
    for r in rows[:14]:
        out.write("  %s\n     RU  %s\n     EN  %s\n" % (r["sku"], r["ru"], r["en"]))
    out.close()
    print(Path("search-titles-report.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
