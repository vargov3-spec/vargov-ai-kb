#!/usr/bin/env python3
"""Сборка пакетов integration/*.json из content/. Запуск из корня репозитория:

    python3 integration/build-bundles.py

Источник правды — файлы в content/. Этот скрипт только преобразует их
в машиночитаемый вид; JSON руками не редактируется.
"""
import re, json, glob, os, hashlib, sys
from datetime import datetime, timezone

LOCALES = ['ru', 'en', 'de', 'fr', 'it', 'es', 'vi', 'ar']
RTL = {'ar'}
BASE = 'content/product-descriptions'
OUT = 'integration'

errors = []


# ────────────────────────────── КАРТОЧКИ ТОВАРОВ ──────────────────────────────

def product_files(loc):
    d = BASE if loc == 'ru' else f'{BASE}/{loc}'
    return sorted(glob.glob(f'{d}/batch-*.md')) + sorted(glob.glob(f'{d}/samples-*.md'))


def parse_product(chunk, src):
    """chunk — текст одной карточки, начиная со строки '## LCxxxx — Тип'."""
    lines = chunk.split('\n')
    m = re.match(r'##\s+(LC[0-9-]+)\s+—\s+(.*)$', lines[0])
    if not m:
        return None
    sku, rest = m.group(1), m.group(2).strip()

    # Пометка награды встречается в двух формах — сохраняем, какая именно,
    # иначе обратная сборка markdown не сможет выбрать правильную.
    award, award_form = False, None
    if '·' in rest and 'Award Winning' in rest:
        rest, award, award_form = rest.split('·')[0].strip(), True, 'dot'
    else:
        am = re.match(r'^(.*?)\s*\(Award Winning\)\s*$', rest)
        if am:
            rest, award, award_form = am.group(1).strip(), True, 'paren'

    paras = [p.strip() for p in '\n'.join(lines[1:]).split('\n\n') if p.strip()]
    body, labels, values = [], [], []
    for p in paras:
        bm = re.match(r'^\*\*(.+?)\*\*\s*(.*)$', p, re.S)
        if bm:
            labels.append(bm.group(1).strip())
            values.append(bm.group(2).strip())
        else:
            body.append(p)

    if len(labels) != 2 or not body:
        errors.append(f'{src}: {sku} — ожидались 2 блока и финальная строка, '
                      f'найдено блоков {len(labels)}, абзацев {len(body)}')
        return None

    made = body.pop()  # последний абзац без метки — строка про изготовление на заказ

    # Метки хранятся без завершающей точки: вёрстка ставит их подзаголовками.
    strip_dot = lambda s: s[:-1] if s.endswith('.') else s

    return sku, {
        'type': rest,
        'awardWinning': award,
        'awardFormat': award_form,          # 'dot' | 'paren' | None
        'paragraphs': body,
        'whereItWorks': values[0],
        'style': values[1],
        'madeToOrder': made,
        'labels': {'whereItWorks': strip_dot(labels[0]), 'style': strip_dot(labels[1])},
        'sourceFile': src,
    }


products = {}
for loc in LOCALES:
    for path in product_files(loc):
        for chunk in re.split(r'\n---\n', open(path, encoding='utf-8').read()):
            chunk = chunk.strip()
            if chunk.startswith('## LC'):
                r = parse_product(chunk, path)
                if r:
                    products.setdefault(r[0], {})[loc] = r[1]


# ──────────────────────────────── ЖУРНАЛ ────────────────────────────────

# Подписи мета-строки по языкам — нужны для обратной сборки markdown.
META_LABELS = {
    'ru': ('Рубрика', 'Дата'), 'en': ('Category', 'Date'), 'de': ('Rubrik', 'Datum'),
    'fr': ('Rubrique', 'Date'), 'it': ('Rubrica', 'Data'), 'es': ('Sección', 'Fecha'),
    'vi': ('Chuyên mục', 'Ngày'), 'ar': ('القسم', 'التاريخ'),
}

RU_MONTHS = {'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6,
             'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10, 'ноября': 11,
             'декабря': 12}

# Устойчивый код рубрики выводится из русского названия — рубрик ровно 10
# и они соответствуют друг другу во всех языках один к одному.
CATEGORY_IDS = {
    'Философия': 'philosophy', 'Производство': 'production', 'Признание': 'recognition',
    'Выставки': 'exhibitions', 'Монтаж': 'installation', 'Истории': 'stories',
    'Подлинность': 'authenticity', 'Новости': 'news', 'Направления': 'directions',
    'Прямая речь': 'first-person',
}


