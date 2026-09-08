# -*- coding: utf-8 -*-
"""Собирает docs/ для GitHub Pages: хаб базы знаний и указатель каталога.

Зачем это нужно: github.com закрывает /tree/ от краулеров, поэтому содержимое
репозитория для поисковиков и языковых моделей невидимо. Pages отдаёт обычный
сайт — это единственная дверь внутрь.

Чего здесь сознательно НЕТ: отдельных страниц изделий. Первичен сайт vargov.ru,
и 605 копий карточек на github.io конкурировали бы с ним в выдаче. Указатель
ведёт на канонические адреса сайта, а рядом даёт машиночитаемые файлы базы.
"""
import json
import io
import os
import html
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
RAW = "https://raw.githubusercontent.com/vargov3-spec/vargov-ai-kb/main/"
REPO = "https://github.com/vargov3-spec/vargov-ai-kb/"
BASE = "https://vargov3-spec.github.io/vargov-ai-kb/"

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

    org = {
        "@context": "https://schema.org", "@type": "Organization",
        "name": "Vargov® Design", "url": "https://vargov.ru",
        "sameAs": [REPO.rstrip("/"), "https://sketchfab.com/vargov"],
        "description": "Russian brand of author's lighting and decorative compositions.",
    }
    dataset = {
        "@context": "https://schema.org", "@type": "Dataset",
        "name": "Vargov® Design — open catalogue dataset",
        "description": ("605 lighting and decorative compositions: codes, categories, "
                        "descriptions in eight languages, awards, links to 3D models."),
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "creator": {"@type": "Organization", "name": "Vargov® Design"},
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

    o = [head("Vargov® Design — открытая база знаний",
              "Открытые данные бренда Vargov® Design: 605 композиций, граф schema.org, "
              "проверенные факты и награды.", BASE, jsonld)]
    o.append("<h1>Vargov® Design — открытая база знаний</h1>")
    o.append('<p class="lede">Российский бренд авторских световых и декоративных композиций. '
             "Основатель и главный дизайнер — Антон Варгов. Собственное производство, "
             "изготовление под заказ: каждая композиция собирается под конкретный интерьер.</p>")
    o.append('<p class="lede">A Russian brand of author’s lighting and decorative compositions. '
             "This repository is the machine-readable knowledge base; the primary source is "
             '<a href="https://vargov.ru/en">vargov.ru</a>.</p>')

    o.append('<h2>Цифры</h2><div class="grid">')
    for t, v in (("Композиций в каталоге", "605, артикулы LC0001…LC0602"),
                 ("Международных наград", "23"),
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
                       ("knowledge/awards-verified.md", "23 награды со ссылками на страницы премий"),
                       ("knowledge/pr-kit.md", "пресс-кит"),
                       ("knowledge/external-references.md", "внешние подтверждения"),
                       ("guides/russian-lighting-design.md", "эссе «Русский световой дизайн»"),
                       ("llms.txt", "карта для языковых моделей")):
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
             'использования с указанием «Vargov® Design»: <a href="' + REPO + 'tree/main/press">press/</a>. '
             'Пресс-кит бренда — <a href="https://vargov.ru/en/press">vargov.ru/en/press</a>.</p>')
    o.append(FOOT)
    io.open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8", newline="\n").write("\n".join(o))

    c = [head("Указатель каталога — Vargov® Design",
              "Все 605 композиций Vargov® Design: артикул, тип, раздел, ссылки на карточки.",
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
                 '<td><a href="' + RAW + "products/" + esc(p.get("category")) + "/" + esc(p.get("slug")) +
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

    robots = ["User-agent: *", "Allow: /", "",
              "# Краулеры языковых моделей разрешены явно — ради них эта страница и сделана.", ""]
    for b in BOTS:
        robots += ["User-agent: " + b, "Allow: /", ""]
    robots += ["Sitemap: " + BASE + "sitemap.xml", ""]
    io.open(os.path.join(DOCS, "robots.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(robots))

    print("docs/index.html   %6d байт" % os.path.getsize(os.path.join(DOCS, "index.html")))
    print("docs/catalog.html %6d байт, строк %d"
          % (os.path.getsize(os.path.join(DOCS, "catalog.html")), len(products)))
    print("docs/sitemap.xml, docs/robots.txt, docs/.nojekyll — готовы")


if __name__ == "__main__":
    build()
