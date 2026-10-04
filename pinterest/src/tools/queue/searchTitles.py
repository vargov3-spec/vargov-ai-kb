# -*- coding: utf-8 -*-
"""Заголовки пинов от поискового запроса, а не от артикула.

Замер 29.08.2026 показал: за четыре месяца охват вырос в 66 раз, а доля
показов, доходящих до сайта, не сдвинулась — 0,09%% весь период. Верх воронки
расширили, проходимость не тронули. Заголовок и есть та проходимость: поиск
Pinterest текстовый, и «Композиция о взмахе» не совпадает ни с одним запросом
живого человека, тогда как «Люстра-каскад» совпадает.

Из чего собираем:
  тип      — из поля type каталога сайта (catalog.generated.json), переведённого
             в слово, которым это ищут, по тому же мосту, что и поиск сайта
             (src/lib/data/productKinds.ts): световая композиция под потолком —
             «люстра», бра — «бра», зеркало — «зеркало», настенная композиция —
             «панно». Прежде тип брался по доске Pinterest, и зеркала, перегородка,
             ограждение лестницы и декор камина выходили «световой скульптурой»
             или «бра» (аудит 03.10.2026, A177);
  форма    — «каскад», «облако», «кольцо»: главный отличительный признак и
             одновременно живой поисковый запрос;
  цвет     — «золотая», «дымчатый», «Gold»: тоже ищут, дополняет форму;
  помещение— бонус, когда уверенно видно.

Форма и цвет берутся ТОЛЬКО из продуктовой части описания (абзацы о самой
вещи). Разделы «Где уместна» и «Стилистика» описывают интерьер вокруг
(«зеркала, латунь, светлые стены»), и цвет из них выходил чужим (A176).
Помещение берётся из продуктовой части и раздела «Где уместна».

МАТЕРИАЛ В ЗАГОЛОВОК НЕ ПИШЕМ — ни «стекло», ни «Glass», ни «латунь».
Правило владельца для всех текстов о товаре, включая Pinterest: «материал мы
нигде не указываем» (27.09.2026; memory/vargov-owner-wording-rules.md). Прежняя
схема «— золотое стекло» к тому же называла стеклом керамику и алюминий
(аудит 03.10.2026, A176, A380, A396). Проверка в main(): заголовок со
стоп-словом (стекло, латунь, хрусталь, медь, керамика и их английские пары)
останавливает сборку.

Артикул оставлен в хвосте: он занимает 22 символа из 100, но гарантирует
уникальность заголовка и нужен покупателю, который знает модель. Поисковые
слова при этом стоят впереди, где они и работают.

Запуск из корня pinterest/:
  python src/tools/queue/searchTitles.py --site <папка репозитория сайта>
      — обновить data/site-products.json из каталога сайта и пересобрать заголовки;
  python src/tools/queue/searchTitles.py
      — пересобрать заголовки по уже снятому data/site-products.json.
Результат: data/search-titles.json и titles/search-titles.json (копия в git
для облачной рутины), отчёт data/search-titles-report.txt.
"""
from __future__ import annotations

import collections
import io
import json
import re
import sys
from pathlib import Path

SITE_PRODUCTS = Path("data/site-products.json")
TITLE_MAX = 100

# --- снимок каталога сайта ------------------------------------------------------
def refresh_site_products(site: Path) -> None:
    """Тип, крепление и раздел — из catalog.generated.json сайта; продуктовая
    часть описания и «Где уместна» — из product-copy/products.ru.json.

    Тип берём именно из catalog.generated.json: у LC0366–LC0380 поле type в
    product-copy сдвинуто вместе с текстами (A017), а каталог верен."""
    data = site / "src" / "lib" / "data"
    cat = json.loads((data / "catalog.generated.json").read_text(encoding="utf-8"))
    copy = json.loads((data / "product-copy" / "products.ru.json").read_text(encoding="utf-8"))["items"]
    out = {}
    for p in cat:
        sku = p["code"]
        c = copy.get(sku) or {}
        out[sku] = {
            "type": p.get("type") or "",
            "mount": p.get("mount") or "",
            "category": p.get("category") or "",
            "productRu": " ".join(c.get("paragraphs") or []),
            "whereRu": c.get("whereItWorks") or "",
        }
    SITE_PRODUCTS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("site-products: %d артикулов из %s" % (len(out), site), file=sys.stderr)


# Описания LC0366–LC0380 на сайте сдвинуты: текст артикула N описывает изделие
# N+2 (аудит 03.10.2026, A017). Пока сайт их не исправит, форму, цвет и
# помещение по этим текстам не определяем — в заголовке остаётся только тип.
SHIFTED = {"LC%04d" % n for n in range(366, 381)}

