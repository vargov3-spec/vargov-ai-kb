# Черновик Wikidata-сущностей для Vargov® Design

Подготовлено 2026-07-06. **Не опубликовано** — создание пунктов Wikidata требует аккаунта и выполняется через веб-интерфейс wikidata.org; в этой сессии нет доступа к браузеру, чтобы сделать это напрямую. Ниже — готовый к вставке черновик на две сущности.

## Почему Wikidata, а не сразу Wikipedia
У Wikidata порог значимости (notability) сильно ниже, чем у Wikipedia: по [правилам Wikidata](https://www.wikidata.org/wiki/Wikidata:Notability) достаточно, чтобы сущность была «идентифицируемой» и описывалась через «серьёзные, публично доступные источники» — не обязательно СМИ. У нас такие источники есть (см. [[external-references]]): страницы победителей в базах International Design Awards, New York Product Design Awards, RLDC, справочник ICONIC, страница жюри ADD Awards.
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
| manufacturer / production place | China (производство), Russia (дизайн) | vargov.ru/branded_products_vargovdesign_ru |

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
| country of citizenship (P27) | Russia (Q159) | косвенно (бренд "Russian", шоурум в Москве) — проверить перед публикацией |
| official website / sameAs | https://www.iconic-world.com/directory/anton-vargov | независимый справочник |
| award received (P166) | International Design Awards winner (LC0236) | https://www.idesignawards.com/winners/zoom.php?eid=9-46057-22 |
| award received (P166) | New York Product Design Awards winner (LC0343) | https://nydesignawards.com/winner-info.php?id=1296 |
| position held / jury member | ADD Awards Grand Jury, 10th season | https://addawards.ru/jury/293063/ |

---

## Что нужно перед публикацией
1. Подтвердить у Антона Варгова точное гражданство/страну (не только предполагать по бренду).
2. Проверить, есть ли у наград (IDA, NYPDA, RLDC, LOOP, ADD) собственные пункты Wikidata — если нет, ссылки на них как на "award received" будут просто текстом/URL, без связи QID-to-QID, это нормально для старта.
3. Создать аккаунт на wikidata.org (обычная бесплатная регистрация) — без аккаунта редактирование ограничено.
4. Опубликовать сначала сущность 2 (Anton Vargov), затем сущность 1 со ссылкой founder → на неё.

См. также [[brand]], [[external-references]].