def iso_date(ru_date):
    m = re.match(r'(\d{1,2})\s+([а-яё]+)\s+(\d{4})', (ru_date or '').strip())
    if not m:
        return None
    d, mon, y = int(m.group(1)), RU_MONTHS.get(m.group(2)), int(m.group(3))
    return f'{y:04d}-{mon:02d}-{d:02d}' if mon else None


def classify(par):
    """Абзац → типизированный блок: пункт списка, подзаголовок или обычный абзац."""
    if par.startswith('- '):
        return {'type': 'li', 'text': par[2:].strip()}
    # Подзаголовок: короткая строка без конечной точки, либо «Плюсы:» / «1. …»
    if len(par) <= 90 and (par.endswith(':') or re.match(r'^\d+[.)]\s', par)) \
            and '\n' not in par:
        return {'type': 'h', 'text': par.rstrip(':').strip()}
    if len(par) <= 60 and not par.endswith(('.', '!', '?', '…')) and '\n' not in par:
        return {'type': 'h', 'text': par}
    return {'type': 'p', 'text': par}


articles = {}
for loc in LOCALES:
    for path in sorted(glob.glob(f'content/journal/{loc}/*.md')):
        slug = os.path.basename(path)[:-3]
        paras = [x.strip() for x in open(path, encoding='utf-8').read().split('\n\n') if x.strip()]
        if len(paras) < 4:
            errors.append(f'{path}: слишком мало блоков ({len(paras)})')
            continue
        title = paras[0].lstrip('# ').strip()
        mm = re.match(r'^[^:]+:\s*(.+?)\s*·\s*[^:]+:\s*(.+?)\s*·\s*Slug:', paras[1])
        if not mm:
            errors.append(f'{path}: не разобрана мета-строка')
            continue
        cat, date = mm.group(1), mm.group(2)
        lead, rest = paras[2], paras[3:]
        articles.setdefault(slug, {})[loc] = {
            'title': title,
            'category': cat,
            'date': date,
            'lead': lead,
            'body': [classify(p) for p in rest],
            'metaLabels': {'category': META_LABELS[loc][0], 'date': META_LABELS[loc][1]},
        }

# Машинная дата и код рубрики берутся из русской версии и общие для всех языков.
article_meta = {}
for slug, per_loc in articles.items():
    ru = per_loc.get('ru', {})
    cid = CATEGORY_IDS.get(ru.get('category'))
    if not cid:
        errors.append(f'{slug}: неизвестная рубрика «{ru.get("category")}»')
    dt = iso_date(ru.get('date'))
    if not dt:
        errors.append(f'{slug}: не разобрана дата «{ru.get("date")}»')
    article_meta[slug] = {'dateISO': dt, 'categoryId': cid}


# ──────────────────────────────── ЗАПИСЬ ────────────────────────────────

def sha(o):
    return hashlib.sha256(json.dumps(o, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]


def dump(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


now = datetime.now(timezone.utc).isoformat(timespec='seconds')
products = {k: products[k] for k in sorted(products)}
articles = {k: articles[k] for k in sorted(articles)}

common = {'schemaVersion': 2, 'locales': LOCALES, 'rtlLocales': sorted(RTL), 'generated': now}

dump({'meta': {'kind': 'product-descriptions', 'skuCount': len(products),
                'checksum': sha(products), **common},
      'items': products}, f'{OUT}/products.json')

dump({'meta': {'kind': 'journal', 'articleCount': len(articles),
                'checksum': sha(articles), **common},
      'articleMeta': article_meta,
      'articles': articles}, f'{OUT}/journal.json')

# Поязычные срезы: странице товара не нужен файл на 8 МБ.
for loc in LOCALES:
    items = {sku: v[loc] for sku, v in products.items() if loc in v}
    dump({'meta': {'kind': 'product-descriptions', 'locale': loc,
                   'dir': 'rtl' if loc in RTL else 'ltr',
                   'skuCount': len(items), 'checksum': sha(items),
                   'generated': now},
          'items': items},
         f'{OUT}/by-locale/products.{loc}.json')

print(f'SKU: {len(products)} | статей: {len(articles)}')
bad = [s for s, v in products.items() if len(v) != len(LOCALES)]
badj = [s for s, v in articles.items() if len(v) != len(LOCALES)]
print(f'SKU не на всех языках: {len(bad)} {bad[:5]}')
print(f'статей не на всех языках: {len(badj)} {badj[:5]}')
if errors:
    print(f'\nОШИБКИ РАЗБОРА ({len(errors)}):')
    for e in errors[:20]:
        print('  -', e)
    sys.exit(1)
print('Ошибок разбора нет.')
