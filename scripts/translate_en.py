"""
Builds the English-language mirror of the knowledge base (en/products,
en/collections, en/datasets, en/references) from scan/products.jsonl.

Translation approach: the vargov.ru catalog reuses a small set of
boilerplate phrases (~120) across almost all product descriptions, with
only dimensions/SKUs varying. Those phrases are translated once here and
substituted mechanically — this is far more reliable than asking a model
to freely translate 645 near-duplicate strings. A handful of genuinely
unique marketing paragraphs are hand-translated in UNIQUE_PARAGRAPHS.

If vargov.ru introduces new boilerplate phrasing this dictionary doesn't
cover, run_all.py's summary will flag it (grep for Cyrillic remaining in
en/datasets/products.jsonl) rather than silently ship broken English.
"""
import json, re, os, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIR = ROOT / "scan"
EN_DIR = ROOT / "en"

CAT_MAP = {
    "lighting_compositions_vargovdesign_ru": "lighting-compositions",
    "decorative_compositions_vargovdesign_ru": "decorative-compositions",
    "decor_and_sculptural_compositions_vargovdesign_ru": "sculptural-decor",
    "floorlamps_and_tablelamps_vargovdesign_ru": "floor-table-lamps",
    "official_showroom_vargovdesign": "showroom-items",
    "elements_in_stock": "stock-elements",
}
CAT_EN = {
    "lighting-compositions": "Lighting compositions",
    "decorative-compositions": "Decorative compositions",
    "sculptural-decor": "Sculptural compositions & decor",
    "floor-table-lamps": "Floor lamps, sconces & tabletop art objects",
    "showroom-items": "Showroom items",
    "stock-elements": "Elements in stock",
}

