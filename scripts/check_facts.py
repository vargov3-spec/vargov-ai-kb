#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сторож фактов бренда: тексты базы знаний против references/brand-facts.json.

ЗАЧЕМ. Сверка 26.10.2026 нашла ~25 расхождений, и все одного класса: число или
слово рядом с числом вписано руками в десяток файлов и в трёх языках, а правится
в одном. «604 из 605» при 603, «три поздравления» при четырёх, «на каждую нить»
при «на отверстие», путь к кнопке FBX, исправленный в RU и EN и забытый в zh.
Прежние сторожа были зелёными на строках с ошибкой: якорь ловил число 26, а слово
«три» на той же строке не видел (check_award_count.py, README:53).

КАК. Факты — в references/brand-facts.json, у каждого источник и дата проверки.
Здесь — ЯКОРЯ: регулярные выражения, которые ловят фразу целиком (число И слово
рядом) по каждому файлу и языку. Якорь обязан найтись: если текст переписали и
якорь пропал, сторож не молчит, а говорит «не смог определить» — это отдельная
строка и тоже код выхода 1, но другая причина, чем «расходится».

Сверяются также структурные факты в JSON (число наград и sameAs в
organization.jsonld, узлы catalog.jsonld, счётчики products.json, реестр
3ddd-models.json) и ЗАПРЕЩЁННЫЕ фразы — прежние неверные формулировки, которые
не должны вернуться пересборкой или копированием.

Файлы вне репозитория (handoff/, конфигуратор) — необязательные: если их нет на
этой машине, якорь пропускается с пометкой, а не падает (в GitHub Actions их нет).

ЖИВЫЕ ЯКОРЯ — только с ключом --live, по одному запросу на источник:
  https://vargov.ru/llms.txt?qa=1  — число наград, 605, 360, слово FBX;
  raw README датасета на Hugging Face — 26, 605, путь к кнопке FBX, крепления.
Расхождение там не чинится в базе — оно передаётся агенту сайта или владельцу
(карточку HF правит он через веб).

Вывод: по строке на находку —
  РАСХОДИТСЯ: <файл>:<строка> — <факт> — ожидалось «…» — найдено «…»
  НЕ СМОГ ОПРЕДЕЛИТЬ: <файл> — <факт> — якорь не найден: <шаблон>
и итог. Код выхода 1 при любой из них.

