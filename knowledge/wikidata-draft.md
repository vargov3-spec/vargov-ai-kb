# Черновик Wikidata-сущностей для Vargov® Design

Подготовлено 2026-07-06, формулировки наград пересобраны из `awards.ts` сайта 2026-09-04. **Не опубликовано** — создание пунктов Wikidata требует аккаунта и выполняется через веб-интерфейс wikidata.org; в этой сессии нет доступа к браузеру, чтобы сделать это напрямую. Ниже — готовый к вставке черновик на две сущности.

## Почему Wikidata, а не сразу Wikipedia
У Wikidata порог значимости (notability) сильно ниже, чем у Wikipedia: по [правилам Wikidata](https://www.wikidata.org/wiki/Wikidata:Notability) достаточно, чтобы сущность была «идентифицируемой» и описывалась через «серьёзные, публично доступные источники» — не обязательно СМИ. У нас такие источники есть (см. [[external-references]]): страницы победителей на сайтах самих премий (IDA Design Awards, NY Product Design Awards, MUSE Design Awards, International Architecture & Design Awards · ADC, The London Design Awards, LIT, LOOP, SIT, BLT, European Product Design Award, Luxury Lifestyle Awards), справочник ICONIC, страница жюри ADD Awards. Всего 22 награды — полный список с официальными формулировками в [[awards-verified]].
Честно: это защитимый, но не железобетонный кейс — источники есть, но это не крупные независимые публикации в прессе. Пункт может быть создан, но теоретически может быть оспорен другим редактором Wikidata. Для Wikipedia (в отличие от Wikidata) этого пока однозначно недостаточно.

---

## Сущность 1: Vargov Design (бренд/организация)

- **Label (en):** Vargov Design
- **Label (ru):** Vargov Design
- **Description (en):** Russian brand of author's lighting and decorative compositions
- **Description (ru):** российский бренд авторских световых и декоративных композиций
- **Aliases:** Vargov®Design, VARGOV

**Заявления (statements):**
| Свойство | Значение | Источник |
|---|---|---|
| instance of (P31) | brand (Q431289) | vargov.ru |
| country (P17) | Russia (Q159) | vargov.ru |
| official website (P856) | https://vargov.ru | — |
| founder (P112) | Anton Vargov (см. сущность 2) | vargov.ru |
| industry (P452) | lighting design / interior design | vargov.ru |

**Не включать:** место производства (страну). Правило владельца: страну не называть, писать «собственное производство» — на сайте и в llms.txt сделано именно так, и заявка в Wikidata с указанием страны производства противоречила бы публичным материалам бренда.

**Не включать без дополнительной проверки:** точный год основания компании (известна только дата регистрации товарного знака — 2022-04-29 заявка, 2022-10-06 регистрация — это НЕ обязательно год основания бизнеса).

---

## Сущность 2: Anton Vargov (персона)

- **Label (en):** Anton Vargov
- **Label (ru):** Антон Варгов
- **Description (en):** Russian lighting and product designer, founder of Vargov Design

**Заявления (statements):**
| Свойство | Значение | Источник |
|---|---|---|
| instance of (P31) | human (Q5) | — |
| occupation (P106) | designer (Q1281618) | vargov.ru, iconic-world.com |
| country of citizenship (P27) | Russia (Q159) | **подтверждено** — страна «Russia / Russian Federation» указана в анкетах победителя трёх независимых премий (IDA, NYPDA, AD-C), см. [[awards-verified]] |
| official website / sameAs | https://www.iconic-world.com/directory/anton-vargov | независимый справочник |
| award received (P166) | International Architecture & Design Awards · ADC 2023 — **Platinum Winner**, Lighting Product Design Built / Professional (LC0303) | https://ad-c.org/winner/light-composition-vargov-design-lc0303/ |
| award received (P166) | MUSE Design Awards 2023 — **Platinum Winner**, Lighting Design — Designer / Custom Lighting (LC0237) | https://design.museaward.com/winners-info.php?id=13101 |
| award received (P166) | The London Design Awards 2023 — **Platinum Winner**, Product Design — Lighting (LC0326) | https://thelondondesignawards.com/winner-info.php?id=538 |
| award received (P166) | NY Product Design Awards 2023 — **Product Designer of the Year**, Lamps & Luminaires — Pendant Luminaires (LC0343) | https://nydesignawards.com/winner-info.php?id=1296 |
| award received (P166) | MUSE Design Awards 2026 — **Gold Winner**, «Oceanic Illumination» (LC0564) | https://design.museaward.com/winners-info.php?id=40265 |
| award received (P166) | International Architecture & Design Awards · ADC 2023 — **Gold Winner**, «Drapery» (LC0323) | https://ad-c.org/winner/vargov-design-lc0323-drapery/ |
| award received (P166) | IDA Design Awards 2022 — Silver, Illumination — Designer Lighting (LC0236) | https://www.idesignawards.com/winners/zoom.php?eid=9-46057-22 |
| award received (P166) | IDA Design Awards 2025 — Honorable Mention, Home & Living / Lighting (LC0516) | https://www.idesignawards.com/winners/zoom.php?eid=9-61165-25 |
| award received (P166) | Luxury Lifestyle Awards 2024 — Winner, Best Luxury Lighting Design Studio in Dubai, UAE | https://luxurylifestyleawards.com/winners/lighting-design-studio/vargov-design |
| position held / jury member | ADD Awards Grand Jury, 10th season | https://addawards.ru/jury/293063/ |

---

## Что нужно перед публикацией
1. ~~Подтвердить гражданство~~ — **сделано 2026-07-07**: страна Russia подтверждена анкетами трёх независимых премий, см. [[awards-verified]].
2. Проверить, есть ли у наград (IDA, NYPDA, MUSE, ADC, LOOP, ADD) собственные пункты Wikidata — если нет, ссылки на них как на "award received" будут просто текстом/URL, без связи QID-to-QID, это нормально для старта.
3. Создать аккаунт на wikidata.org (обычная бесплатная регистрация) — без аккаунта редактирование ограничено.
4. Опубликовать сначала сущность 2 (Anton Vargov), затем сущность 1 со ссылкой founder → на неё.

**Статус готовности: черновик полный, блокеров нет** (июльская блокировка диапазона 46.28.64.0/21 истекла 13.08.2026; заходить лучше не через VPN — Wikimedia блокирует диапазоны хостингов). Осталось только действие пользователя — аккаунт и внесение (создание учётных записей я не выполняю).

См. также [[brand]], [[external-references]].