UNIQUE_PARAGRAPHS = [
    ("Эта настенная композиция существует на грани между объектом искусства и архитектурной пластикой. Она не стремится быть симметричной или “правильной” - напротив, её сила в естественной неравномерности и ощущении живого движения.",
     "This wall composition exists on the border between an art object and architectural sculpture. It does not strive to be symmetrical or “correct” — on the contrary, its strength lies in natural irregularity and a sense of living movement."),
    ("Этот торшер выглядит как вертикальная световая скульптура, собранная из ритма, стекла и отражений. Прозрачные стеклянные элементы насыщенного зелёно-бирюзового оттенка выстроены слоями вокруг источника света. Их форма напоминает кристаллизованные лепестки, застывшие в момент движения. Тонкие вертикальные стойки и основание из металла с тёплым золотым покрытием добавляют архитектурную строгость и балансируют органичность стекла. За счёт этого контраста торшер воспринимается не как обычный источник света, а как арт-объект, который работает и днём, и вечером.",
     "This floor lamp looks like a vertical light sculpture built from rhythm, glass and reflections. Transparent glass elements in a rich green-turquoise shade are layered around the light source. Their shape recalls crystallized petals frozen mid-motion. Slender vertical uprights and a metal base with a warm gold finish add architectural rigor and balance the organic quality of the glass. This contrast makes the floor lamp read not as an ordinary light source but as an art object that works both day and night."),
    ("LC0487 - авторская световая композиция, стилизованная под подводный мир коралловых рифов. Она переносит зрителя в сердце морской экосистемы, где сквозь ажурную структуру кораллов свободно проникает свет, а между ними скользят яркие экзотические рыбки. Базовая форма выполнена из белой перфорированной керамики - она имитирует текстуру кораллов, органичную и сложную по геометрии. Эти элементы моделируются вручную, создавая ощущение живой, «дышащей» структуры, насыщенной воздухом и светом. Внутри и вокруг этой структуры рассыпаны цветные стеклянные элементы, вдохновлённые формой тропических рыб. Их поверхности покрыты металлическими отблесками - золотыми, синими и дымчато-серыми, что делает их похожими на рыбью чешую, переливающуюся в солнечных лучах под водой. Источник света интегрирован внутрь композиции и преломляется через стекло и керамику, создавая игру бликов, имитирующую мерцание воды и солнечные лучи, проходящие сквозь толщу океана. LC0487 - это не просто осветительный объект, а погружение в подводную сказку, где свет, форма и цвет сливаются в единый художественный образ.",
     "LC0487 is a signature lighting composition styled after the underwater world of coral reefs. It carries the viewer into the heart of a marine ecosystem, where light passes freely through an openwork coral structure and bright exotic fish glide between the forms. The base shape is made of white perforated ceramic, imitating the organic, geometrically complex texture of coral. These elements are hand-modeled, creating the feel of a living, “breathing” structure filled with air and light. Colored glass elements inspired by the shapes of tropical fish are scattered inside and around this structure. Their surfaces are covered with metallic highlights — gold, blue and smoky grey — making them resemble fish scales shimmering in sunlight underwater. The light source is integrated inside the composition and refracts through the glass and ceramic, creating a play of reflections that imitates the shimmer of water and sunbeams passing through the depths of the ocean. LC0487 is not just a lighting object but an immersion into an underwater fairy tale, where light, form and color merge into a single artistic image."),
    ("Да, мы понимаем, что этот дизайн не для всех. Потому что не каждый готов спокойно поставить в интерьер предмет, который выглядит как капельница и при этом становится самым обсуждаемым объектом в комнате. Кому-то нужен безопасный декор. Кому-то очередной нейтральный торшер, который никто не заметит. А кому-то интереснее жить среди вещей с характером, иронией и лёгкой внутренней дерзостью. Driplight - это несколько капель света для тех, кто не боится предметов с подтекстом. Торшер в форме капельницы - это как бытовая ирония, переведённая в объект интерьера: знакомый медицинский силуэт вдруг становится источником мягкого света, спокойствия и даже лёгкой самоиронии. Показания к применению: — понедельник — хроническая усталость — дедлайны — плохое настроение — творческий кризис — просто так Способ применения: 1 торшер в день по мере необходимости Побочные эффекты: — улыбка — вдохновение — желание жить и делать крутые вещи ПЕРЕД ИСПОЛЬЗОВАНИЕМ УБЕДИТЕСЬ, ЧТО У ВАС ЕСТЬ ЧУВСТВО ЮМОРА.",
     "Yes, we know this design isn't for everyone. Not everyone is ready to calmly place an object that looks like an IV drip stand in their interior — and have it become the most talked-about piece in the room. Some people want safe decor. Some want yet another neutral floor lamp nobody will notice. And some find it more interesting to live among objects with character, irony and a touch of inner boldness. Driplight is a few drops of light for those who aren't afraid of objects with a subtext. A floor lamp shaped like an IV drip stand is domestic irony translated into an interior object: a familiar medical silhouette suddenly becomes a source of soft light, calm, and even a little self-irony. Indications for use: — Monday — chronic fatigue — deadlines — bad mood — creative block — just because. Directions: 1 floor lamp per day, as needed. Side effects: — smiling — inspiration — the urge to live and make cool things. BEFORE USE, MAKE SURE YOU HAVE A SENSE OF HUMOR."),
]