Запуск: python scripts/check_facts.py [--live]
Из build_pages.py: check_facts.run(live=False) -> (расхождения, не определено).
"""
from __future__ import annotations

import argparse
import json
import hashlib
import re
import sys
import urllib.request
from pathlib import Path

KB = Path(__file__).resolve().parent.parent
FACTS_PATH = KB / "references" / "brand-facts.json"

# Файлы вне репозитория: отсутствие — не ошибка, а пометка.
OPTIONAL_FILES = {
    "handoff/novoe-na-saite-s-2026-10-01.md",
}
CONFIGURATOR = Path(r"V:/защита контента/configurator")

MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]


def iso_ru(s: str) -> str:
    y, m, d = s.split("-")
    return f"{d}.{m}.{y}"


def iso_en(s: str) -> str:
    y, m, d = s.split("-")
    return f"{int(d)} {MONTHS_EN[int(m) - 1]} {y}"


def iso_zh(s: str) -> tuple[str, str, str]:
    y, m, d = s.split("-")
    return (y, str(int(m)), str(int(d)))


def norm(s) -> str:
    """Сравнение без пробелов, запятых-разделителей и регистра: «1 795 801» = «1795801», «2,700» = «2700»."""
    return re.sub(r"[\s,\u00a0]+", "", str(s)).lower()


def load_facts() -> dict:
    data = json.loads(FACTS_PATH.read_text(encoding="utf-8"))
    return data["facts"]


def anchors(F: dict) -> list[tuple[str, str, str, tuple]]:
    """(файл, факт, шаблон с группами, ожидаемые значения групп)."""
    v = lambda k: F[k]["value"]
    fam = v("families")
    n_aw, n_pr = str(v("awards_total")), str(v("awards_programmes"))
    total, calc, scheme = str(v("catalogue_total")), str(v("open_with_calc")), str(v("mounting_scheme"))
    n_rib, n_fr = str(len(v("ribbons"))), str(len(v("frame")))
    scene = v("fixed_scenes")[0]
    reg, linked = str(v("models3d_registry_entries")), str(v("models3d_linked"))
    no_model = F["models3d_linked"]["without"]
    cert = v("certification")
    tm, TM = v("trademark"), F["trademark"]
    fbx, fix, fr = v("fbx_button_path"), v("fbx_fixings"), v("frame_hang")
    ifc = v("ifc_class")
    ceil = str(v("ceiling_default_mm"))
    comm = F["commendations"]
    codes = v("catalogue_codes")
    langs = [l for l in v("languages_site") if l != "ru"]
    A: list[tuple[str, str, str, tuple]] = []

    # ---------------------------------------------------------------- llms.txt (RU)
    f = "llms.txt"
    A += [
        (f, "awards_total — строка 5 по правилу pr-kit", r"(\d+) достижений на международных премиях", (n_aw,)),
        (f, "catalogue_total + коды", r"Каталог — (\d+) композиций с артикулами (LC\d{4})…(LC\d{4})", (total, codes["first"], codes["last"])),
        (f, "awards_total + awards_programmes", r"Награды — (\d+), в (\d+) программах", (n_aw, n_pr)),
        (f, "awards_total — ссылка на awards-verified", r"awards-verified\.md\) — (\d+) наград со ссылками", (n_aw,)),
        (f, "families.lighting", r"Световые композиции\]\([^)]+\) — (\d+) позици", (str(fam["lighting"]),)),
        (f, "families.decorative", r"Декоративные композиции\]\([^)]+\) — (\d+) позици", (str(fam["decorative"]),)),
        (f, "families.sculptural-decor", r"Скульптурные композиции и декор\]\([^)]+\) — (\d+) позици", (str(fam["sculptural-decor"]),)),
        (f, "families.floor-table-lamps", r"Торшеры, бра, настольные арт-объекты\]\([^)]+\) — (\d+) позици", (str(fam["floor-table-lamps"]),)),
        (f, "models3d_registry_entries / models3d_linked / catalogue_total", r"\((\d+) записи — по одной на каждую композицию со ссылкой: (\d+) из (\d+) композиций каталога, без моделей только (LC\d{4}) и (LC\d{4})\)", (reg, linked, total, no_model[0], no_model[1])),
        (f, "Store в описании графа", r"граф schema\.org: Organization, Person, (Store) \(шоурум\)", ("Store",)),
        (f, "датасет Hugging Face упомянут", r"Датасет на (Hugging Face): \[vargov-design/vargov-design-catalog\]", ("Hugging Face",)),
        (f, "brand-facts.json упомянут", r"\[references/(brand-facts\.json)\]", ("brand-facts.json",)),
        (f, "certification 004/020", r"ТР ТС 004/2011 на (\d+) артикулов LC, из них (\d+) — также по ТР ТС 020/2011", (str(cert["tr_cu_004"]), str(cert["tr_cu_020"]))),
        (f, "certification 037", r"ТР ЕАЭС 037/2016 на те же (\d+) артикулов", (str(cert["tr_eaeu_037"]),)),
        (f, "certification срок", r"знак EAC, действуют до (\d{4}) года", (str(cert["valid_until_year"]),)),
        (f, "trademark RU", r"Россия, свидетельство № (\d+) \(до (\d\d\.\d\d\.\d{4})\)", (str(tm["ru_no"]), iso_ru(TM["ru_until"]))),
        (f, "trademark IR", r"Мадридской системе № ([\d ]+) с охраной в Китае \(до (\d\d\.\d\d\.\d{4})\), класс (\d+)", (str(tm["ir_no"]), iso_ru(TM["ir_china_until"]), str(tm["ir_class"]))),
        (f, "trademark логотип", r"Логотип VARGOV® DESIGN: Россия, свидетельство № (\d+) \(приоритет (\d\d\.\d\d\.\d{4}), зарегистрирован (\d\d\.\d\d\.\d{4}), действует до (\d\d\.\d\d\.\d{4})\)", (str(tm["logo_ru_no"]), iso_ru(TM["logo_priority"]), iso_ru(TM["logo_registered"]), iso_ru(TM["logo_until"]))),
        (f, "open_with_calc", r"Полный расчёт и выгрузка — у (\d+) композиций из (\d+)", (calc, total)),
        (f, "ceiling_default_mm", r"по умолчанию (\d+) мм — высота помещения", (ceil,)),
        (f, "fbx_button_path", r"в том же ящике «([^»]+)» шага «([^»]+)», сразу под «([^»]+)» — стоит кнопка «([^»]+)»", (fbx["drawer_ru"], fbx["step_ru"], fbx["under_ru"], fbx["button_ru"])),
        (f, "fbx_fixings — класс «на нить / на отверстие»", r"потолочные крепления отдельными объектами \((одно крепление на каждое отверстие|крепление на каждую нить)", (fix["ru"],)),
        (f, "mounting_scheme", r"Монтажная схема 1:1 есть у (\d+) из этих (\d+) композиций", (scheme, calc)),
        (f, "ribbons — число лент без схемы", r"её нет у (\d+) лент", (n_rib,)),
        (f, "frame — число и формулировка подвеса", r"у (\d+) композиций на каркасе \((у элементов своих нитей к потолку нет|элементы висят на каркасе, нитей к потолку ноль)", (n_fr, fr["ru"])),
        (f, "fixed_scenes — настенное бра", r"готовой сцены (LC\d{4}(?:-\d)?) — это настенное бра", (scene,)),
        (f, "ifc_class — по элементу", r"Класс решается по (элементу), а не по артикулу", ("элементу",)),
        (f, "ifc_class — исключение", r"известное исключение — (LC\d{4})", (ifc["exception"],)),
        (f, "EPDA 2026 в перечне «Среди них»", r"Winner — European Product Design Award 2026 \((LC\d{4}-\d)\)", ("LC0543-2",)),
        (f, "languages_site — семь языков кроме русского", r"English — \[(/en)\].*?Deutsch — \[(/de)\].*?Italiano — \[(/it)\].*?Français — \[(/fr)\].*?Español — \[(/es)\].*?Tiếng Việt — \[(/vi)\].*?العربية — \[(/ar)\]", tuple("/" + l for l in langs)),
        (f, "languages_kb_only — китайский только в базе", r"中文 \((только база знаний)\)", ("только база знаний",)),
    ]
    # ---------------------------------------------------------------- en/llms.txt
    f = "en/llms.txt"
    A += [
        (f, "awards_total — line 5", r"(\d+) awards from international juries\.", (n_aw,)),
        (f, "catalogue_total + codes", r"holds (\d+) compositions with LC article codes \((LC\d{4})…(LC\d{4})\)", (total, codes["first"], codes["last"])),
        (f, "awards_total + programmes", r"(\d+) awards across (\d+) programmes", (n_aw, n_pr)),
        (f, "awards_total — awards-verified link", r"awards-verified\.md\) — (\d+) awards with links", (n_aw,)),
        (f, "families.lighting", r"Lighting compositions\]\([^)]+\) — (\d+) items", (str(fam["lighting"]),)),
        (f, "families.decorative", r"Decorative compositions\]\([^)]+\) — (\d+) items", (str(fam["decorative"]),)),
        (f, "families.sculptural-decor", r"Sculptural compositions & décor\]\([^)]+\) — (\d+) items", (str(fam["sculptural-decor"]),)),
        (f, "families.floor-table-lamps", r"Floor lamps, sconces, table art objects\]\([^)]+\) — (\d+) items", (str(fam["floor-table-lamps"]),)),
        (f, "models3d registry / linked / total", r"\((\d+) entries — one for each composition that carries a link: (\d+) of the (\d+) in the catalogue; only (LC\d{4}) and (LC\d{4}) have no model\)", (reg, linked, total, no_model[0], no_model[1])),
        (f, "Store in the graph description", r"Organization, Person, (Store) \(the showroom\)", ("Store",)),
        (f, "Hugging Face dataset mentioned", r"(Hugging Face) dataset: \[vargov-design/vargov-design-catalog\]", ("Hugging Face",)),
        (f, "brand-facts.json mentioned", r"\[references/(brand-facts\.json)\]", ("brand-facts.json",)),
        (f, "certification 004/020", r"TR CU 004/2011 covering (\d+) LC articles, (\d+) of them also to TR CU 020/2011", (str(cert["tr_cu_004"]), str(cert["tr_cu_020"]))),
        (f, "certification 037", r"037/2016 declarations covering the same (\d+) articles", (str(cert["tr_eaeu_037"]),)),
        (f, "certification validity", r"EAC mark, valid until (\d{4})", (str(cert["valid_until_year"]),)),
        (f, "trademark RU", r"Russia, registration No\. (\d+) \(to (\d+ \w+ \d{4})\)", (str(tm["ru_no"]), iso_en(TM["ru_until"]))),
        (f, "trademark IR", r"Madrid System No\. ([\d ]+) with protection in China \(to (\d+ \w+ \d{4})\), class (\d+)", (str(tm["ir_no"]), iso_en(TM["ir_china_until"]), str(tm["ir_class"]))),
        (f, "trademark logo", r"logo: Russia, registration No\. (\d+) \(priority (\d+ \w+ \d{4}), registered (\d+ \w+ \d{4}), in force until (\d+ \w+ \d{4})\)", (str(tm["logo_ru_no"]), iso_en(TM["logo_priority"]), iso_en(TM["logo_registered"]), iso_en(TM["logo_until"]))),
        (f, "open_with_calc", r"export are available for (\d+) of (\d+) compositions", (calc, total)),
        (f, "ceiling_default_mm", r"default ([\d,]+) mm — the room height", (ceil,)),
        (f, "fbx_button_path", r'the same "([^"]+)" drawer of the "([^"]+)" step, right under "([^"]+)", also carries a "([^"]+)" button', (fbx["drawer_en"], fbx["step_en"], fbx["under_en"], fbx["button_en"])),
        (f, "fbx_fixings — strand / hole class", r"the ceiling fixings as separate objects \((one per ceiling hole|one per strand)", (fix["en"],)),
        (f, "mounting_scheme", r"The 1:1 drawing exists for (\d+) of those (\d+) compositions", (scheme, calc)),
        (f, "ribbons", r"it is absent for (\d+) ribbons", (n_rib,)),
        (f, "frame — count and wording", r"for (\d+) compositions on a frame \((the elements have no strands of their own|the elements hang from the frame, with zero strands)", (n_fr, fr["en"])),
        (f, "fixed_scenes — wall light", r"the ready scene (LC\d{4}(?:-\d)?) — a wall light", (scene,)),
        (f, "ifc_class — per element", r"The class is decided per (element), not per article", ("element",)),
        (f, "ifc_class — exception", r"known exception — (LC\d{4})", (ifc["exception"],)),
        (f, "EPDA 2026 in 'Among them'", r"Winner — European Product Design Award 2026 \((LC\d{4}-\d)\)", ("LC0543-2",)),
        (f, "languages_site", r"English — \[(/en)\].*?Deutsch — \[(/de)\].*?Italiano — \[(/it)\].*?Français — \[(/fr)\].*?Español — \[(/es)\].*?Tiếng Việt — \[(/vi)\].*?العربية — \[(/ar)\]", tuple("/" + l for l in langs)),
        (f, "languages_kb_only", r"中文 \((knowledge base only)\)", ("knowledge base only",)),
    ]
    # ---------------------------------------------------------------- zh/llms.txt
    f = "zh/llms.txt"
    zh_ir = iso_zh(TM["ir_china_until"])
    zh_lp, zh_lr, zh_lu = iso_zh(TM["logo_priority"]), iso_zh(TM["logo_registered"]), iso_zh(TM["logo_until"])
    A += [
        (f, "awards_total — 第 5 行", r"(\d+) 项国际评委会奖项", (n_aw,)),
        (f, "catalogue_total + 货号", r"目录收录 (\d+) 件构成，货号 (LC\d{4})…(LC\d{4})", (total, codes["first"], codes["last"])),
        (f, "awards_programmes + awards_total", r"(\d+) 个奖项计划共 (\d+) 项奖项", (n_pr, n_aw)),
        (f, "awards_total — awards-verified", r"awards-verified\.md\) — (\d+) 项奖项", (n_aw,)),
        (f, "families.lighting", r"灯光构成\]\([^)]+\) — (\d+) 件", (str(fam["lighting"]),)),
        (f, "families.decorative", r"装饰构成\]\([^)]+\) — (\d+) 件", (str(fam["decorative"]),)),
        (f, "families.sculptural-decor", r"雕塑构成与装饰\]\([^)]+\) — (\d+) 件", (str(fam["sculptural-decor"]),)),
        (f, "families.floor-table-lamps", r"落地灯、壁灯与桌面艺术品\]\([^)]+\) — (\d+) 件", (str(fam["floor-table-lamps"]),)),
        (f, "models3d registry / total / linked", r"（(\d+) 条——每件带链接的构成一条：(\d+) 件构成中 (\d+) 件带链接；仅 (LC\d{4}) 与 (LC\d{4}) 没有模型）", (reg, total, linked, no_model[0], no_model[1])),
        (f, "Store 节点", r"Organization、Person、(Store)（展厅）", ("Store",)),
        (f, "Hugging Face 数据集", r"(Hugging Face) 数据集：\[vargov-design/vargov-design-catalog\]", ("Hugging Face",)),
        (f, "brand-facts.json", r"\[references/(brand-facts\.json)\]", ("brand-facts.json",)),
        (f, "certification 004/020", r"系列证书覆盖 (\d+) 个 LC 货号，其中 (\d+) 个同时通过 TR CU 020/2011", (str(cert["tr_cu_004"]), str(cert["tr_cu_020"]))),
        (f, "certification 037", r"037/2016 声明覆盖同样的 (\d+) 个货号", (str(cert["tr_eaeu_037"]),)),
        (f, "certification 有效期", r"EAC 标志，有效至 (\d{4}) 年", (str(cert["valid_until_year"]),)),
        (f, "trademark RU + IR", r"俄罗斯注册号 (\d+)；马德里体系国际注册号 ([\d ]+)，在中国受保护（至 (\d{4}) 年 (\d+) 月 (\d+) 日），第 (\d+) 类", (str(tm["ru_no"]), str(tm["ir_no"]), zh_ir[0], zh_ir[1], zh_ir[2], str(tm["ir_class"]))),
        (f, "trademark 标志", r"标志 VARGOV® DESIGN，俄罗斯注册号 (\d+)（优先权日 (\d{4}) 年 (\d+) 月 (\d+) 日，注册日 (\d{4}) 年 (\d+) 月 (\d+) 日，有效期至 (\d{4}) 年 (\d+) 月 (\d+) 日）", (str(tm["logo_ru_no"]), *zh_lp, *zh_lr, *zh_lu)),
        (f, "open_with_calc", r"(\d+) 件构成中有 (\d+) 件可完整计算并导出", (total, calc)),
        (f, "ceiling_default_mm", r"默认 (\d+) 毫米", (ceil,)),
        (f, "fbx_button_path", r"在“([^”]+)”（[^）]*）步骤的“([^”]+)”（[^）]*）抽屉内，紧邻“([^”]+)”下方设有“([^”]+)”按钮", (fbx["step_zh"], fbx["drawer_zh"], fbx["under_en"], fbx["button_en"])),
        (f, "fbx_fixings — 吊线 / 孔", r"吊顶固定件为独立对象（(每个吊顶孔一个|每根吊线一个)", (fix["zh"],)),
        (f, "mounting_scheme", r"在这 (\d+) 件中，有 (\d+) 件可获得 1:1 放样图", (calc, scheme)),
        (f, "ribbons", r"(\d+) 件灯带没有", (n_rib,)),
        (f, "frame — 数量与表述", r"(\d+) 件骨架式构成没有（(元件自身没有通向吊顶的吊线|元件悬挂于骨架，通向吊顶的吊线为零)", (n_fr, fr["zh"])),
        (f, "fixed_scenes — 壁灯", r"成品场景 (LC\d{4}(?:-\d)?) 也没有 —— 它是壁灯", (scene,)),
        (f, "ifc_class — 按元件", r"类别按(元件)而非货号判定", ("元件",)),
        (f, "ifc_class — 例外", r"已知例外 (LC\d{4})", (ifc["exception"],)),
        (f, "EPDA 2026", r"Winner — European Product Design Award 2026（(LC\d{4}-\d)）", ("LC0543-2",)),
    ]
    # ---------------------------------------------------------------- llms-full.txt (RU + EN дословно)
    f = "llms-full.txt"
    A += [
        (f, "awards_total RU", r"(\d+) достижений на международных премиях", (n_aw,)),
        (f, "awards_total EN", r"(\d+) awards from international juries\.", (n_aw,)),
        (f, "models3d registry RU", r"\((\d+) записи — по одной на каждую композицию со ссылкой: (\d+) из (\d+)", (reg, linked, total)),
        (f, "models3d registry EN", r"\((\d+) entries — one for each composition that carries a link: (\d+) of the (\d+)", (reg, linked, total)),
        (f, "fbx_button_path RU", r"в том же ящике «([^»]+)» шага «([^»]+)»", (fbx["drawer_ru"], fbx["step_ru"])),
        (f, "fbx_button_path EN", r'the same "([^"]+)" drawer of the "([^"]+)" step', (fbx["drawer_en"], fbx["step_en"])),
        (f, "fbx_fixings RU", r"потолочные крепления отдельными объектами \((одно крепление на каждое отверстие|крепление на каждую нить)", (fix["ru"],)),
        (f, "fbx_fixings EN", r"the ceiling fixings as separate objects \((one per ceiling hole|one per strand)", (fix["en"],)),
        (f, "Store RU", r"граф schema\.org: Organization, Person, (Store)", ("Store",)),
        (f, "Store EN", r"Organization, Person, (Store) \(the showroom\)", ("Store",)),
        (f, "certification RU", r"ТР ТС 004/2011 на (\d+) артикулов LC, из них (\d+) — также по ТР ТС 020/2011", (str(cert["tr_cu_004"]), str(cert["tr_cu_020"]))),
        (f, "certification EN", r"TR CU 004/2011 covering (\d+) LC articles, (\d+) of them also to TR CU 020/2011", (str(cert["tr_cu_004"]), str(cert["tr_cu_020"]))),
    ]
    # ---------------------------------------------------------------- README.md
    f = "README.md"
    A += [
        (f, "awards_total — описание графа", r"Organization \(бренд, (\d+) наград", (n_aw,)),
        (f, "awards_total — правила текстов", r"дословно из `awards\.ts`: (\d+) наград", (n_aw,)),
        (f, "commendations — слово «четыре/три»", r"(\S+) поздравления жюри в счёт не идут", (comm["word_ru"],)),
        (f, "commendations — файлов писем", r"\(записей четыре, файлов-писем (\S+)\)", ({3: "три", 4: "четыре"}.get(comm["files"], str(comm["files"])),)),
        (f, "catalogue_total — datasets", r"\| `datasets/`, `en/datasets/` \| (\d+) композиций", (total,)),
        (f, "Store в описании графа", r"Person \(основатель\), (Store) \(шоурум\)", ("Store",)),
        (f, "brand-facts.json назван источником", r"Источник фактов — `references/(brand-facts\.json)`", ("brand-facts.json",)),
    ]
    # ---------------------------------------------------------------- knowledge/brand.md
    f = "knowledge/brand.md"
    A += [
        (f, "awards_total — заголовок", r"^## Награды — (\d+)", (n_aw,)),
        (f, "awards_total — awardsCount", r"`awardsCount\(\)` = (\d+);", (n_aw,)),
        (f, "commendations", r"(\S+) «Официальных поздравления жюри»", (comm["word_ru"],)),
        (f, "awards_programmes", r"пересчитано сборщиком `build_from_site\.py` [\d.]+: (\d+) программ, (\d+) записей", (n_pr, str(v("awards_total") + v("commendations")))),
        (f, "models3d_registry_entries", r"`references/3ddd-models\.json` \((\d+) записи", (reg,)),
        (f, "models3d_linked — арифметика", r"минус два без слага \((LC\d{4}), (LC\d{4})\) — это \*\*(\d+) композиции с узлом `3DModel`\*\*", (no_model[0], no_model[1], linked)),
        (f, "models3d_graph_nodes", r"самих узлов `3DModel` в графе (\d+)", (str(v("models3d_graph_nodes")),)),
        (f, "models3d_linked + collection_pages — счёт", r"\*\*(\d+) прямые карточки\*\* и (\d+) списка на (\d+) артикулов", (linked, str(v("collection_pages")), total)),
        (f, "collection_pages — не снят ни у кого", r"узлов `CollectionPage` (\d+), снят ни у кого", (str(v("collection_pages")),)),
        (f, "trademark RU", r"Товарный знак \*\*VARGOV\*\*, регистрационный № (\d+)\.", (str(tm["ru_no"]),)),
        (f, "trademark IR", r"Мадридской системе № ([\d ]+)\. Дата регистрации: (\d\d\.\d\d\.\d{4})\. Действует до (\d\d\.\d\d\.\d{4})\.", (str(tm["ir_no"]), iso_ru(TM["ir_registered"]), iso_ru(TM["ir_china_until"]))),
    ]
    # ---------------------------------------------------------------- knowledge/awards-verified.md
    f = "knowledge/awards-verified.md"
    A += [
        (f, "awards_total — awardsCount", r"`awardsCount\(\)` = \*\*(\d+)\*\*", (n_aw,)),
        (f, "awards_total — заголовок", r"^## (\d+) наград", (n_aw,)),
        (f, "awards_total + commendations — правила владельца", r"- наград \*\*(\d+)\*\*; (\S+) «Официальных поздравления жюри»", (n_aw, comm["word_ru"])),
        (f, "awards_total — итого по уровням", r"Итого (\d+)\.", (n_aw,)),
        (f, "awards_total + awarded_skus — правило пары", r"премий (\d+), артикулов с\s+наградой (\d+)\.", (n_aw, str(v("awarded_skus")))),
        (f, "awarded_skus — индекс", r"— \*\*(\d+) артикула\*\*\. Сверка", (str(v("awarded_skus")),)),
        (f, "awarded_skus — счёт индекса", r"^Счёт: .*= \*\*(\d+)\*\*\.", (str(v("awarded_skus")),)),
        (f, "commendations — заголовок раздела", r"^## (\S+) документа, которые в счёт не идут", (comm["word_ru"],)),
        (f, "awards_total — дата счёта", r"\*\*на \d\d\.\d\d\.\d{4} это (\d+)\*\*", (n_aw,)),
    ]
    # ---------------------------------------------------------------- knowledge/pr-kit.md
    f = "knowledge/pr-kit.md"
    A += [
        (f, "awards_total + programmes — источник", r"Источник — `awards\.ts` сайта, (\d+) наград в (\d+) программах", (n_aw, n_pr)),
        (f, "awards_total — заголовок", r"## Число наград: (\d+),", (n_aw,)),
        (f, "awards_total — boilerplate", r"- Награды: (\d+) достижений", (n_aw,)),
        (f, "awards_total — правило формулировки RU", r"RU:\s+(\d+) достижений на международных премиях", (n_aw,)),
        (f, "awards_total — правило формулировки EN", r"EN:\s+(\d+) awards from international juries", (n_aw,)),
    ]
    # ---------------------------------------------------------------- knowledge/whats-new-2026-10.md
    f = "knowledge/whats-new-2026-10.md"
    A += [
        (f, "open_with_calc RU", r"Полный расчёт — у (\d+) композиций из (\d+)", (calc, total)),
        (f, "open_with_calc EN", r"Full calculation: (\d+) of (\d+) compositions", (calc, total)),
        (f, "mounting_scheme RU", r"Схема есть у (\d+) из (\d+) композиций", (scheme, calc)),
        (f, "mounting_scheme EN", r"drawing exists for (\d+) of the (\d+) compositions", (scheme, calc)),
        (f, "ribbons RU", r"её нет у (\d+) лент", (n_rib,)),
        (f, "ribbons EN", r"(\d+) ribbons have none", (n_rib,)),
        (f, "frame RU", r"у (\d+) композиций\s+на каркасе \((у элементов своих нитей к потолку нет|элементы висят на каркасе, нитей к потолку ноль)", (n_fr, fr["ru"])),
        (f, "frame EN", r"nor do (\d+) compositions on a\s+frame \((their elements have no strands of their own|their elements hang from the frame, with zero strands)", (n_fr, fr["en_whats_new"])),
        (f, "fixed_scenes RU", r"у готовой сцены (LC\d{4}(?:-\d)?) — это настенное", (scene,)),
        (f, "ceiling_default_mm RU", r"по умолчанию (\d+) мм — это высота потолка", (ceil,)),
        (f, "ceiling_default_mm EN", r"default ([\d,]+) mm — the ceiling height", (ceil,)),
        (f, "awards_total RU", r"Всего наград (\d+)\.", (n_aw,)),
        (f, "awards_total EN", r"(\d+) awards in total", (n_aw,)),
        (f, "fbx_fixings RU", r"креплениями \((одно крепление на\s+каждое отверстие|крепление на каждую нить)", (fix["ru"],)),
        (f, "fbx_fixings EN", r"the fixings \((one per\s+ceiling hole|one per strand)", (fix["en"],)),
        (f, "open_with_calc — круг FBX RU", r"Круг тот же, что у выгрузки IFC4: (\d+) композиций из (\d+)", (calc, total)),
        (f, "open_with_calc — FBX scope EN", r"The scope is the same as for the IFC4 export: (\d+) compositions out of (\d+)", (calc, total)),
    ]
    # ---------------------------------------------------------------- knowledge/award-profiles-fix-2026-09.md
    f = "knowledge/award-profiles-fix-2026-09.md"
    A += [
        (f, "awards_total — bio для кабинетов", r"full project support\. (\d+) awards from international juries", (n_aw,)),
        (f, "awards_total — короткое bio", r"Anton Vargov\. (\d+) awards from international", (n_aw,)),
    ]
    # ---------------------------------------------------------------- datasets/hf-README.md
    f = "datasets/hf-README.md"
    A += [
        (f, "catalogue_total + languages — заголовок и bibtex", r"(\d+) lighting and decorative compositions in (\d+) languages", (total, str(len(v("languages_site"))))),
        (f, "families", r"`lighting` \((\d+)\), `decorative` \((\d+)\), `sculptural-decor` \((\d+)\), `floor-table-lamps` \((\d+)\)", (str(fam["lighting"]), str(fam["decorative"]), str(fam["sculptural-decor"]), str(fam["floor-table-lamps"]))),
        (f, "models3d_linked", r"3dsky\.org\. Present for (\d+) of (\d+) records", (linked, total)),
        (f, "awarded_skus + awards_total", r"True for (\d+) records: (\d+) awards", (str(v("awarded_skus")), n_aw)),
        (f, "certification — записей с cert", r"`cert` \|[^\n]*Present for (\d+) records", (str(cert["tr_cu_004"]),)),
        (f, "awards_total — абзац о бренде", r"holds \*\*(\d+) design\s+awards\*\*", (n_aw,)),
        (f, "trademark RU", r"registered in Russia \(№ (\d+), \d+ \w+ (\d{4})\)", (str(tm["ru_no"]), str(tm["ru_registered_year"]))),
        (f, "trademark IR", r"Madrid System \(№ (\d+), (\d+ \w+ \d{4})\), class (\d+)", (str(tm["ir_no"]), iso_en(TM["ir_registered"]), str(tm["ir_class"]))),
        (f, "trademark logo", r"logo is registered separately in Russia \(№ (\d+), registered (\d+ \w+ \d{4}),\s+in force until (\d+ \w+ \d{4})\)", (str(tm["logo_ru_no"]), iso_en(TM["logo_registered"]), iso_en(TM["logo_until"]))),
        (f, "open_with_calc", r"For the (\d+) compositions that open with a full calculation", (calc,)),
        (f, "fbx_button_path", r'the "([^"]+)" drawer of the "([^"]+)" step, right under "([^"]+)"', (fbx["drawer_en"], fbx["step_en"], fbx["under_en"])),
        (f, "fbx_fixings", r"ceiling fixings as separate objects \((one per ceiling hole|one per strand)", (fix["en"],)),
        (f, "open_with_calc — FBX scope", r"Both exports cover the same (\d+)\s+of (\d+) compositions", (calc, total)),
    ]
    # ---------------------------------------------------------------- handoff (вне репозитория)
    f = "handoff/novoe-na-saite-s-2026-10-01.md"
    A += [
        (f, "awards_total + awarded_skus — раздел 52", r"### 52\. Страница /awards: «(\d+) наград» в шапке и все (\d+) награждённых артикула", (n_aw, str(v("awarded_skus")))),
        (f, "awards_total — дословная фраза /awards", r"Работы Vargov®Design отмечены (\d+) наградами", (n_aw,)),
        (f, "awards_total — витрины и FAQ", r"Работы бренда отмечены (\d+) международными премиями", (n_aw,)),
        (f, "awards_total — «у трёх из N»", r"У трёх из (\d+) наград бумаги нет", (n_aw,)),
    ]
    # ---------------------------------------------------------------- эссе IFC4 (дополнительно: класс «каркас / бра»)
    f = "knowledge/ifc4-in-the-model-essay.md"
    A += [
        (f, "границ в разделе «Где файл заканчивается» (RU)", r"^(\S+) границ, названных прямо", ("пять",)),
        (f, "limits in 'Where the file stops' (EN)", r"^(\S+) limits, stated plainly", ("five",)),
        (f, "open_with_calc RU", r"Полностью выгружаются (\d+) композиций из (\d+)", (calc, total)),
        (f, "fixed_scenes — настенное бра RU", r"Готовая сцена (LC\d{4}(?:-\d)?) — настенное бра", (scene,)),
        (f, "fixed_scenes — wall light EN", r"The ready-made scene (LC\d{4}(?:-\d)?) is a wall light", (scene,)),
    ]
    return A


def forbidden(F: dict) -> list[tuple[str, str, str]]:
    """(файл, запрещённая фраза, почему). Прежние неверные формулировки не должны вернуться."""
    fix, fr = F["fbx_fixings"]["forbidden"], F["frame_hang"]["forbidden"]
    reg_old = str(F["models3d_registry_entries"]["value"] + 1)
    out = []
    for f in ("llms.txt", "llms-full.txt", "knowledge/whats-new-2026-10.md", "knowledge/ifc4-in-the-model-essay.md"):
        out += [(f, fix["ru"], "FBX: одно крепление на отверстие, не на нить (View3D.tsx:3559-3563)"),
                (f, fr["ru"], "каркас подвешен к потолку тросами (frame.ts:1-4)"),
                (f, "крепить к потолку нечего", "каркас подвешен к потолку (frame.ts:1-4)")]
    for f in ("en/llms.txt", "llms-full.txt", "knowledge/whats-new-2026-10.md", "knowledge/ifc4-in-the-model-essay.md", "datasets/hf-README.md"):
        out += [(f, fix["en"], "FBX: one fixing per hole, not per strand"),
                (f, fr["en"], "the frame is suspended from the ceiling"),
                (f, "nothing to fix to the ceiling", "the frame is suspended from the ceiling")]
    out += [("zh/llms.txt", fix["zh"], "FBX：每孔一个固定件"),
            ("zh/llms.txt", fr["zh"], "骨架吊于吊顶"),
            ("zh/llms.txt", "Crystal Breakthrough", "конкурсное название владелец оставил вне публикации (awards-verified.md, строка 25 таблицы)"),
            ("zh/llms.txt", "价格与生产", "ящик «Документы» — в шаге «3D схема композиции» (коммит d3688d9)"),
            ("datasets/hf-README.md", "Price & production", "the Documents drawer is in the 3D composition scheme step (commit d3688d9)")]
    for f in ("llms.txt", "llms-full.txt", "knowledge/brand.md"):
        out.append((f, f"{reg_old} из {F['catalogue_total']['value']}", "реестр 3D: 603 записи после снятия фантома LC0104-1"))
    for f in ("en/llms.txt", "llms-full.txt"):
        out.append((f, f"{reg_old} of the {F['catalogue_total']['value']}", "3D registry: 603 entries"))
    out.append(("zh/llms.txt", f"{reg_old} 件带链接", "3D 登记：603 条"))
    out.append(("README.md", "три поздравления", "поздравлений четыре (awards-verified.md, раздел «Четыре документа»)"))
    return out


def structural(F: dict) -> list[tuple[str, str, str, str, str]]:
    """Проверки JSON: (вид, файл, факт, ожидалось, найдено). Вид — 'mismatch' | 'unknown'."""
    out = []
    v = lambda k: F[k]["value"]

    def jload(rel):
        return json.loads((KB / rel).read_text(encoding="utf-8"))

    def check(file, fact, exp, got):
        if norm(exp) != norm(got):
            out.append(("mismatch", file, fact, str(exp), str(got)))

    # organization.jsonld
    rel = "references/organization.jsonld"
    g = {n.get("@type"): n for n in jload(rel).get("@graph", [])}
    org, person = g.get("Organization") or {}, g.get("Person") or {}
    check(rel, "awards_total — Organization.award", v("awards_total"), len(org.get("award") or []))
    ids = {i.get("value") for i in org.get("identifier") or []}
    for key in ("ru_no", "ir_no"):
        if str(v("trademark")[key]) not in ids:
            out.append(("mismatch", rel, f"trademark.{key} в identifier", str(v("trademark")[key]), "нет"))
    for u in v("sameAs")["organization"]:
        if u not in (org.get("sameAs") or []):
            out.append(("mismatch", rel, "sameAs.organization", u, "нет в Organization.sameAs"))
    for u in v("sameAs")["person"]:
        if u not in (person.get("sameAs") or []):
            out.append(("mismatch", rel, "sameAs.person", u, "нет в Person.sameAs"))
    # catalog.jsonld
    rel = "references/catalog.jsonld"
    nodes = jload(rel).get("@graph", [])
    types = {}
    for n in nodes:
        types[n.get("@type")] = types.get(n.get("@type"), 0) + 1
    check(rel, "catalogue_total — узлов Product", v("catalogue_total"), types.get("Product", 0))
    check(rel, "Store — узел шоурума", 1, types.get("Store", 0))
    org_c = next((n for n in nodes if n.get("@type") == "Organization"), {})
    check(rel, "awards_total — Organization.award", v("awards_total"), len(org_c.get("award") or []))
    m3 = cp = with_model = awarded = 0
    for n in nodes:
        if n.get("@type") != "Product":
            continue
        so = n.get("subjectOf") or []
        so = [so] if isinstance(so, dict) else so
        k = sum(1 for x in so if x.get("@type") == "3DModel")
        m3 += k
        with_model += 1 if k else 0
        cp += sum(1 for x in so if x.get("@type") == "CollectionPage")
        awarded += 1 if n.get("award") else 0
    check(rel, "models3d_graph_nodes — узлов 3DModel", v("models3d_graph_nodes"), m3)
    check(rel, "models3d_linked — Product с 3DModel", v("models3d_linked"), with_model)
    check(rel, "collection_pages — узлов CollectionPage", v("collection_pages"), cp)
    check(rel, "awarded_skus — Product с award", v("awarded_skus"), awarded)
    # products.json
    rel = "datasets/products.json"
    P = jload(rel)
    check(rel, "catalogue_total — записей", v("catalogue_total"), len(P))
    codes = sorted(p["code"] for p in P)
    check(rel, "catalogue_codes.first", v("catalogue_codes")["first"], codes[0])
    check(rel, "catalogue_codes.last", v("catalogue_codes")["last"], codes[-1])
    fam = {}
    labels_ru, labels_en = {}, {}
    for p in P:
        fam[p.get("category")] = fam.get(p.get("category"), 0) + 1
        lab = p.get("category_label") or {}
        labels_ru.setdefault(p.get("category"), lab.get("ru"))
        labels_en.setdefault(p.get("category"), lab.get("en"))
    for k, n in v("families").items():
        check(rel, f"families.{k}", n, fam.get(k, 0))
        check(rel, f"families.labels_ru.{k}", F["families"]["labels_ru"][k], labels_ru.get(k))
        check(rel, f"families.labels_en.{k}", F["families"]["labels_en"][k], labels_en.get(k))
    check(rel, "awarded_skus — award_winning", v("awarded_skus"), sum(1 for p in P if p.get("award_winning")))
    check(rel, "models3d_linked — model3d непуст", v("models3d_linked"), sum(1 for p in P if p.get("model3d")))
    check(rel, "models3d_linked.without", sorted(F["models3d_linked"]["without"]), sorted(p["code"] for p in P if not p.get("model3d")))
    cert = [p for p in P if p.get("cert")]
    regs = {"004/2011": 0, "020/2011": 0, "037/2016": 0}
    for p in cert:
        s = json.dumps(p["cert"], ensure_ascii=False)
        for r in regs:
            regs[r] += 1 if r in s else 0
    c = v("certification")
    check(rel, "certification.tr_cu_004", c["tr_cu_004"], regs["004/2011"])
    check(rel, "certification.tr_cu_020", c["tr_cu_020"], regs["020/2011"])
    check(rel, "certification.tr_eaeu_037", c["tr_eaeu_037"], regs["037/2016"])
    check(rel, "certification — записей с cert", c["tr_cu_004"], len(cert))
    years = {str(p["cert"].get("untilIso", ""))[:4] for p in cert}
    check(rel, "certification.valid_until_year", {str(c["valid_until_year"])}, years)
    langs = set()
    for p in P[:5]:
        langs |= set((p.get("description") or {}).keys())
    check(rel, "languages_site — ключи i18n", sorted(v("languages_site")), sorted(langs))
    # 3ddd-models.json
    rel = "references/3ddd-models.json"
    items = jload(rel)["items"]
    check(rel, "models3d_registry_entries — len(items)", v("models3d_registry_entries"), len(items))
    extra = sorted(set(items) - set(codes))
    check(rel, "записей вне каталога (фантомы вроде LC0104-1)", [], extra)
    # конфигуратор — только если он есть на этой машине
    osk = CONFIGURATOR / "public" / "open-skus.json"
    if osk.is_file():
        o = json.loads(osk.read_text(encoding="utf-8"))
        rel = "configurator/public/open-skus.json"
        check(rel, "open_with_calc — count", v("open_with_calc"), o.get("count"))
        check(rel, "open_with_calc — len(skus)", v("open_with_calc"), len(set(o.get("skus") or [])))
        check(rel, "frame — frames", sorted(v("frame")), sorted(o.get("frames") or []))
        rib = sorted(k for k, s in (o.get("series") or {}).items() if isinstance(s, dict) and s.get("ribbon"))
        check(rel, "ribbons — series.ribbon", sorted(v("ribbons")), rib)
        check(rel, "mounting_scheme = count − ленты − каркасные − сцены",
              v("mounting_scheme"), (o.get("count") or 0) - len(rib) - len(o.get("frames") or []) - len(v("fixed_scenes")))
    else:
        out.append(("skipped", "configurator/public/open-skus.json", "open_with_calc / ribbons / frame", "", "конфигуратора на этой машине нет — пропущено"))
    return out


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "vargov-ai-kb check_facts (one request per source)"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


def live(F: dict) -> list[tuple[str, str, str, str, str]]:
    """Живые якоря: (вид, источник, факт, ожидалось, найдено). По одному запросу на источник."""
    out = []
    v = lambda k: F[k]["value"]
    n_aw, total, calc = str(v("awards_total")), str(v("catalogue_total")), str(v("open_with_calc"))
    fbx, fix = v("fbx_button_path"), v("fbx_fixings")
    srcs = v("live_sources")

    def grab(label, url):
        try:
            return fetch(url)
        except Exception as e:  # noqa: BLE001 — сеть, любая причина
            out.append(("unknown", label, "сеть", "", f"запрос не удался: {e}"))
            return None

    # 1) vargov.ru/llms.txt — канонический источник сайта (с ?qa=1, чтобы не пачкать метрики)
    url = srcs["site_llms"] + "?qa=1"
    t = grab("vargov.ru/llms.txt", url)
    if t is not None:
        # Сайт пишет «Awards: 26, among them …» (references/vargov.ru-llms.txt:18); запасной
        # якорь — «N awards». Ни того, ни другого — «не смог определить», а не «расходится».
        m = re.search(r"Awards:\s*(\d+)\b", t)
        found = [m.group(1)] if m else sorted({x for x in re.findall(r"\b(\d{1,2}) awards\b", t)})
        if not found:
            out.append(("unknown", "vargov.ru/llms.txt", "awards_total — «Awards: N» / «N awards»", n_aw, "якорь не найден"))
        elif found != [n_aw]:
            out.append(("mismatch", "vargov.ru/llms.txt", "awards_total — «Awards: N»", n_aw, ", ".join(found)))
        if not re.search(rf"\b{total}\b", t):
            out.append(("mismatch", "vargov.ru/llms.txt", "catalogue_total", total, "числа нет"))
        if not re.search(rf"\b{calc} of {total}\b", t):
            out.append(("mismatch", "vargov.ru/llms.txt", "open_with_calc — «360 of 605»", f"{calc} of {total}", "фразы нет"))
        if not re.search(r"\bFBX\b", t):
            out.append(("mismatch", "vargov.ru/llms.txt", "выгрузка FBX упомянута", "слово FBX", "слова нет"))
    # 2) живая карточка датасета на Hugging Face
    t = grab("Hugging Face README", srcs["hf_readme_raw"])
    if t is not None:
        label = "Hugging Face README"
        m = re.search(r"holds \*\*(\d+) design\s+awards\*\*", t)
        if not m:
            out.append(("unknown", label, "awards_total — «holds N design awards»", n_aw, "якорь не найден"))
        elif m.group(1) != n_aw:
            out.append(("mismatch", label, "awards_total — «holds N design awards»", n_aw, m.group(1)))
        m = re.search(r"True for (\d+) records: (\d+) awards", t)
        if not m:
            out.append(("unknown", label, "awarded_skus + awards_total", "", "якорь не найден"))
        elif (m.group(1), m.group(2)) != (str(v("awarded_skus")), n_aw):
            out.append(("mismatch", label, "awarded_skus + awards_total", f"{v('awarded_skus')} / {n_aw}", f"{m.group(1)} / {m.group(2)}"))
        if not re.search(rf"\b{total} lighting and decorative compositions\b", t):
            out.append(("mismatch", label, "catalogue_total", total, "фразы «605 lighting and decorative compositions» нет"))
        m = re.search(r'the "([^"]+)" drawer of the "([^"]+)" step', t)
        if not m:
            out.append(("unknown", label, "fbx_button_path", "", "якорь не найден"))
        elif (m.group(1), m.group(2)) != (fbx["drawer_en"], fbx["step_en"]):
            out.append(("mismatch", label, "fbx_button_path", f'"{fbx["drawer_en"]}" drawer of the "{fbx["step_en"]}" step', f'"{m.group(1)}" drawer of the "{m.group(2)}" step'))
        m = re.search(r"ceiling fixings as separate objects \((one per ceiling hole|one per strand)", t)
        if not m:
            out.append(("unknown", label, "fbx_fixings", "", "якорь не найден"))
        elif m.group(1) != fix["en"]:
            out.append(("mismatch", label, "fbx_fixings", fix["en"], m.group(1)))
    return out


ASSISTANT_PACK = "integration/assistant-answers.json"
ASSISTANT_CATEGORIES = {"catalog", "choice", "custom", "ordering", "price", "materials", "colours", "sizes",
                        "installation", "connection", "production-time", "delivery", "certification", "warranty",
                        "configurator", "brief", "bim", "dealers", "showroom", "awards", "brand", "care", "other"}
# Запреты для ответов помощника на сайте (договор с агентом сайта 27.10.2026): ответ — опубликованный факт о бренде.
ASSISTANT_FORBIDDEN = [
    (r"₽|\bруб(?:\.|л|ей)|\$\s?\d|\d\s?\$|\bUSD\b|€|\bEUR\b", "цены не называем (шеф-монтаж — «по согласованию»)"),
    (r"клемм|\bterminal block", "клеммы не упоминаем"),
    (r"Crystal Breakthrough", "конкурсное название не публикуем (владелец 27.10.2026)"),
    (r"\b2[0-9]\s+(?:наград|international (?:design )?awards)", "награды: «26 достижений на международных премиях» / «26 awards from international juries»"),
    (r"\b(?:10|15|30)\s?(?:мм|mm)\b", "числа правила зазора между отверстиями — внутренние (владелец 25.10.2026)"),
    (r"(?:металлическ\w*|metal) (?:баз\w*|base)[^.]{0,60}(?:схем\w* 1:1|1:1 drawing)", "схема 1:1 при металлической базе — внутренний документ"),
]
# страна производства: Китай допустим только в связке с охраной товарного знака
ASSISTANT_COUNTRY = r"Кита\w*|\bChina\b|\bChinese\b|\bКНР\b"
ASSISTANT_COUNTRY_OK = r"охран|protect|Мадрид|Madrid|товарн\w+ знак|trademark"


def assistant_pack(F: dict) -> tuple[list[str], list[str]]:
    """Пакет ответов помощника: структура, запреты, числа из brand-facts.json. (расхождения, не определено)."""
    bad: list[str] = []
    unknown: list[str] = []
    p = KB / ASSISTANT_PACK
    if not p.is_file():
        return bad, unknown
    try:
        pkg = json.loads(p.read_text(encoding="utf-8"))
        entries = pkg["entries"]
        meta = pkg["meta"]
    except (ValueError, KeyError) as e:
        return bad, [f"НЕ СМОГ ОПРЕДЕЛИТЬ: {ASSISTANT_PACK} — не читается: {e}"]
    canon = json.dumps(entries, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    real = hashlib.sha256(canon.encode("utf-8")).hexdigest()[:16]
    if meta.get("checksum") != real:
        bad.append(f"РАСХОДИТСЯ: {ASSISTANT_PACK} — meta.checksum — ожидалось «{real}» — найдено «{meta.get('checksum')}»")
    if meta.get("count") != len(entries):
        bad.append(f"РАСХОДИТСЯ: {ASSISTANT_PACK} — meta.count — ожидалось «{len(entries)}» — найдено «{meta.get('count')}»")
    total = str(F["catalogue_total"]["value"])
    allowed_of_total = {str(F[k]["value"]) for k in ("open_with_calc", "mounting_scheme", "models3d_linked", "awarded_skus")}
    allowed_of_total.add(str(F["certification"]["value"]["tr_cu_004"]))
    awards = str(F["awards_total"]["value"])
    seen = set()
    for e in entries:
        eid = e.get("id", "?")
        if eid in seen:
            bad.append(f"РАСХОДИТСЯ: {ASSISTANT_PACK} — {eid} — id повторяется")
        seen.add(eid)
        if e.get("category") not in ASSISTANT_CATEGORIES:
            bad.append(f"РАСХОДИТСЯ: {ASSISTANT_PACK} — {eid} — категория вне закрытого списка — найдено «{e.get('category')}»")
        focus = e.get("focus")
        if focus and not str(focus.get("path", "")).startswith("/"):
            bad.append(f"РАСХОДИТСЯ: {ASSISTANT_PACK} — {eid} — focus.path должен начинаться с «/» — найдено «{focus.get('path')}»")
        for lang, text in (e.get("a") or {}).items():
            where = f"{ASSISTANT_PACK} — {eid}/{lang}"
            for rx, why in ASSISTANT_FORBIDDEN:
                m = re.search(rx, text, re.IGNORECASE)
                if m:
                    bad.append(f"РАСХОДИТСЯ: {where} — запрещённое — ожидалось «нет: {why}» — найдено «{m.group(0)}»")
            for m in re.finditer(ASSISTANT_COUNTRY, text):
                around = text[max(0, m.start() - 120):m.end() + 60]
                if not re.search(ASSISTANT_COUNTRY_OK, around, re.IGNORECASE):
                    bad.append(f"РАСХОДИТСЯ: {where} — страна производства не называется — найдено «{m.group(0)}»")
            for m in re.finditer(rf"\b(\d{{2,3}})\s+(?:из|of(?: the)?)\s+{total}\b", text):
                if m.group(1) not in allowed_of_total:
                    bad.append(f"РАСХОДИТСЯ: {where} — «N из {total}» — ожидалось одно из {sorted(allowed_of_total)} — найдено «{m.group(1)}»")
            for m in re.finditer(r"\b(\d{2})\s+(?:достижени\w*|awards from international juries)", text):
                if m.group(1) != awards:
                    bad.append(f"РАСХОДИТСЯ: {where} — число наград — ожидалось «{awards}» — найдено «{m.group(1)}»")
    return bad, unknown


def run(live_mode: bool = False) -> tuple[list[str], list[str]]:
    """Возвращает (расхождения, не определено) — готовые строки для печати."""
    F = load_facts()
    bad: list[str] = []
    unknown: list[str] = []
    notes: list[str] = []
    cache: dict[str, str | None] = {}

    def text_of(rel):
        if rel not in cache:
            p = KB / rel
            cache[rel] = p.read_text(encoding="utf-8").replace("\r\n", "\n") if p.is_file() else None
        return cache[rel]

    for rel, fact, pat, exp in anchors(F):
        t = text_of(rel)
        if t is None:
            if rel in OPTIONAL_FILES:
                notes.append(f"пропущено: {rel} — файла нет на этой машине (вне репозитория)")
            else:
                unknown.append(f"НЕ СМОГ ОПРЕДЕЛИТЬ: {rel} — {fact} — файла нет")
            continue
        hits = list(re.finditer(pat, t, re.MULTILINE | re.DOTALL))
        if not hits:
            unknown.append(f"НЕ СМОГ ОПРЕДЕЛИТЬ: {rel} — {fact} — якорь не найден: {pat!r}")
            continue
        for m in hits:
            line = t.count("\n", 0, m.start()) + 1
            got = m.groups()
            if len(got) != len(exp):
                unknown.append(f"НЕ СМОГ ОПРЕДЕЛИТЬ: {rel}:{line} — {fact} — у якоря {len(got)} групп, ожидаемых значений {len(exp)}")
                continue
            for e, g in zip(exp, got):
                if norm(e) != norm(g):
                    bad.append(f"РАСХОДИТСЯ: {rel}:{line} — {fact} — ожидалось «{e}» — найдено «{g}»")
    for rel, phrase, why in forbidden(F):
        t = text_of(rel)
        if t is None:
            continue
        pos = t.find(phrase)
        if pos >= 0:
            line = t.count("\n", 0, pos) + 1
            bad.append(f"РАСХОДИТСЯ: {rel}:{line} — запрещённая фраза — ожидалось «фразы нет: {why}» — найдено «{phrase}»")
    for kind, rel, fact, exp, got in structural(F):
        if kind == "mismatch":
            bad.append(f"РАСХОДИТСЯ: {rel} — {fact} — ожидалось «{exp}» — найдено «{got}»")
        elif kind == "unknown":
            unknown.append(f"НЕ СМОГ ОПРЕДЕЛИТЬ: {rel} — {fact} — {got}")
        else:
            notes.append(got if rel == "" else f"{rel}: {got}")
    pack_bad, pack_unknown = assistant_pack(F)
    bad += pack_bad
    unknown += pack_unknown
    if live_mode:
        for kind, src, fact, exp, got in live(F):
            tag = "[live] "
            if kind == "mismatch":
                bad.append(f"РАСХОДИТСЯ: {tag}{src} — {fact} — ожидалось «{exp}» — найдено «{got}»")
            else:
                unknown.append(f"НЕ СМОГ ОПРЕДЕЛИТЬ: {tag}{src} — {fact} — {got}")
    for n in notes:
        print("пометка:", n)
    return bad, unknown


def main() -> int:
    ap = argparse.ArgumentParser(description="Сверка текстов базы с references/brand-facts.json")
    ap.add_argument("--live", action="store_true", help="плюс vargov.ru/llms.txt?qa=1 и живая карточка Hugging Face (по одному запросу)")
    args = ap.parse_args()
    F = load_facts()
    n_anchors = len(anchors(F)) + len(forbidden(F))
    bad, unknown = run(live_mode=args.live)
    for b in bad:
        print(b)
    for u in unknown:
        print(u)
    print(f"check_facts: якорей {n_anchors} (+ структурные проверки JSON{', + живые источники' if args.live else ''}); "
          f"расхождений {len(bad)}, не определено {len(unknown)}")
    if bad and unknown:
        print("код 1: есть и расхождения, и ненайденные якоря")
    elif bad:
        print("код 1: расхождения с brand-facts.json")
    elif unknown:
        print("код 1: якоря не найдены — текст переписали, поправьте ANCHORS в check_facts.py или верните формулировку")
    else:
        print("Тексты базы совпадают с references/brand-facts.json.")
    return 1 if (bad or unknown) else 0


if __name__ == "__main__":
    raise SystemExit(main())
