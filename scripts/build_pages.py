# -*- coding: utf-8 -*-
"""Собирает docs/ для GitHub Pages: хаб базы знаний и указатель каталога.

Зачем это нужно: github.com закрывает /tree/ от краулеров, поэтому содержимое
репозитория для поисковиков и языковых моделей невидимо. Pages отдаёт обычный
сайт — это единственная дверь внутрь.

Чего здесь сознательно НЕТ: отдельных страниц изделий. Первичен сайт vargov.ru,
и 605 копий карточек на github.io конкурировали бы с ним в выдаче. Указатель
ведёт на канонические адреса сайта, а рядом даёт машиночитаемые файлы базы.

Заодно собирается llms-full.txt в корне: дословно llms.txt (RU) + en/llms.txt (EN)
с датой сборки. До 03.10.2026 его латали руками, шапка «Собрано 2026-09-05» стояла
месяц, а в теле жили «более 300 артикулов» и не было двух гайдов и ссылки на zh.

Перед сборкой — сверки чисел llms-файлов с данными репозитория (число записей
references/3ddd-models.json, подборки «по пространству» против зеркала llms.txt
сайта) и узла бренда в графе базы (адрес Organization = адрес Store, год, регионы,
sameAs, zh у Dataset — см. check_brand_graph). Расхождение печатается и даёт код
выхода 2 — файлы при этом собираются.

python scripts/build_pages.py --check — те же сверки плюс «сгенерированное не
отстало от источника» (llms-full.txt содержит llms.txt и en/llms.txt дословно, хаб
печатает текущее число наград), БЕЗ записи файлов; код выхода 1 при расхождении.
Этот режим для канарейки (.github/workflows/update-knowledge-base.yml): правка
llms.txt руками без пересборки иначе молча оставляет llms-full.txt старым (A110).

robots.txt в docs/ отдаётся по адресу /vargov-ai-kb/robots.txt, а краулеры читают
robots.txt только из корня хоста (RFC 9309) — vargov3-spec.github.io/robots.txt
отвечает 404, то есть обход разрешён целиком, но строку Sitemap отсюда никто не
прочтёт. Карту сайта Pages нужно отдавать иначе: Search Console / Bing Webmaster
или корневой репозиторий vargov3-spec.github.io со своим robots.txt.
"""
import json
import io
import os
import re
import html
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
RAW = "https://raw.githubusercontent.com/vargov3-spec/vargov-ai-kb/main/"
REPO = "https://github.com/vargov3-spec/vargov-ai-kb/"
BASE = "https://vargov3-spec.github.io/vargov-ai-kb/"
# Написание имени — как на сайте и в логотипе (Organization.name в seo.ts, подпись
# пресс-фото «© Vargov®Design» на vargov.ru/press): без пробела. До 03.10.2026 хаб
# писал «Vargov® Design», и Organization хаба расходился с графом базы по имени.
BRAND = "Vargov®Design"
ORG_ID = "https://vargov.ru#organization"
PERSON_ID = "https://vargov.ru#person"
SHOWROOM_ID = "https://vargov.ru#showroom"
DATASET_ID = "https://github.com/vargov3-spec/vargov-ai-kb#dataset"

# Узел бренда в графе базы носит тот же @id, что на сайте, поэтому обязан говорить то же,
# что сайт (src/lib/seo.ts:182 foundingDate, :189–190 адрес, :240 areaServed;
# src/lib/orgGraph.ts:44 Hugging Face, :54–55 Medium и LinkedIn основателя; коммит c9c03f5,
# 02.10.2026). 03.10 эти поля исправлены в references/*.jsonld, а генератор
# scripts/build_from_site.py их ещё не знает: локальная пересборка молча вернёт латинский
# адрес и выбросит остальное (A285, A205, A153, A123). Сверка ниже ловит такой откат.
SITE_FOUNDING_DATE = "2018"            # первые работы бренда, слово владельца 02.10.2026
SITE_AREA_SERVED = {"RU", "AE", "VN"}  # Москва, Дубай, Ханой
ORG_SAME_AS_REQUIRED = ("https://huggingface.co/vargov-design",)
PERSON_SAME_AS_REQUIRED = ("https://medium.com/@antonvargov",
                           "https://www.linkedin.com/in/anton-vargov-95938643a")