PHRASES = [
    ("Изготовление композиций любого размера из любого количества элементов на заказ",
     "Custom-made compositions in any size and any number of elements"),
    ("Для расчета необходимого количества элементов по габаритным размерам нужной вам композиции, стоимости производства и доставки, обращайтесь в WhatsApp",
     "To calculate the number of elements needed for your desired composition size, as well as production and delivery cost, please contact us via WhatsApp"),
    ("Гарантия распространяется только на оригинальный товар", "The warranty applies only to the original product"),
    ("Цветочные бутоны ручной работы из холодного фарфора с диодом на металлическом каркасе, коллаборация Jardiz , Fabli , Vargov®Design",
     "Handmade flower buds made of cold porcelain with an LED on a metal frame, a collaboration between Jardiz, Fabli and Vargov®Design"),
    ("Цена указана за один погонные метр ленты", "Price shown is per linear meter of strip"),
    ("Цена указана за один погонный метр ленты", "Price shown is per linear meter of strip"),
    ("Цена указана за один погонный метр", "Price shown is per linear meter"),
    ("Цена указана за один подвес:", "Price shown is per single pendant:"),
    ("Цена указана за один элемент", "Price shown is per single element"),
    ("Цена указана за композицию", "Price shown is for the whole composition"),
    ("Элемент представлен в официальном шоуруме Vargov®Design по адресу: Москва, Нахимовский проспект 24, павильон 2, стенд 212",
     "This element is on display at the official Vargov®Design showroom: Moscow, Nakhimovsky Prospekt 24, Pavilion 2, Stand 212"),
    ("Бра для световой композиции:", "Sconce for lighting composition:"),
    ("Размеры композиций на примере:", "Example composition sizes:"),
    ("Возможные размеры элементов:", "Possible element sizes:"),
    ("Размер одного элемента (микс):", "Size of one element (mixed):"),
    ("Размер элемента (микс):", "Element size (mixed):"),
    ("Размер декоративного элемента:", "Decorative element size:"),
    ("Размер керамического элемента:", "Ceramic element size:"),
    ("Размер хрустального элемента:", "Crystal element size:"),
    ("Размер основного элемента:", "Main element size:"),
    ("Размер композиции:", "Composition size:"),
    ("Размер одного элемента:", "Size of one element:"),
    ("Размер элементов:", "Elements size:"),
    ("Размер элемента:", "Element size:"),
    ("Размер торшера:", "Floor lamp size:"),
    ("Размер бра:", "Sconce size:"),
    ("с цоколем:", "with base:"),
    ("высота композиции", "composition height"),
    ("отрезка", "segment"),
    ("ветка", "branch"),
    ("лист", "leaf"),
    ("Количество элементов в композиции:", "Number of elements in composition:"),
    ("Материал элемента:", "Element material:"),
    ("Цвет:", "Color:"),
    ("Диоды:", "LEDs:"),
    ("прозрачные бесцветные с пузырьками воздуха", "clear colorless with air bubbles"),
    ("микс 50/50, золото/прозрачные бесцветные", "50/50 mix, gold / clear colorless"),
    ("белая эмаль/зеркальное золото", "white enamel / mirror gold"),
    ("черная эмаль/зеркальное золото", "black enamel / mirror gold"),
    ("янтарные", "amber"),
    ("бесцветные", "clear colorless"),
    ("стекло", "glass"),
    ("керамика", "ceramic"),
    ("Размер композиции и элемента может быть любой, все индивидуально и на заказ.",
     "Composition and element size can be anything, fully custom-made."),
    ("Размер композиции может быть любой, все индивидуально и на заказ.",
     "Composition size can be anything, fully custom-made."),
    ("Характеристики композиции", "Specifications for composition"),
    ("Характеристики светильника", "Fixture specifications"),
    ("Элемент для композиций", "Element for compositions"),
    ("Элементы для композиций", "Elements for compositions"),
    ("и для бра", "and for sconce"),
    ("Элемент:", "Element:"),
    ("Цвет элементов:", "Elements color:"),
    ("Цвет элемента:", "Element color:"),
    ("Цвет каркаса:", "Frame color:"),
    ("Цвет монтажного комплекта:", "Mounting kit color:"),
    ("Цвет кабеля:", "Cable color:"),
    ("Ширина ленты:", "Strip width:"),
    ("Длина ленты:", "Strip length:"),
    ("Длина шнура: любая", "Cord length: any"),
    ("Длина провода/троса: любая", "Wire/cable length: any"),
    ("Длина троса: любая", "Cable length: any"),
    ("Размер элементов (микс):", "Elements size (mixed):"),
    ("Размер камней:", "Stone size:"),
    ("Размер светового элемента:", "Light element size:"),
    ("Диоды маломощные:", "Low-power LEDs:"),
    ("Диод в элементе:", "LED in element:"),
    ("Диод:", "LED:"),
    ("два диода", "two LEDs"),
    ("погонных метров", "linear meters"),
    ("любой цвет", "any color"),
    ("Материал:", "Material:"),
    ("хрусталь", "crystal"),
    ("прозрачный бесцветный", "clear colorless"),
    ("прозрачные", "clear"),
    ("прозрачный", "clear"),
    ("синий бирюзовый", "blue turquoise"),
    ("хром/золото", "chrome/gold"),
    ("золото/серебро с эффектом старения", "gold/silver with aged effect"),
    ("красный", "red"),
    ("дымчатый", "smoky"),
    ("коньяк", "cognac"),
    ("белый", "white"),
    ("черный", "black"),
    ("латунь", "brass"),
    ("гибкий металлокаркас", "flexible metal frame"),
    ("с добавлением в массу стекла частиц золотой фольги", "with gold foil particles added into the glass"),
    ("Подключение к одному выводу 220V", "Connects to a single 220V output"),
    ("Композиция может быть любого размера и содержать любое количество элементов.",
     "The composition can be of any size and contain any number of elements."),
    ("Варианты композиций от Vargov®Design", "Composition options from Vargov®Design"),
    ("Фурнитура:", "Hardware:"),
    ("Параметры композиции:", "Composition parameters:"),
    ("размер композиции:", "composition size:"),
    ("длина контура:", "outline length:"),
    ("количество элементов", "number of elements"),
    ("мощность композиции:", "composition power:"),
    ("диоды", "LEDs"),
    ("Состав композиции:", "Composition consists of:"),
    ("6-ти рядная лента с диодами", "6-row LED strip"),
    ("размер стержня", "rod size"),
    ("Скаты с диодами", "Slopes with LEDs"),
    ("размер ската", "slope size"),
    ("количество", "quantity"),
    ("H стеклянного элемента", "H of the glass element"),
    ("регулируемая", "adjustable"),
    ("угол изгиба", "bend angle"),
    ("Элемент для композиции", "Element for composition"),
    ("любой", "any"),
    ("композиции", "composition"),
    ("композиция", "composition"),
    ("элемента", "element"),
    ("элементов", "elements"),
    ("элемент", "element"),
    ("нет", "none"),
    ("шар", "sphere"),
    ("янтарный", "amber"),
    ("янтарь", "amber"),
    ("белая эмаль", "white enamel"),
    ("на металлической базе", "on a metal base"),
    ("Размер", "Size"),
    ("от ", "from "),
    (" до ", " to "),
    ("шт", "pcs"),
    ("микс", "mix"),
]

