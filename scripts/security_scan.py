"""
Мониторинг целостности vargov.ru и configurator.vargov.ru.

Скачивает страницы сайта (из sitemap.xml) и их JS-бандлы, извлекает все
внешние домены и сверяет с белым списком. Появление нового домена — признак
внедрения чужого кода (пиксель, «ловец номеров», подменённый счётчик).

Два уровня строгости:
  - script/iframe/preconnect (исполняемое/загружаемое) — строгий список SCRIPT_ALLOWLIST;
  - обычные ссылки (href) — более широкий DOMAIN_ALLOWLIST.

Дополнительно сверяет ID счётчиков Яндекс.Метрики с ожидаемыми: чужой или
подменённый счётчик отдаёт поведение посетителей (вебвизор) постороннему аккаунту.

Output: scan/security_report.md. Exit code 1 при любом нарушении — чтобы
GitHub Action упал и владелец получил уведомление.
"""
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIR = ROOT / "scan"
SCAN_DIR.mkdir(exist_ok=True)
REPORT = SCAN_DIR / "security_report.md"

SITEMAP_URL = "https://vargov.ru/sitemap.xml"
EXTRA_PAGES = ["https://configurator.vargov.ru/"]
MAX_PAGES = 40
MAX_JS_PER_HOST = 40

# Домены, которым разрешено отдавать скрипты/фреймы/preconnect.
SCRIPT_ALLOWLIST = {
    "vargov.ru", "www.vargov.ru", "configurator.vargov.ru",
    "mc.yandex.ru",                      # Яндекс.Метрика
    "static.tildacdn.com", "thumb.tildacdn.com",  # фото товаров конфигуратора
}

# Домены, на которые разрешены обычные ссылки (href) и упоминания в JS.
DOMAIN_ALLOWLIST = SCRIPT_ALLOWLIST | {
    "vargov.design",
    "t.me", "wa.me", "www.youtube.com", "rutube.ru", "i.ytimg.com",
    "schema.org", "www.w3.org", "nextjs.org", "react.dev", "reactjs.org", "github.com",
    "3ddd.ru",
}

# Ожидаемые счётчики Метрики: 111091941 — vargov.ru, 89943818 — конфигуратор.
EXPECTED_METRIKA_IDS = {"111091941", "89943818"}

URL_RE = re.compile(r'https?:(?:\\/\\/|//)([a-zA-Z0-9.-]+\.[a-z]{2,})')
SCRIPT_SRC_RE = re.compile(r'<script[^>]+src="(https?://[^"]+)"', re.I)
IFRAME_SRC_RE = re.compile(r'<iframe[^>]+src="(https?://[^"]+)"', re.I)
PRECONNECT_RE = re.compile(r'<link[^>]+rel="(?:preconnect|dns-prefetch)"[^>]+href="(https?://[^"]+)"', re.I)
LOCAL_JS_RE = re.compile(r'(?:src="|href=")(/(?:_next/static|assets)/[^"]+\.js)"')
METRIKA_ID_RE = re.compile(r'(?:tag\.js\?id=|ym\(\s*)(\d{6,})')


def curl(url, max_time=30):
    r = subprocess.run(
        ["curl", "-sS", "-L", "--max-time", str(max_time), "-A", "Mozilla/5.0", url],
        capture_output=True, timeout=max_time + 10)
    return r.stdout.decode("utf-8", errors="ignore") if r.returncode == 0 else ""


def host_of(url):
    m = re.match(r'https?://([^/]+)', url)
    return m.group(1).lower() if m else ""


def main():
    sitemap = curl(SITEMAP_URL)
    pages = re.findall(r'<loc>([^<]+)</loc>', sitemap)[:MAX_PAGES] + EXTRA_PAGES
    if len(pages) <= len(EXTRA_PAGES):
        print("WARN: sitemap пуст или недоступен", file=sys.stderr)

    script_hosts, all_hosts, metrika_ids = {}, {}, {}
    seen_js = set()

    for page in pages:
        html = curl(page)
        if not html:
            print(f"WARN: не скачалась {page}", file=sys.stderr)
            continue
        origin = "https://" + host_of(page)
        for rx in (SCRIPT_SRC_RE, IFRAME_SRC_RE, PRECONNECT_RE):
            for u in rx.findall(html):
                script_hosts.setdefault(host_of(u), set()).add(page)
        for h in URL_RE.findall(html):
            all_hosts.setdefault(h.lower(), set()).add(page)
        for mid in METRIKA_ID_RE.findall(html):
            metrika_ids.setdefault(mid, set()).add(page)
        # Свои JS-бандлы тоже проверяем на зашитые внешние адреса.
        js_paths = [p for p in LOCAL_JS_RE.findall(html)][:MAX_JS_PER_HOST]
        for jp in js_paths:
            js_url = origin + jp
            if js_url in seen_js:
                continue
            seen_js.add(js_url)
            js = curl(js_url)
            for h in URL_RE.findall(js):
                all_hosts.setdefault(h.lower(), set()).add(js_url)
            for mid in METRIKA_ID_RE.findall(js):
                metrika_ids.setdefault(mid, set()).add(js_url)

    def own(h):
        return h == "vargov.ru" or h.endswith(".vargov.ru")

    bad_scripts = {h: p for h, p in script_hosts.items()
                   if h and not own(h) and h not in SCRIPT_ALLOWLIST}
    bad_domains = {h: p for h, p in all_hosts.items()
                   if h and not own(h) and h not in DOMAIN_ALLOWLIST}
    bad_metrika = {i: p for i, p in metrika_ids.items()
                   if i not in EXPECTED_METRIKA_IDS}

    lines = ["# Отчёт мониторинга целостности сайта", "",
             f"Страниц проверено: {len(pages)}, JS-файлов: {len(seen_js)}", ""]
    ok = True
    if bad_scripts:
        ok = False
        lines.append("## ТРЕВОГА: скрипты/фреймы с неизвестных доменов")
        for h, p in sorted(bad_scripts.items()):
            lines.append(f"- `{h}` — {', '.join(sorted(p)[:3])}")
        lines.append("")
    if bad_metrika:
        ok = False
        lines.append("## ТРЕВОГА: неожиданный счётчик Яндекс.Метрики")
        for i, p in sorted(bad_metrika.items()):
            lines.append(f"- id `{i}` — {', '.join(sorted(p)[:3])}")
        lines.append("")
    if bad_domains:
        ok = False
        lines.append("## Внимание: новые внешние домены (ссылки/упоминания)")
        for h, p in sorted(bad_domains.items()):
            lines.append(f"- `{h}` — {', '.join(sorted(p)[:3])}")
        lines.append("")
    if ok:
        lines.append("Нарушений нет: все внешние домены и счётчики Метрики соответствуют белому списку.")
        lines.append("")
        lines.append("Найденные внешние домены: " + ", ".join(sorted(h for h in all_hosts if not own(h))))

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
