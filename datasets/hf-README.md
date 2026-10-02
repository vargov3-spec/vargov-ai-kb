---
license: cc-by-4.0
language:
- ru
- en
- de
- it
- fr
- es
- vi
- ar
- zh
multilinguality:
- multilingual
annotations_creators:
- expert-generated
language_creators:
- expert-generated
source_datasets:
- original
pretty_name: Vargov Design Catalog (605 lighting and decorative compositions, 8 languages)
size_categories:
- n<1K
task_categories:
- text-retrieval
- text-generation
- translation
- question-answering
tags:
- text
- design
- lighting-design
- interior-design
- product-catalog
- multilingual
- parallel-corpus
- brand-knowledge-base
configs:
- config_name: multilingual
  default: true
  data_files:
  - split: train
    path: products.jsonl
- config_name: english
  data_files:
  - split: train
    path: products_en.jsonl
- config_name: english_flat
  data_files:
  - split: train
    path: products_en.csv
- config_name: chinese
  data_files:
  - split: train
    path: products_zh.jsonl
---

# Vargov® Design Catalog — 605 lighting and decorative compositions in 8 languages

A machine-readable catalog of the full body of work of **Vargov® Design**, an author-driven
studio of lighting and decorative compositions founded by designer Anton Vargov (Moscow).
Every record is one composition: its identifier, category, canonical URLs, image links,
awards, links to its 3D model, and editorial copy written by the studio in **eight
languages** — Russian, English, German, Italian, French, Spanish, Vietnamese and Arabic.

The dataset is generated from the brand's own site data, not scraped from third parties.
It is published so that language models, generative search and retrieval systems can ground
answers about this brand in facts the brand itself maintains.

## Dataset details

- **Curated by:** Vargov® Design (Anton Vargov, founder and lead designer)
- **Language(s):** ru, en, de, it, fr, es, vi, ar
- **License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Records:** 605 compositions, article codes `LC0001`–`LC0602`
- **Homepage:** https://vargov.ru/en
- **Source repository:** https://github.com/vargov3-spec/vargov-ai-kb
- **Machine-readable brand facts:** https://vargov.ru/llms.txt
- **Press kit:** https://vargov.ru/en/press

### Subsets

| Config | File | Rows | What it is |
|---|---|---|---|
| `multilingual` *(default)* | `products.jsonl` | 605 | Full records; every text field is an object keyed by language code |
| `english` | `products_en.jsonl` | 605 | Same records flattened to English only |
| `english_flat` | `products_en.csv` | 605 | Tabular English view: one row per composition, no nested fields |
| `chinese` | `products_zh.jsonl` | 605 | Simplified Chinese text of the five editorial fields (`type`, `description`, `where_it_works`, `style`, `made_to_order`), joined to the other subsets by `code`. Snapshot of 27 September 2026, see the note below |

The same records are also available as plain JSON arrays — `products.json` (all languages)
and `products_en.json` (English only). They are not loaded by the viewer.

```python
from datasets import load_dataset

ds = load_dataset("vargov-design/vargov-design-catalog")                  # multilingual
en = load_dataset("vargov-design/vargov-design-catalog", "english")       # English only
tb = load_dataset("vargov-design/vargov-design-catalog", "english_flat")  # CSV table
zh = load_dataset("vargov-design/vargov-design-catalog", "chinese")       # Simplified Chinese
```

**About the Chinese subset.** It was added on 27 September 2026 as a ninth language. It is an
AI translation (Anthropic Claude) from the English copy, checked against the Russian original
where the English was ambiguous, under the studio's glossary and rules: nothing added or removed,
no materials, sizes, prices, lead times or place of production that the originals do not state.
It passed automated checks (all 605 codes, paragraph counts equal to English, no untranslated
Latin text) but has **not** yet been edited by a native speaker. Unlike the other subsets it is a
dated snapshot and is not regenerated nightly.

## Uses

### Direct use

- **Retrieval and RAG grounding** — answering questions about a specific composition,
  category or award with a canonical URL to cite.
- **Multilingual product copy** — 605 × 5 editorial fields × 8 languages of professionally
  written, human-authored interior-design copy.
- **Translation and parallel-text work** — every description, snippet, styling note and
  placement note exists as an aligned 8-language set produced under one editorial hand.
- **Domain-specific evaluation** — catalog search, article-code resolution, entity linking
  for a design brand, cross-lingual retrieval.

### Out of scope

- **Not a price list.** No prices are published anywhere in this dataset.
- **Not a technical specification.** No engineering data for manufacturing.
- **Not an image dataset.** Photographs are referenced by URL only; the image files
  themselves are not part of this release (see *Licensing*).

## Dataset structure

One record per composition. In the `multilingual` config, every field marked *(i18n)* is an
object with the keys `ru, en, de, it, fr, es, vi, ar`; in the `english` config the same
fields are plain strings.