# --- тип изделия -------------------------------------------------------------
# (русский тип, английский тип, род русского типа, цеплять ли форму через дефис)
# Род нужен, чтобы согласовать цвет: «люстра — золотая», «торшер — золотой».
# Форму не цепляем, когда главное слово типа стоит не последним
# («Декор камина-кольца» читается как брак).
CHANDELIER = ("Люстра", "Chandelier", "f", True)
LIGHT_SCULPTURE = ("Световая скульптура", "Light Sculpture", "f", True)
EXACT_TYPE = {
    "Зеркала":                  ("Зеркало", "Mirror", "n", True),
    "Зеркала и декор":          ("Зеркало", "Mirror", "n", True),
    "Межкомнатная перегородка": ("Перегородка", "Room Divider", "f", True),
    "Лестничное ограждение":    ("Ограждение лестницы", "Staircase Railing", "n", False),
    "Декор камина":             ("Декор камина", "Fireplace Decor", "m", False),
    "Ландшафтная скульптура":   ("Ландшафтная скульптура", "Landscape Sculpture", "f", True),
    "Декор":                    ("Настенный декор", "Wall Decor", "m", True),
    "Скульптура":               ("Скульптура", "Sculpture", "f", True),
    "Подвесная скульптура":     ("Подвесная скульптура", "Hanging Sculpture", "f", True),
    "Настенная скульптура":     ("Настенная скульптура", "Wall Sculpture", "f", True),
    "Настенный арт-объект":     ("Настенный арт-объект", "Wall Art Object", "m", False),
    "Настольный арт-объект":    ("Настольный арт-объект", "Table Art Object", "m", False),
    "Напольный арт-объект":     ("Напольный арт-объект", "Floor Art Object", "m", False),
    # «панно» — слово, которым поиск сайта называет настенные композиции
    "Настенная композиция":     ("Панно", "Wall Art", "n", True),
    "Настенные световые композиции": ("Настенный светильник", "Wall Light", "m", True),
    "Настенно-потолочная декоративная композиция":
                                ("Настенно-потолочная композиция", "Wall-to-Ceiling Sculpture", "f", True),
    "Авторская тематическая композиция": CHANDELIER,
}


def search_type(sp: dict) -> tuple:
    t = (sp.get("type") or "").strip()
    tl = t.lower()
    mount = sp.get("mount") or ""
    if t in EXACT_TYPE:
        return EXACT_TYPE[t]
    if "бра" in tl.split("-") or tl.startswith("бра") or tl.endswith("-бра"):
        return ("Бра", "Wall Sconce", "n", True)
    if tl.startswith("торшер"):
        if "настольн" in tl:
            return ("Настольный светильник", "Table Lamp", "m", True)
        return ("Торшер", "Floor Lamp", "m", True)
    if tl == "световая композиция":
        if mount == "floor":
            return ("Напольная световая скульптура", "Floor Light Sculpture", "f", True)
        if mount == "wall":
            return ("Настенный светильник", "Wall Light", "m", True)
        return CHANDELIER
    if tl == "декоративная композиция":
        if mount == "wall":
            return ("Настенная световая скульптура", "Wall Light Sculpture", "f", True)
        if mount == "table":
            return ("Настольная световая скульптура", "Table Light Sculpture", "f", True)
        if mount == "floor":
            return ("Напольная световая скульптура", "Floor Light Sculpture", "f", True)
        return LIGHT_SCULPTURE
    raise SystemExit("Тип сайта без перевода в поисковый: %r — допишите EXACT_TYPE" % t)


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
    # форма, а не материал; по-английски «Crystal» читается как «хрусталь»
    (r"\bкристалл\w*", "кристаллы", "Faceted"),
    (r"\bснежин\w*", "снежинки", "Snowflake"),
    (r"\bзвёзд\w*|\bзвезд\w*", "звёзды", "Star"),
    (r"\bлент[аыуойе]\w*", "ленты", "Ribbon"),
    (r"\bтрубк\w*|\bтруб[аыуой]\b", "трубки", "Tube"),
    (r"\bсосульк\w*", "сосульки", "Icicle"),
]
FORMS = [(re.compile(p, re.I), ru, en) for p, ru, en in FORMS]

# --- цвет и отделка: тоже поисковые слова ------------------------------------
# Только видимый цвет, без материала. Русский цвет согласуется с родом типа
# («люстра — золотая», «торшер — золотой», «бра — золотое»), поэтому хранится
# тремя формами: ж, м, ср. Латунь даёт цвет «тёплого золота» — несклоняемый
# оборот. Медь как оттенок не ведём: в описаниях это перелив рядом с другим
# цветом, и победит основной.
# Порядок: сначала редкое и характерное, потом общее — «прозрачное» есть почти
# везде и перехватило бы всё остальное.
def _adj(stem_f, stem_m, stem_n):
    return {"f": stem_f, "m": stem_m, "n": stem_n}