CSS = """
:root{--ink:#14161a;--dim:#6b7280;--line:#e5e7eb;--bg:#fbfbfc;--acc:#1a4fd6}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:32px 20px 72px}
h1{font-size:30px;line-height:1.2;margin:0 0 8px;letter-spacing:-.01em}
h2{font-size:19px;margin:36px 0 10px;letter-spacing:-.01em}
p{margin:0 0 12px}
.lede{color:var(--dim);max-width:70ch}
a{color:var(--acc);text-decoration:none}
a:hover{text-decoration:underline}
ul{margin:0 0 12px;padding-left:20px}
li{margin:3px 0}
code{background:#eef0f3;border-radius:4px;padding:1px 5px;font-size:13px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.card{border:1px solid var(--line);border-radius:10px;padding:14px 16px;background:#fff}
.card h3{margin:0 0 6px;font-size:15px}
.card p{margin:0;color:var(--dim);font-size:14px}
table{border-collapse:collapse;width:100%;font-size:14px;background:#fff}
th,td{border-bottom:1px solid var(--line);padding:7px 9px;text-align:left;vertical-align:top}
th{position:sticky;top:0;background:#fff;font-weight:600}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:10px}
.muted{color:var(--dim);font-size:14px}
.foot{margin-top:44px;padding-top:18px;border-top:1px solid var(--line);color:var(--dim);font-size:13px}
@media (prefers-color-scheme:dark){
 :root{--ink:#e8eaed;--dim:#9aa2ad;--line:#2a2e35;--bg:#0f1114;--acc:#7aa2ff}
 .card,table,th{background:#151920}
 code{background:#22262e}
}
"""

FOOT = (
    '<div class="foot">Первичный источник фактов — сайт бренда '
    '<a href="https://vargov.ru">vargov.ru</a>. Этот репозиторий следует за ним. '
    "Данные — CC BY 4.0; фотографии и товарный знак лицензией не передаются."
    "</div></div>\n"
)

BOTS = ("GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-Web",
        "anthropic-ai", "PerplexityBot", "Google-Extended", "CCBot",
        "Applebot-Extended", "YandexBot")


def esc(s):
    return html.escape("" if s is None else str(s), quote=True)


def head(title, desc, canonical, extra=""):
    return (
        "<!doctype html>\n<html lang=\"ru\">\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
        "<title>" + esc(title) + "</title>\n"
        "<meta name=\"description\" content=\"" + esc(desc) + "\">\n"
        "<meta name=\"robots\" content=\"index,follow,max-snippet:-1,max-image-preview:large\">\n"
        "<link rel=\"canonical\" href=\"" + canonical + "\">\n"
        "<style>" + CSS + "</style>\n" + extra + "\n<div class=\"wrap\">\n"
    )