RE_PHRASES = [
    (re.compile(r"Заказ от (\d+) штук\.?"), r"Minimum order: \1 pieces."),
    (re.compile(r"3D\s*модел[ья]\s*\(max,\s*fbx\)\s*в\s*реальном\s*производственном\s*размере\s*:?\s*скачать\s*3[DdДд]\s*модел[ья]", re.I),
     "3D model (max, fbx) at actual production scale: download the 3D model"),
    (re.compile(r"3D\s*модел[ья]\s*\(max,\s*fbx\)\s*в\s*реальном\s*производственном\s*размере\s*:\s*[Dd]ownload", re.I),
     "3D model (max, fbx) at actual production scale: download the 3D model"),
]

TITLE_PHRASES = [
    ("Настенно-потолочная декоративная композиция", "Wall-ceiling decorative composition"),
    ("Настенная световая скульптура-бра", "Wall light sculpture-sconce"),
    ("Торшер-световая скульптура", "Floor lamp-light sculpture"),
    ("Бра-настенная световая композиция", "Sconce-wall lighting composition"),
    ("Настенные световые композиции", "Wall lighting compositions"),
    ("Настенная декоративная композиция", "Wall decorative composition"),
    ("Настенная световая композиция", "Wall lighting composition"),
    ("Бра-настенная скульптура", "Sconce-wall sculpture"),
    ("Ландшафтная скульптура", "Landscape sculpture"),
    ("Авторская тематическая композиция", "Signature themed composition"),
    ("Межкомнатная перегородка", "Interior partition"),
    ("Подвесная скульптура", "Hanging sculpture"),
    ("Настольный арт-объект", "Tabletop art object"),
    ("Напольный арт-объект", "Floor art object"),
    ("Настенный арт-объект", "Wall art object"),
    ("Световая композиция", "Lighting composition"),
    ("Декоративная композиция", "Decorative composition"),
    ("Настенная композиция", "Wall composition"),
    ("Настенная скульптура", "Wall sculpture"),
    ("Декор камина", "Fireplace decor"),
    ("Зеркала и декор", "Mirrors and decor"),
    ("Декор для лестницы", "Staircase decor"),
    ("Световой элемент", "Light element"),
    ("Торшер Driplight", "Floor lamp Driplight"),
    ("Торшер", "Floor lamp"),
    ("Зеркала", "Mirrors"),
    ("Бра", "Sconce"),
    ("Декор", "Decor"),
    ("Скульптура", "Sculpture"),
    ("Элементы для композиций", "Elements for compositions"),
    ("Элементы", "Elements"),
    ("в наличии", "in stock"),
    ("и для бра", "and for sconce"),
]