TONES = [
    # Дымчатое семейство собрано широко: у этих вещей «серый дым», «графит» и
    # «стальные блики» описывают один и тот же оттенок, и по отдельности каждое
    # слово встречается реже, чем проходное «белый» из соседнего предложения.
    # «серый» перечислен точными формами: широкое \bсер[ыаоуи]\w* ловит ещё и
    # «серия», а это слово стоит в описаниях чаще самого цвета.
    (r"\bдымчат\w*|\bдым\w*|\bграфит\w*|\bстальн\w*"
     r"|\bсер(?:ый|ая|ое|ые|ого|ому|ым|ыми|ых|ой|ую)\b",
     _adj("дымчатая", "дымчатый", "дымчатое"), "Smoky"),
    (r"\bянтарн\w*", _adj("янтарная", "янтарный", "янтарное"), "Amber"),
    (r"\bмолочн\w*|\bопалов\w*", _adj("молочно-белая", "молочно-белый", "молочно-белое"), "Milky White"),
    (r"\bлатун\w*", _adj("цвета тёплого золота", "цвета тёплого золота", "цвета тёплого золота"), "Warm Gold"),
    (r"\bзолот\w*|\bпозолот\w*", _adj("золотая", "золотой", "золотое"), "Gold"),
    (r"\bчёрн\w*|\bчерн\w*", _adj("чёрная", "чёрный", "чёрное"), "Black"),
    (r"\bбел\w*", _adj("белая", "белый", "белое"), "White"),
    (r"\bпрозрачн\w*|\bбесцветн\w*", _adj("прозрачная", "прозрачный", "прозрачное"), "Clear"),
]
TONES = [(re.compile(p, re.I), ru, en) for p, ru, en in TONES]

# Цвет прожилок камня — не цвет вещи. У торшеров на каменном основании
# «золотистые прожилки» (LC0209), «серые прожилки» (LC0207), «белая жила»
# (LC0208) перебивали прозрачную крону: заголовок называл бесцветный абажур
# золотым. Перед подсчётом цвета такие обороты вырезаются целиком.
VEIN_RX = re.compile(
    r"(?:[а-яё-]+(?:ыми|ими|ой|ей|ая|яя|ое|ее|ые|ие|ий|ый|ую|юю|ого|его|ым|им)\s*,?\s*(?:и\s+)?){1,4}"
    r"(?:прожилк\w*|жилк\w*|жил(?:а|ы|у|е|ой|ами|ах)\b)", re.I)

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

# --- стоп-слова: материал в заголовке останавливает сборку --------------------
STOP_RX = re.compile(
    r"стекл|стеклян|glass|латун|brass|хрустал|crystal|\bмед[ьи]\b|медн|copper"
    r"|керами|ceramic|металл|metal|алюмин|alumin|бронз|bronze|фарфор|porcelain",
    re.I)


def _first(rules, blob, min_hits=1):
    """Побеждает не первое правило по списку, а самое частое в описании.

    Порядок правил задаёт лишь приоритет при равенстве. Брать первое
    совпадение нельзя: в описании LC0036 «прозрачная, как ледяной брусок»
    один раз мелькает «белый», и заголовок получал «белый» вместо
    прозрачного — мелкая, но неправда в витрине.
    """
    best, best_n = ("", ""), 0
    for rx, ru, en in rules:
        n = len(rx.findall(blob))
        if n >= min_hits and n > best_n:
            best, best_n = (ru, en), n
    return best


def ingredients(sku: str, sp: dict) -> dict:
    t_ru, t_en, gender, attach = search_type(sp)
    if sku in SHIFTED:
        product, where = "", ""
    else:
        product, where = sp.get("productRu") or "", sp.get("whereRu") or ""
    f_ru, f_en = _first(FORMS, product)
    tone, c_en = _first(TONES, VEIN_RX.sub(" ", product))
    c_ru = tone[gender] if tone else ""
    s_ru, s_en = _first(SPACES, product + " " + where, SPACE_MIN_HITS)
    # «Ограждение лестницы над лестницей» — помещение уже названо типом.
    if s_en == "for a Staircase" and "Staircase" in t_en:
        s_ru, s_en = "", ""
    return dict(type_ru=t_ru, type_en=t_en, attach=attach,
                form_ru=f_ru if attach else "", form_en=f_en,
                tone_ru=c_ru, tone_en=c_en, space_ru=s_ru, space_en=s_en)