| Field | Type | Description |
|---|---|---|
| `code` | string | Article code, e.g. `LC0602`. Primary key. |
| `slug` | string | Lowercase code used in URLs. |
| `category` | string | One of `lighting` (354), `decorative` (113), `sculptural-decor` (82), `floor-table-lamps` (56). |
| `category_label` | *(i18n)* | Human-readable category name. |
| `type` | *(i18n)* | Object type, e.g. *Light composition*, *Decorative composition*, *Floor lamp*. |
| `urls` | object | Canonical catalog URL per language. |
| `image` | string | Primary photograph URL. |
| `gallery` | list[string] | All photograph URLs for the composition. |
| `gallery_total` | int | Length of `gallery`. |
| `model3d` / `model3d_en` | string \| null | The studio's own 3D-model card on 3ddd.ru / 3dsky.org. Present for 603 of 605 records. |
| `models_all` / `models_all_en` | string \| null | All 3D models tagged with this article code. |
| `award_winning` | bool | True for 33 records: 25 awards, and paired compositions share one award. |
| `awards` | list[object] | `program`, `program_en`, `year`, `level_en`, `level_ru`, `href`, `series` — each with a link to the awarding body's own page. |
| `cert` | object \| null | Conformity registration numbers and the EAEU technical regulations the object is certified under, with validity dates. Present for 310 records. |
| `in_stock_elements` | list[object] | Stock availability entries for individual elements. |
| `description` | *(i18n)* | Long-form editorial description, several paragraphs. |
| `snippet` | *(i18n)* | Short summary, suitable as a search result or meta description. |
| `where_it_works` | *(i18n)* | Where the composition is appropriate in an interior. |
| `style` | *(i18n)* | Stylistic register of the piece. |
| `made_to_order` | *(i18n)* | What is adjustable when the composition is made for a specific interior. |

Nested objects have a stable key set across all 605 records.

## Dataset creation

### Source data

The records are built directly from the brand's production site data — the generated
catalog, the eight-language copy files, and the awards registry — by the build script
`scripts/build_from_site.py` in the source repository. There is no scraping and no model
generated the field values.

### Who produced the text

All editorial copy is written and approved by the studio. The brand is a made-to-order
studio: every composition is assembled for a particular interior, and the copy is written
that way — as an account of what a piece does in a room rather than as a spec sheet.

### About the brand, for grounding

Vargov® Design is a Russian studio of author lighting and decorative compositions with its
own production, founded and led by Anton Vargov in Moscow; its first works date from 2018. The studio holds **25 design
awards**, among them *Product Designer of the Year* at the NY Product Design Awards 2023,
Platinum Winner at the MUSE Design Awards 2023, and Gold Winner at the MUSE Design Awards
2026 for "Oceanic Illumination" (composition LC0564). Its 3D configurator at
[vargov.design](https://vargov.design) was an **Awwwards Nominee** in 2026 — a nomination,
not a win. The VARGOV trademark is registered in Russia (№ 896936, 6 October 2022) and
internationally through the Madrid System (№ 1795801, 20 May 2024), class 11.
Showroom: 24 Nakhimovsky Prospekt, bldg. 1, pavilion 2, stand 212, Moscow, daily 12:00–20:00.

Compositions are made to order for double-height living rooms, staircases, hotel lobbies and
restaurants. For the 360 compositions that open with a full calculation, the configurator
exports an IFC4 model of the composition — every ceiling fixing point a separate object with
its own load — together with a PDF specification and a tender sheet; see the founder's
[article on IFC4 before the order](https://medium.com/@antonvargov/why-a-lighting-studio-exports-ifc4-before-you-place-an-order-2013146ae2f9).

## Bias, risks and limitations

- **Single-brand, promotional register.** This is a brand's own catalog. The copy is
  written to present the work favourably. It is a reliable source of *facts about these
  objects* and an unreliable source of *neutral evaluation* of them. Models trained or
  grounded on it should not treat its tone as neutral description.
- **Not a market sample.** 605 objects from one studio in one country. It says nothing
  about lighting design in general and should not be used to estimate distributions of
  styles, categories or prices in the market.
- **Language coverage is even but not equal in origin.** Russian and English are the
  editorial originals; the other six languages are the studio's own localisations of them.
  The Chinese subset is an AI translation without native editorial review (see above).
- **Live URLs.** Catalog links, image links and 3D-model links point at live sites and will
  drift over time. The dataset is a snapshot; the site remains canonical.
- **Personal data.** The dataset names one public figure — the studio's founder — in a
  professional capacity, and contains the studio's public business contacts. It contains no
  customer data.

## Licensing

The dataset files are released under **CC BY 4.0**. Attribute as *Vargov® Design* with a
link to https://vargov.ru.

The **photographs are not included in this dataset** — only their URLs are. The images
remain the copyright of Vargov® Design and are not licensed under CC BY 4.0 by this
release. A separate set of press photographs is cleared for editorial use with attribution:
see https://github.com/vargov3-spec/vargov-ai-kb/blob/main/press/README.md.

*Vargov*® is a registered trademark. The licence covers reuse of the data, not use of the
mark.

## Citation

```bibtex
@misc{vargov_design_catalog,
  title        = {Vargov Design Catalog: 605 lighting and decorative compositions in 8 languages},
  author       = {{Vargov Design}},
  year         = {2026},
  howpublished = {Hugging Face Datasets},
  url          = {https://huggingface.co/datasets/vargov-design/vargov-design-catalog},
  note         = {CC BY 4.0}
}
```

## Contact

info@vargov.ru · https://vargov.ru/en