def normalize_units(text):
    if not text:
        return text
    text = text.replace("мм", "mm").replace("см", "cm").replace("шт.", "pcs")
    text = re.sub(r"(?<=\d)[Хх](?=\d)", "x", text)
    text = re.sub(r"\bН(?=\d)", "H", text)
    return text


def translate_text(text, phrase_map):
    if not text:
        return text
    for ru, en in UNIQUE_PARAGRAPHS:
        text = text.replace(ru, en)
    for pattern, repl in RE_PHRASES:
        text = pattern.sub(repl, text)
    for ru, en in phrase_map:
        text = text.replace(ru, en)
    return normalize_units(text)


def has_cyrillic(text):
    return bool(re.search(r"[а-яА-ЯёЁ]", text or ""))


def safe_id(p):
    if p.get("sku"):
        return re.sub(r"[^A-Za-z0-9_-]", "_", p["sku"])
    return str(p.get("uid") or "unknown")


def build_en():
    products = []
    with open(SCAN_DIR / "products.jsonl", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                products.append(json.loads(line))

    unresolved = []
    for p in products:
        p["category_slug"] = CAT_MAP.get(p["category"], p["category"])
        p["title_en"] = translate_text(p.get("title") or "", TITLE_PHRASES)
        p["description_en"] = translate_text(p.get("description") or "", PHRASES)
        if has_cyrillic(p["title_en"]) or has_cyrillic(p["description_en"]):
            unresolved.append(p)

    by_cat = {}
    for p in products:
        by_cat.setdefault(p["category_slug"], []).append(p)

    prod_dir = EN_DIR / "products"
    for slug, items in by_cat.items():
        cat_dir = prod_dir / slug
        cat_dir.mkdir(parents=True, exist_ok=True)
        for p in items:
            pid = safe_id(p)
            title = p.get("title_en") or CAT_EN.get(slug, slug)
            desc = p.get("description_en") or ""
            gallery = p.get("gallery") or []
            lines = [
                f"# {title} ({p.get('sku') or pid})", "",
                f"- Category: {CAT_EN.get(slug, slug)}",
                f"- SKU: {p.get('sku') or 'not specified'}",
                f"- Source: {p['url']}",
                "- Price: on request (not published on the website)", "",
                "## Description (as published on the source site)",
                desc if desc else "_No description published for this item._", "",
            ]
            if gallery:
                lines.append("## Images")
                lines += [f"{i}. {img}" for i, img in enumerate(gallery, 1)]
                lines.append("")
            lines += [
                "## Note",
                "Detailed technical specifications (materials, dimensions, color, light temperature) are not published individually for most items on the source site — they are confirmed with the brand on a per-order basis.",
            ]
            (cat_dir / f"{pid}.md").write_text("\n".join(lines), encoding="utf-8")

    coll_dir = EN_DIR / "collections"
    coll_dir.mkdir(exist_ok=True)
    for slug, items in by_cat.items():
        en_name = CAT_EN.get(slug, slug)
        src_cat = items[0]["category"]
        lines = [f"# {en_name}", "", f"Source category: https://vargov.ru/{src_cat}", "",
                 f"Items in this collection: {len(items)}", "", "## Item list"]
        for p in sorted(items, key=lambda x: x.get("sku") or ""):
            pid = safe_id(p)
            lines.append(f"- [{p.get('sku') or pid}](../products/{slug}/{pid}.md) — {p['url']}")
        (coll_dir / f"{slug}.md").write_text("\n".join(lines), encoding="utf-8")

    ds_dir = EN_DIR / "datasets"
    ds_dir.mkdir(exist_ok=True)
    out_products = [{
        "url": p["url"], "category": p["category_slug"],
        "category_label": CAT_EN.get(p["category_slug"], p["category_slug"]),
        "sku": p.get("sku"), "title": p.get("title_en"),
        "description": p.get("description_en"), "gallery": p.get("gallery"),
    } for p in products]

    (ds_dir / "products.json").write_text(json.dumps(out_products, ensure_ascii=False, indent=2), encoding="utf-8")
    with open(ds_dir / "products.jsonl", "w", encoding="utf-8") as f:
        for p in out_products:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    with open(ds_dir / "products.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sku", "category", "category_label", "title", "url", "image_count", "first_image", "description"])
        for p in out_products:
            w.writerow([p.get("sku") or "", p["category"], p["category_label"], p.get("title") or "",
                        p["url"], len(p.get("gallery") or []), (p.get("gallery") or [""])[0],
                        (p.get("description") or "")[:500]])
    with open(ds_dir / "products.md", "w", encoding="utf-8") as f:
        f.write("# Vargov Design — product summary\n\n")
        f.write(f"Total products collected: {len(products)}\n\n| Category | Count |\n|---|---|\n")
        for slug, items in sorted(by_cat.items(), key=lambda x: -len(x[1])):
            f.write(f"| {CAT_EN.get(slug, slug)} | {len(items)} |\n")
        f.write("\n## Full list\n\n| SKU | Category | URL |\n|---|---|---|\n")
        for p in sorted(products, key=lambda x: (x["category_slug"], x.get("sku") or "")):
            f.write(f"| {p.get('sku') or safe_id(p)} | {CAT_EN.get(p['category_slug'], p['category_slug'])} | {p['url']} |\n")

    ref_dir = EN_DIR / "references"
    ref_dir.mkdir(exist_ok=True)
    graph = []
    for p in products:
        node = {
            "@type": "Product", "@id": p["url"], "url": p["url"],
            "name": p.get("title_en") or CAT_EN.get(p["category_slug"], p["category_slug"]),
            "sku": p.get("sku"), "category": CAT_EN.get(p["category_slug"], p["category_slug"]),
            "description": (p.get("description_en") or "")[:1000] or None,
            "brand": {"@type": "Brand", "name": "Vargov Design"},
            "manufacturer": {"@type": "Organization", "name": "Vargov Design"},
            "image": p.get("gallery") or None,
            "offers": {"@type": "Offer", "priceCurrency": "USD",
                       "availability": "https://schema.org/PreOrder", "url": p["url"]},
        }
        graph.append({k: v for k, v in node.items() if v is not None})
    (ref_dir / "schema-products.jsonld").write_text(
        json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2),
        encoding="utf-8")

    print(f"EN build: {len(products)} products, {len(unresolved)} still containing Cyrillic residue")
    if unresolved:
        report = SCAN_DIR / "en_unresolved.txt"
        with open(report, "w", encoding="utf-8") as f:
            for p in unresolved:
                f.write(f"--- {p.get('sku')} ({p['url']}) ---\n")
                f.write(f"title_en: {p['title_en']}\ndesc_en: {p['description_en']}\n\n")
        print(f"See {report} for items needing new phrase-dictionary entries")


if __name__ == "__main__":
    build_en()