def title_ru(ing: dict, sku: str, angle: int, wave2: bool = False) -> str:
    """«Люстра-каскад в двусветную гостиную — золотая | Vargov Design LC0024».

    Порядок продиктован тем, как читают ленту: сначала предмет и его форма,
    потом место, и лишь затем цвет. Хвост с артикулом отбрасывается
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
    parts = [lead, ing["tone_en"], ing["form_en"], ing["type_en"], space]
    # ужимаем с хвоста, но тип не теряем никогда
    order = [4, 0, 1, 2]
    for drop in [[]] + [order[:i + 1] for i in range(len(order))]:
        cur = [p for i, p in enumerate(parts) if i not in drop and p]
        s = " ".join(cur)
        if len(s) + len(tail) <= TITLE_MAX:
            return s + tail
    return (ing["type_en"] + tail)[:TITLE_MAX]


def main():
    args = sys.argv[1:]
    if "--site" in args:
        refresh_site_products(Path(args[args.index("--site") + 1]))
    site = json.loads(SITE_PRODUCTS.read_text(encoding="utf-8"))
    # Доска — по-прежнему из board-map.json: она нужна очереди, а не заголовку.
    boards = json.loads(Path("data/board-map.json").read_text(encoding="utf-8"))
    generic = boards.get("__generic__", "Hotel & Restaurant Lighting")
    rows, stats = [], collections.Counter()
    for i, sku in enumerate(sorted(site)):
        sp = site[sku]
        ing = ingredients(sku, sp)
        stats["форма"] += bool(ing["form_en"])
        stats["цвет"] += bool(ing["tone_en"])
        stats["помещение"] += bool(ing["space_ru"])
        stats[ing["type_ru"]] += 1
        rows.append({
            "sku": sku,
            "board": boards.get(sku) or generic,
            "ru": title_ru(ing, sku, i),
            "en": title_en(ing, sku, i),
            "ru2": title_ru(ing, sku, i + 1, wave2=True),
            "en2": title_en(ing, sku, i + 1, wave2=True),
        })

    # Проверки до записи: без материала, без дублей, волны не совпадают.
    errors = []
    for r in rows:
        for lang in ("ru", "en", "ru2", "en2"):
            m = STOP_RX.search(r[lang])
            if m:
                errors.append("%s %s: стоп-слово «%s» в «%s»" % (r["sku"], lang, m.group(0), r[lang]))
            if len(r[lang]) > TITLE_MAX:
                errors.append("%s %s: длина %d" % (r["sku"], lang, len(r[lang])))
        if r["ru"] == r["ru2"] or r["en"] == r["en2"]:
            errors.append("%s: волна-2 повторяет волну-1" % r["sku"])
    for lang in ("ru", "en", "ru2", "en2"):
        dup = [t for t, c in collections.Counter(r[lang] for r in rows).items() if c > 1]
        errors += ["дубль %s: %s" % (lang, t) for t in dup]
    if errors:
        print("\n".join(errors[:50]), file=sys.stderr)
        raise SystemExit("заголовки не записаны: %d ошибок" % len(errors))

    payload = json.dumps(rows, ensure_ascii=False, indent=1)
    Path("data/search-titles.json").write_text(payload, encoding="utf-8")
    # Вторая копия — в отслеживаемой папке: data/ лежит в .gitignore, а этот
    # файл нужен облачной рутине, которая клонирует репозиторий и переписывает
    # заголовки в очереди без участия компьютера.
    Path("titles").mkdir(exist_ok=True)
    Path("titles/search-titles.json").write_text(payload, encoding="utf-8")

    n = len(rows)
    out = io.open("data/search-titles-report.txt", "w", encoding="utf-8")
    out.write("Моделей: %d\n" % n)
    for k in ("форма", "цвет", "помещение"):
        out.write("  %-10s у %3d (%2.0f%%)\n" % (k, stats[k], 100 * stats[k] / n))
    out.write("\nТипы:\n")
    for k, v in stats.most_common():
        if k not in ("форма", "цвет", "помещение"):
            out.write("  %-32s %d\n" % (k, v))
    for lang in ("ru", "en", "ru2", "en2"):
        vals = [r[lang] for r in rows]
        out.write("\n%-4s уникальных %d/%d, макс. длина %d\n"
                  % (lang, len(set(vals)), n, max(len(v) for v in vals)))
    out.write("\nстоп-слов (материалов): 0, дублей: 0, совпадений волна-1 == волна-2: 0\n")
    out.write("\nПРИМЕРЫ\n")
    for r in rows[:14]:
        out.write("  %s\n     RU  %s\n     EN  %s\n" % (r["sku"], r["ru"], r["en"]))
    out.close()
    print(Path("data/search-titles-report.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
