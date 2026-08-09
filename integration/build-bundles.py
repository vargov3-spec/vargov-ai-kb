#!/usr/bin/env python3
# Сборка пакетов integration/*.json из content/. Запуск из корня репозитория.

import re, json, glob, os, hashlib
LOCALES=['ru','en','de','fr','it','es','vi','ar']
BASE='content/product-descriptions'

# ---------- КАРТОЧКИ ТОВАРОВ ----------
def files(loc):
    d = BASE if loc=='ru' else f'{BASE}/{loc}'
    return sorted(glob.glob(f'{d}/batch-*.md'))+sorted(glob.glob(f'{d}/samples-*.md'))

def parse_item(chunk):
    """chunk = текст одного товара, начиная со строки '## LCxxxx — Тип'"""
    lines=chunk.split('\n')
    head=lines[0]
    m=re.match(r'##\s+(LC[0-9-]+)\s+—\s+(.*)$', head)
    if not m: return None
    sku, rest = m.group(1), m.group(2).strip()
    award=False
    if '·' in rest and 'Award Winning' in rest:
        rest = rest.split('·')[0].strip(); award=True
    am=re.match(r'^(.*?)\s*\(Award Winning\)\s*$', rest)
    if am:
        rest=am.group(1).strip(); award=True
    paras=[p.strip() for p in '\n'.join(lines[1:]).split('\n\n') if p.strip()]
    body, blocks = [], {}
    order=[]
    for p in paras:
        bm=re.match(r'^\*\*(.+?)\*\*\s*(.*)$', p, re.S)
        if bm:
            label=bm.group(1).strip(); val=bm.group(2).strip()
            blocks[label]=val; order.append(label)
        else:
            body.append(p)
    made = body.pop() if body else None      # последний абзац без метки = «на заказ»
    where = blocks[order[0]] if len(order)>0 else None
    style = blocks[order[1]] if len(order)>1 else None
    return sku, {
        'type': rest, 'awardWinning': award,
        'paragraphs': body, 'whereItWorks': where, 'style': style,
        'madeToOrder': made,
        'labels': {'whereItWorks': order[0] if order else None,
                   'style': order[1] if len(order)>1 else None},
    }

products={}
prod_files={}
for loc in LOCALES:
    prod_files[loc]=[]
    for p in files(loc):
        raw=open(p,encoding='utf-8').read()
        prod_files[loc].append(os.path.basename(p))
        chunks=re.split(r'\n---\n', raw)
        for c in chunks:
            c=c.strip()
            if not c.startswith('## LC'): continue
            r=parse_item(c)
            if not r: continue
            sku,data=r
            data['sourceFile']=os.path.basename(p)
            products.setdefault(sku,{})[loc]=data

# ---------- ЖУРНАЛ ----------
articles={}
for loc in LOCALES:
    for p in sorted(glob.glob(f'content/journal/{loc}/*.md')):
        slug=os.path.basename(p)[:-3]
        raw=open(p,encoding='utf-8').read()
        paras=[x.strip() for x in raw.split('\n\n') if x.strip()]
        title=paras[0].lstrip('# ').strip()
        meta=paras[1]
        cat=date=None
        mm=re.match(r'^[^:]+:\s*(.+?)\s*·\s*[^:]+:\s*(.+?)\s*·\s*Slug:', meta)
        if mm: cat,date=mm.group(1),mm.group(2)
        rest=paras[2:]
        lead=rest[0] if rest else None
        body=rest[1:] if len(rest)>1 else []
        articles.setdefault(slug,{})[loc]={
            'title':title,'category':cat,'date':date,'lead':lead,'body':body}

def sha(o): return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True).encode()).hexdigest()[:16]

prod_bundle={
  'meta':{'kind':'product-descriptions','locales':LOCALES,
          'skuCount':len(products),'generated':'см. git log',
          'note':'Тексты карточек товаров. Ключ — артикул (SKU), затем код языка.',
          'checksum':sha(products)},
  'items':products}
jour_bundle={
  'meta':{'kind':'journal','locales':LOCALES,'articleCount':len(articles),
          'note':'Статьи раздела «Прямая речь». Ключ — slug статьи, затем код языка.',
          'checksum':sha(articles)},
  'articles':articles}

json.dump(prod_bundle,open('integration/products.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
json.dump(jour_bundle,open('integration/journal.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)

print('SKU:',len(products),'| статей:',len(articles))
bad=[s for s,v in products.items() if len(v)!=8]
print('SKU не на 8 языках:',len(bad), bad[:5])
badj=[s for s,v in articles.items() if len(v)!=8]
print('статей не на 8 языках:',len(badj), badj[:5])
miss=[(s,l) for s,v in products.items() for l,d in v.items() if not d['whereItWorks'] or not d['style'] or not d['madeToOrder']]
print('карточек с недобранными блоками:',len(miss), miss[:5])