def build():
    products = json.load(io.open(os.path.join(ROOT, "datasets", "products.json"), encoding="utf-8"))
    # Число наград — из organization.jsonld (его пишет ночная сверка из awardsCount() сайта),
    # а не литералом: литерал «23» простоял с 08.09 при 25 на бою.
    org = json.load(io.open(os.path.join(ROOT, "references", "organization.jsonld"), encoding="utf-8"))
    # organization.jsonld — это {"@graph": [...]}, награды лежат у узла Organization (регрессия 02.10:
    # org.get("award") давал 0, хаб печатал «0 наград»). Меньше 20 — сборку остановить, а не печатать.
    org_node = next((n for n in org.get("@graph", [org]) if n.get("@type") == "Organization"), {})
    n_awards_int = len(org_node.get("award", []))
    if n_awards_int < 20:
        raise SystemExit(f"build_pages: у Organization в organization.jsonld {n_awards_int} наград — меньше 20, хаб не собираю")
    n_awards = str(n_awards_int)
    os.makedirs(DOCS, exist_ok=True)
    io.open(os.path.join(DOCS, ".nojekyll"), "w").write("")
    today = datetime.date.today().isoformat()

    cats, labels = {}, {}
    for p in products:
        cats.setdefault(p.get("category"), []).append(p)
    for c, arr in cats.items():
        lab = arr[0].get("category_label") or {}
        labels[c] = (lab.get("ru") or c, lab.get("en") or c)
    order = ["lighting", "decorative", "sculptural-decor", "floor-table-lamps"]

    # Организация хаба — тот же узел, что в references/organization.jsonld и на сайте:
    # тот же @id и то же имя (берутся из графа базы, а не литералом). Без @id и с
    # другим именем это была для машины вторая организация (аудит 03.10, A285).
    if org_node.get("@id") != ORG_ID or org_node.get("name") != BRAND:
        raise SystemExit("build_pages: у Organization в organization.jsonld @id/имя не "
                         f"{ORG_ID} / {BRAND}: {org_node.get('@id')} / {org_node.get('name')}")
    org = {
        "@context": "https://schema.org", "@type": "Organization",
        "@id": org_node["@id"], "name": org_node["name"], "url": "https://vargov.ru",
        "sameAs": [REPO.rstrip("/"), "https://sketchfab.com/vargov"],
        "description": "Russian brand of author's lighting and decorative compositions.",
    }
    dataset = {
        "@context": "https://schema.org", "@type": "Dataset",
        "name": BRAND + " — open catalogue dataset",
        "description": ("605 lighting and decorative compositions: codes, categories, "
                        "descriptions in eight languages, awards, links to 3D models."),
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "creator": {"@id": ORG_ID},
        "url": BASE, "isAccessibleForFree": True,
        "distribution": [
            {"@type": "DataDownload", "encodingFormat": "application/json",
             "contentUrl": RAW + "datasets/products.json"},
            {"@type": "DataDownload", "encodingFormat": "application/x-ndjson",
             "contentUrl": RAW + "datasets/products.jsonl"},
            {"@type": "DataDownload", "encodingFormat": "text/csv",
             "contentUrl": RAW + "datasets/products.csv"},
            {"@type": "DataDownload", "encodingFormat": "application/ld+json",
             "contentUrl": RAW + "references/catalog.jsonld"},
        ],
    }
    jsonld = ('<script type="application/ld+json">' + json.dumps(org, ensure_ascii=False) + "</script>\n"
              '<script type="application/ld+json">' + json.dumps(dataset, ensure_ascii=False) + "</script>")

    n_award = sum(1 for p in products if p.get("award_winning"))
    n_cert = sum(1 for p in products if p.get("cert"))

    o = [head(BRAND + " — открытая база знаний",
              "Открытые данные бренда " + BRAND + ": 605 композиций, граф schema.org, "
              "проверенные факты и награды.", BASE, jsonld)]
    o.append("<h1>" + esc(BRAND) + " — открытая база знаний</h1>")
    o.append('<p class="lede">Российский бренд авторских световых и декоративных композиций. '
             "Основатель и главный дизайнер — Антон Варгов. Собственное производство, "
             "изготовление под заказ: каждая композиция собирается под конкретный интерьер.</p>")
    o.append('<p class="lede">A Russian brand of author’s lighting and decorative compositions. '
             "This repository is the machine-readable knowledge base; the primary source is "
             '<a href="https://vargov.ru/en">vargov.ru</a>.</p>')

    o.append('<h2>Цифры</h2><div class="grid">')
    for t, v in (("Композиций в каталоге", "605, артикулы LC0001…LC0602"),
                 ("Международных наград", n_awards),
                 ("Композиций-лауреатов", str(n_award)),
                 ("С сертификатом ЕАЭС", str(n_cert)),
                 ("Языков описаний", "8"),
                 ("Лицензия данных", "CC BY 4.0")):
        o.append('<div class="card"><h3>' + esc(t) + "</h3><p>" + esc(v) + "</p></div>")
    o.append("</div>")

    o.append("<h2>Открытые данные</h2><ul>")
    for path, note in (("datasets/products.json", "605 композиций, описания на восьми языках"),
                       ("datasets/products.jsonl", "то же, построчно"),
                       ("datasets/products.csv", "то же, таблицей"),
                       ("en/datasets/products.json", "только английский"),
                       ("references/catalog.jsonld", "граф schema.org: Organization, Person, Store, Dataset и 605 Product"),
                       ("references/organization.jsonld", "карточка организации"),
                       ("references/dataset.jsonld", "описание датасета"),
                       ("references/3ddd-models.json", "артикул → карточка 3D-модели"),
                       ("references/sketchfab-models.json", "артикул → модель на Sketchfab")):
        o.append('<li><a href="' + RAW + path + '"><code>' + esc(path) + "</code></a> — "
                 '<span class="muted">' + esc(note) + "</span></li>")
    o.append("</ul>")

    o.append("<h2>Проверенные факты</h2><ul>")
    for path, note in (("knowledge/brand.md", "факты о бренде"),
                       ("knowledge/awards-verified.md", n_awards + " наград со ссылками на страницы премий"),
                       ("knowledge/pr-kit.md", "пресс-кит"),
                       ("knowledge/external-references.md", "внешние подтверждения"),
                       ("guides/russian-lighting-design.md", "эссе «Русский световой дизайн»"),
                       ("llms.txt", "карта для языковых моделей"),
                       ("llms-full.txt", "та же карта на двух языках одним файлом (RU + EN)"),
                       ("zh/llms.txt", "карта на китайском — только для базы знаний")):
        o.append('<li><a href="' + RAW + path + '"><code>' + esc(path) + "</code></a> — "
                 '<span class="muted">' + esc(note) + "</span></li>")
    o.append("</ul>")

    o.append("<h2>Указатель каталога</h2><ul>")
    o.append('<li><a href="catalog.html">Все 605 композиций</a> — '
             '<span class="muted">артикул, тип, ссылки на карточки сайта</span></li>')
    for c in order:
        if c in cats:
            ru, en = labels[c]
            o.append("<li>" + esc(ru) + " / " + esc(en) + " — " + str(len(cats[c])) +
                     ' <span class="muted">(<a href="' + RAW + "collections/" + c + ".md\">collections/" +
                     esc(c) + ".md</a>)</span></li>")
    o.append("</ul>")

    o.append("<h2>Пресс</h2>")
    o.append('<p class="lede">Десять фотографий до 2000 px и логотип свободны для редакционного '
             'использования с указанием «' + BRAND + '»: <a href="' + REPO + 'tree/main/press">press/</a>. '
             'Пресс-кит бренда — <a href="https://vargov.ru/en/press">vargov.ru/en/press</a>.</p>')
    o.append(FOOT)
    io.open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8", newline="\n").write("\n".join(o))

    c = [head("Указатель каталога — " + BRAND,
              "Все 605 композиций " + BRAND + ": артикул, тип, раздел, ссылки на карточки.",
              BASE + "catalog.html")]
    c.append('<p class="muted"><a href="./">← база знаний</a></p>')
    c.append("<h1>Указатель каталога</h1>")
    c.append('<p class="lede">605 композиций. Карточки живут на сайте бренда — здесь только '
             "указатель и машиночитаемые файлы. ★ отмечены лауреаты премий.</p>")
    c.append('<div class="scroll"><table><thead><tr><th>Артикул</th><th>Тип</th><th>Type</th>'
             "<th>Раздел</th><th>Карточка</th><th>Данные</th></tr></thead><tbody>")
    for p in sorted(products, key=lambda x: x["code"]):
        t = p.get("type") or {}
        u = p.get("urls") or {}
        ru_lab = labels.get(p.get("category"), ("", ""))[0]
        mark = " ★" if p.get("award_winning") else ""
        c.append("<tr><td><b>" + esc(p["code"]) + "</b>" + mark + "</td><td>" + esc(t.get("ru")) +
                 "</td><td>" + esc(t.get("en")) + "</td><td>" + esc(ru_lab) + "</td>"
                 '<td><a href="' + esc(u.get("ru")) + '">RU</a> · <a href="' + esc(u.get("en")) + '">EN</a></td>'
                 '<td><a href="' + RAW + "products/" + esc(p.get("category")) + "/" + esc(p["code"]) +
                 '.md">md</a></td></tr>')
    c.append("</tbody></table></div>")
    c.append(FOOT)
    io.open(os.path.join(DOCS, "catalog.html"), "w", encoding="utf-8", newline="\n").write("\n".join(c))

    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, freq, pri in ((BASE, "weekly", "1.0"), (BASE + "catalog.html", "weekly", "0.8")):
        sm.append("  <url><loc>" + u + "</loc><lastmod>" + today +
                  "</lastmod><changefreq>" + freq + "</changefreq><priority>" + pri + "</priority></url>")
    sm.append("</urlset>")
    io.open(os.path.join(DOCS, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write("\n".join(sm) + "\n")

    robots = ["# Этот файл лежит в подпапке /vargov-ai-kb/ и краулерами не читается: robots.txt",
              "# действует только из корня хоста (RFC 9309). Оставлен как документ намерения.",
              "User-agent: *", "Allow: /", "",
              "# Краулеры языковых моделей разрешены явно — ради них эта страница и сделана.", ""]
    for b in BOTS:
        robots += ["User-agent: " + b, "Allow: /", ""]
    robots += ["Sitemap: " + BASE + "sitemap.xml", ""]
    io.open(os.path.join(DOCS, "robots.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(robots))

    print("docs/index.html   %6d байт" % os.path.getsize(os.path.join(DOCS, "index.html")))
    print("docs/catalog.html %6d байт, строк %d"
          % (os.path.getsize(os.path.join(DOCS, "catalog.html")), len(products)))
    print("docs/sitemap.xml, docs/robots.txt, docs/.nojekyll — готовы")



LLMS_FULL_HEAD = """# {brand} — llms-full.txt

Полная карта на двух языках: дословно llms.txt (RU) и en/llms.txt (EN) этого
репозитория, склеенные сборщиком scripts/build_pages.py. Собрано {today}.
Китайская версия — отдельный файл zh/llms.txt (ссылка — в разделах
«Языковые версии» / «Language versions» ниже).

Канонический источник фактов — https://vargov.ru/llms.txt, он генерируется
самим сайтом. Проверенные награды со ссылками на страницы премий и сертификаты —
knowledge/awards-verified.md. Факты о бренде — knowledge/brand.md.

Пер-товарные датасеты ({n} позиций x 8 языков) пересобираются локальным
сборщиком scripts/build_from_site.py и опубликованы под лицензией CC BY 4.0 —
ссылки в разделах «Открытые данные» / «Open data» ниже.

---

"""


def read(rel):
    return io.open(os.path.join(ROOT, rel), encoding="utf-8").read()


def build_llms_full():
    """llms-full.txt = шапка + llms.txt + en/llms.txt, дословно. Руками не править."""
    ru, en = read("llms.txt").rstrip("\n"), read("en/llms.txt").rstrip("\n")
    n = len(json.load(io.open(os.path.join(ROOT, "datasets", "products.json"), encoding="utf-8")))
    text = (LLMS_FULL_HEAD.format(brand=BRAND, today=datetime.date.today().isoformat(), n=n)
            + ru + "\n\n---\n\n" + en + "\n")
    path = os.path.join(ROOT, "llms-full.txt")
    io.open(path, "w", encoding="utf-8", newline="\n").write(text)
    full = read("llms-full.txt")
    if ru not in full or en not in full:
        raise SystemExit("build_pages: llms-full.txt не содержит llms.txt и en/llms.txt целиком")
    print("llms-full.txt     %6d байт (RU + EN)" % os.path.getsize(path))


def check_llms_numbers():
    """Числа llms-файлов против данных репозитория. Возвращает список расхождений."""
    problems = []
    texts = {rel: read(rel) for rel in ("llms.txt", "en/llms.txt", "zh/llms.txt")}
    # 1) Реестр 3D-карточек: число записей в тексте = len(items). «604» простояло
    #    с 02.10, когда фантом LC0104-1 из файла уже убрали (аудит 03.10, A108).
    n3 = len(json.load(io.open(os.path.join(ROOT, "references", "3ddd-models.json"),
                                encoding="utf-8"))["items"])
    pats = {"llms.txt": r"\((\d+) записи", "en/llms.txt": r"\((\d+) entries",
            "zh/llms.txt": r"（(\d+) 条"}
    for rel, pat in pats.items():
        m = re.search(pat, texts[rel])
        if not m or int(m.group(1)) != n3:
            problems.append(f"{rel}: записей 3ddd-models.json в тексте "
                            f"{m.group(1) if m else 'нет'}, в файле {n3}")
    # 2) Подборки «по пространству»: тот же набор /for/<key>, что в llms.txt сайта
    #    (зеркало снимает ночная сверка). atrium и banquet появились на сайте 10.09,
    #    база их не знала до 03.10 (A257).
    if os.path.isfile(os.path.join(ROOT, "references", "vargov.ru-llms.txt")):
        site = set(re.findall(r"vargov\.ru/en/for/([a-z-]+)", read("references/vargov.ru-llms.txt")))
        for rel, pat in (("llms.txt", r"vargov\.ru/for/([a-z-]+)"),
                         ("en/llms.txt", r"vargov\.ru/en/for/([a-z-]+)"),
                         ("zh/llms.txt", r"vargov\.ru/en/for/([a-z-]+)")):
            kb = set(re.findall(pat, texts[rel]))
            if site and kb != site:
                problems.append(f"{rel}: подборки по пространству расходятся с сайтом — "
                                f"нет {sorted(site - kb)}, лишние {sorted(kb - site)}")
    else:
        print("ВНИМАНИЕ: нет references/vargov.ru-llms.txt — подборки с сайтом не сверены")
    return problems


def graph_nodes(rel):
    """Узлы JSON-LD файла по @id (файл — либо {"@graph": [...]}, либо один узел)."""
    doc = json.load(io.open(os.path.join(ROOT, rel), encoding="utf-8"))
    return {n.get("@id"): n for n in doc.get("@graph", [doc]) if isinstance(n, dict)}


def check_brand_graph():
    """Узел бренда в references/*.jsonld против сайта и сам с собой. Список расхождений."""
    problems = []
    org_f = graph_nodes("references/organization.jsonld")
    cat_f = graph_nodes("references/catalog.jsonld")
    ds_f = graph_nodes("references/dataset.jsonld")

    def addr(n):
        a = (n or {}).get("address") or {}
        return f"«{a.get('streetAddress')}, {a.get('addressLocality')}»"

    for rel, g in (("references/organization.jsonld", org_f), ("references/catalog.jsonld", cat_f)):
        org, person, store = g.get(ORG_ID), g.get(PERSON_ID), g.get(SHOWROOM_ID)
        if not (org and person and store):
            problems.append(f"{rel}: нет узла Organization, Person или Store с @id сайта")
            continue
        # Один физический шоурум: адрес бренда пишется так же, как адрес Store в том же
        # графе, — русской записью, как на сайте (иначе Google не свяжет его с Картами).
        if org.get("address") != store.get("address"):
            problems.append(f"{rel}: адрес Organization {addr(org)} не совпадает с адресом "
                            f"Store {addr(store)} — генератор вернул латинский адрес?")
        if org.get("foundingDate") != SITE_FOUNDING_DATE:
            problems.append(f"{rel}: foundingDate у Organization {org.get('foundingDate')!r}, "
                            f"на сайте {SITE_FOUNDING_DATE!r}")
        if set(org.get("areaServed") or []) != SITE_AREA_SERVED:
            problems.append(f"{rel}: areaServed у Organization {org.get('areaServed')}, "
                            f"на сайте {sorted(SITE_AREA_SERVED)}")
        for node, need, who in ((org, ORG_SAME_AS_REQUIRED, "Organization"),
                                (person, PERSON_SAME_AS_REQUIRED, "Person")):
            miss = [u for u in need if u not in (node.get("sameAs") or [])]
            if miss:
                problems.append(f"{rel}: в sameAs у {who} нет {miss} (на сайте есть)")
    # Один @id — один узел: в двух файлах базы он должен совпадать. Награды Person ночная
    # сверка пишет только в catalog.jsonld, поэтому у Person сравниваются имя и sameAs.
    def norm(v):
        return sorted(v) if isinstance(v, list) and all(isinstance(x, str) for x in v) else v
    for nid, keys in ((ORG_ID, ("name", "address", "foundingDate", "areaServed", "sameAs")),
                      (PERSON_ID, ("name", "sameAs")), (SHOWROOM_ID, ("name", "address"))):
        a, b = org_f.get(nid) or {}, cat_f.get(nid) or {}
        diff = [k for k in keys if norm(a.get(k)) != norm(b.get(k))]
        if diff:
            problems.append(f"{nid}: organization.jsonld и catalog.jsonld расходятся в {diff}")
    # Китайский слой датасета: если файлы лежат в datasets/, Dataset обязан их называть.
    zh = [rel for rel in ("datasets/products-zh.json", "datasets/products-zh.jsonl")
          if os.path.isfile(os.path.join(ROOT, rel))]
    for rel, g in (("references/dataset.jsonld", ds_f), ("references/catalog.jsonld", cat_f)):
        ds = g.get(DATASET_ID)
        if not ds:
            problems.append(f"{rel}: нет узла Dataset {DATASET_ID}")
            continue
        if zh and "zh" not in (ds.get("inLanguage") or []):
            problems.append(f"{rel}: в inLanguage у Dataset нет «zh», а {zh[0]} опубликован")
        urls = [d.get("contentUrl", "") for d in ds.get("distribution") or []]
        miss = [z for z in zh if not any(u.endswith("/" + z) for u in urls)]
        if miss:
            problems.append(f"{rel}: в distribution у Dataset нет {miss}")
    return problems


def check_generated():
    """Сгенерированное не отстало от источников. Ничего не пишет. Список расхождений."""
    problems = []
    ru, en = read("llms.txt").rstrip("\n"), read("en/llms.txt").rstrip("\n")
    full = read("llms-full.txt")
    for rel, part in (("llms.txt", ru), ("en/llms.txt", en)):
        if part not in full:
            problems.append(f"llms-full.txt не содержит {rel} дословно — правили руками без "
                            "пересборки: python scripts/build_pages.py")
    org = graph_nodes("references/organization.jsonld").get(ORG_ID) or {}
    n_awards = len(org.get("award", []))
    card = "<h3>Международных наград</h3><p>" + str(n_awards) + "</p>"
    if card not in read("docs/index.html"):
        problems.append(f"docs/index.html не печатает текущее число наград ({n_awards} в "
                        "organization.jsonld) — хаб не пересобран: python scripts/build_pages.py")
    return problems


if __name__ == "__main__":
    import sys
    if "--check" in sys.argv[1:]:
        # Режим канарейки: только чтение, ни одного файла не пишет.
        probs = check_llms_numbers() + check_brand_graph() + check_generated()
        for p in probs:
            print("РАСХОЖДЕНИЕ:", p)
        if probs:
            raise SystemExit(1)
        print("build_pages --check: llms-файлы, граф бренда и сгенерированные файлы в порядке")
        raise SystemExit(0)
    probs = check_llms_numbers() + check_brand_graph()
    build()
    build_llms_full()
    for p in probs:
        print("РАСХОЖДЕНИЕ:", p)
    if probs:
        raise SystemExit(2)
