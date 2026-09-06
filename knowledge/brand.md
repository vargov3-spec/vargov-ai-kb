# Vargov® Design — Brand Facts

Источник: репозиторий сайта `V:/new site Vargov Design/web` (`src/lib/data/*`, `src/lib/seo.ts`, `src/app/llms.txt/route.ts`), сверено 2026-09-04. Живой сайт — [vargov.ru](https://vargov.ru), машиночитаемая карта — [vargov.ru/llms.txt](https://vargov.ru/llms.txt). Ниже — только подтверждённые данными сайта факты; всё, что осталось с прежней (Tilda) версии и на новом сайте не сверено, помечено явно.

## Кто это
- Бренд: **Vargov® Design** (в разметке сайта — `Vargov®Design`, alternateName `Vargov Design`) — авторские световые и декоративные композиции.
- Слоган (seo.ts): «Российский дизайн. Мировой масштаб.» / «Russian design. Global scale.»
- Описание организации (seo.ts, ORG_TEXT): «Авторский бренд коллекционных световых и декоративных композиций из художественного стекла, хрусталя, керамики и металла» — это описание бренда; в текстах о конкретных изделиях материалы не называются (правило владельца).
- Основатель и главный дизайнер: **Антон Варгов** (Anton Vargov, «Founder and lead designer»). Член жюри премий в области дизайна и архитектуры (ADD Awards, Высокое жюри X сезона, 2024).
- Собственное производство, изготовление под заказ: каждая композиция собирается под конкретный интерьер, масштаб и геометрия подстраиваются под пространство (llms.txt).
- Organization JSON-LD: `@id` = `https://vargov.ru#organization` (ORG_ID в seo.ts) — использовать для `brand`/`manufacturer` в любой внешней разметке; `areaServed`: RU, AE, VN; логотип — ImageObject 512×512 из `/press-assets/` (файл `vargov-design-logo-512.png`, см. [[gap-list-2026-09]] п. 8), не `apple-icon.png`. В сборщике базы (`references/organization.jsonld`) поле `logo` не задано — добавить тот же ImageObject.

## Платформа сайта
- vargov.ru — собственный сайт на **Next.js** на собственном VPS (nginx), не Tilda; переезд завершён к 27.07.2026. Старые адреса Tilda (`/…_vargovdesign_ru/tproduct/…`) редиректят, печатать только канонические.
- **8 языков**: RU — корень `https://vargov.ru`, EN — `https://vargov.ru/en`, далее `https://vargov.ru/<de|it|fr|es|vi|ar>`; hreflang с `x-default` = EN. VI и AR переведены не целиком (комментарий в `domains.ts`).
- `vargov.design` — **не сайт, а английский конфигуратор**; `configurator.vargov.ru` — русский конфигуратор. Awwwards Nominee 2026 (номинация, не победа).
- Для ИИ: `robots.txt` явно разрешает GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-Web, anthropic-ai, PerplexityBot, Perplexity-User, Google-Extended, Applebot-Extended, Amazonbot, CCBot, YandexBot; `llms.txt` собирается из данных (число композиций и наград не вписано руками); sitemap.xml; Organization и BreadcrumbList JSON-LD. **Product JSON-LD на карточках нет** (снята 26.08.2026, см. [[ai-visibility-audit-2026-09]]).

## Товарный знак
- Товарный знак **VARGOV**, регистрационный № 896936.
- Дата подачи заявки: 29.04.2022. Дата регистрации: 06.10.2022. Действует до 29.04.2032.
- Правообладатель: Антон Варгов.

## Каталог: 605 композиций, 4 категории
`catalog.generated.json` — 605 позиций, артикулы LC0001…LC0602; у каждой обложка, галерея, тип и категория. Карточка: `https://vargov.ru/catalog/<slug>` (slug = артикул строчными, напр. `lc0602`), EN — `https://vargov.ru/en/catalog/<slug>`, другие языки — `https://vargov.ru/<lang>/catalog/<slug>`. Обложки — `https://vargov.ru/img/catalog/…`.

| Категория (ключ) | RU (навигация) | EN | Позиций | RU | EN |
|---|---|---|---|---|---|
| `lighting` | Световые композиции | Lighting compositions | 352 | https://vargov.ru/lighting | https://vargov.ru/en/lighting |
| `decorative` | Декоративные композиции | Decorative compositions | 114 | https://vargov.ru/decorative | https://vargov.ru/en/decorative |
| `floor-table-lamps` | Торшеры и арт-объекты | Floor lamps, sconces & tabletop objects | 56 | https://vargov.ru/floor-table-lamps | https://vargov.ru/en/floor-table-lamps |
| `sculptural-decor` | Скульптурные композиции | Sculptural compositions & decor | 83 | https://vargov.ru/sculptural-decor | https://vargov.ru/en/sculptural-decor |

- Общий каталог: https://vargov.ru/catalog (EN https://vargov.ru/en/catalog) — поиск по артикулу, фильтр по типу, поиск по фотографии. PDF-каталог: https://vargov.ru/pdf/vargov-catalog-ru.pdf, https://vargov.ru/pdf/vargov-catalog-en.pdf.
- Подборки «по пространству» (`/for/<key>`, EN `/en/for/<key>`): hotel-lobby, double-height, stairwell, restaurant, dining, bedroom, retail, spa.
- 3D-модели: у карточек есть ссылки на модели аккаунта vargov на 3ddd.ru (поле `model3d`).
- **Описания**: `product-copy/products.{ru,en,de,fr,it,es,vi,ar}.json` — 605 SKU × 8 языков, согласованы владельцем (`type`, `paragraphs`, `whereItWorks`, `style`, `madeToOrder`, флаг `awardWinning`). Это единственный источник названий (тип + артикул) и описаний для любых материалов.

## Элементы в наличии
- Страница https://vargov.ru/in-stock (EN `/en/in-stock`), обновляется четыре раза в день (llms.txt). Данные — `instock.generated.json`: 24 записи на 2026-09-04 (артикул, размер, материал, цвет, количество) — это **элементы**, а не готовые изделия.
- Условия программы прежней версии сайта (срок 15–20 рабочих дней вместо 40–60, цена ниже примерно на 10%, кастомизация подвеса/кабеля/крепежа/цвета) — на новом сайте **не сверено**.

## Процесс заказа (текст прежней версии сайта, июль 2026 — на новом сайте не сверено)
1. Заказ — связь через WhatsApp, расчёт стоимости и сроков, договор-спецификация. 2. Предоплата 50%. 3. Производство 40–60 рабочих дней (3D-модель, монтажная схема, изготовление). 4. Подтверждение фото/видео. 5. Окончательная оплата 50%. 6. Доставка 14–25 дней по региону. 7. Монтаж — опционально (Россия, ОАЭ). Подтверждённое llms.txt: доставка по всему миру в фирменной обрешётке; для архитекторов — https://vargov.ru/en/architects (как идёт проект от эскиза до монтажа).

## Награды — 23
Полный верифицированный список с официальными формулировками, ссылками на страницы премий и сертификатами — [[awards-verified]] (источник `awards.ts`, `awardsCount()` = 23; два «Официальных поздравления жюри» — документы, в счёт не идут). Программы: MUSE Design Awards (Platinum 2023, Gold 2026), International Architecture & Design Awards · ADC (Platinum, Gold 2023), The London Design Awards (Platinum 2023), NY Product Design Awards (Product Designer of the Year, Gold ×2 2023), Houzee Awards (Gold 2023), IDA Design Awards (Silver 2022, Honorable Mention 2025), LIT Lighting Design Awards (Winner 2022, Honorable Mention 2025), European Product Design Award 2023, BLT Built Design Awards 2023, SIT Furniture Design Award (2023, 2025), LOOP Design Awards 2025, Luxury Lifestyle Awards 2024, ADD Awards (2-е место 2023; жюри 2024), Interlight Russia · Российский светодизайн (специальный приз 2022), Awwwards (Nominee 2026). Страница: https://vargov.ru/awards · https://vargov.ru/en/awards. В Organization JSON-LD: «Более 20 международных премий в области дизайна и света».

## Выставки
- **2022** — специальный приз конкурса «Российский светодизайн» на Interlight за серию ленточных композиций LC0217 (награда № 22 в [[awards-verified]]).
- **Октябрь 2025** — **первый собственный стенд** бренда на Interlight Moscow; композиции показаны собранными и включёнными в реальном масштабе. После выставки экспозиция целиком переехала в шоурум. Формулировка «первое участие в 2025» не используется (правило владельца). Видео-интервью: https://www.youtube.com/watch?v=_HBECagnlDI. Раздел «Проекты»: https://vargov.ru/projects.

## Сертификация (страница https://vargov.ru/certification · https://vargov.ru/en/certification)
- Серийные **сертификаты соответствия ТР ЕАЭС**: № 10095925 (ТР ТС 004/2011 «О безопасности низковольтного оборудования» + ТР ТС 020/2011 «Электромагнитная совместимость», 53 артикула) и № 10095927 (ТР ТС 004/2011, 250 артикулов); схема 1с, серийный выпуск; действуют с 01.06.2026 по 31.05.2031; орган — ООО «Тест-С.-Петербург» (аттестат РОСС RU.0001.10СП28); более 300 артикулов LC; знак **EAC**.
- Испытания по ГОСТ IEC 60598-1-2017, 60598-2-1-2011, 62471-2013, 62493-2014, 61547-2013, CISPR 15-2014, 61000-3-2-2017, 61000-3-3-2015.
- **Декларации о соответствии ТР ЕАЭС 037/2016** (ограничение опасных веществ): ЕАЭС N RU Д-CN.РА07.В.71518/26 (53 артикула) и ЕАЭС N RU Д-CN.РА07.В.71557/26 (266 артикулов), зарегистрированы 29.08.2026, действуют до 27.08.2031; 310 уникальных артикулов.
- Короткая строка (CERT_LINE): «EAC · ТР ТС 004/2011, ТР ТС 020/2011, ТР ЕАЭС 037/2016 · испытания по ГОСТ IEC 60598-1».

## Шоурум и дилеры
- Официальный шоурум: Москва, Нахимовский проспект 24, павильон 2, стенд 212 (латиницей: 24 Nakhimovsky Prospekt, Pavilion 2, Stand 212, Moscow). Открыт ежедневно 12:00–20:00; телефон шоурума +7 (925) 888-77-44. Страница https://vargov.ru/showroom.
- Официальные дилеры: список и контакты — https://vargov.ru/official-dealers (в базе знаний не дублируются; перечень — в приватной папке PR владельца). Шоурум подробно — [[dealers-showrooms]].

## Контакты (seo.ts CONTACTS)
- Email: info@vargov.ru
- Телефон: +7 916 537 33 52 (`tel:+79165373352`)
- WhatsApp: https://wa.me/79165373352 (старый `wa.me/message/SAC5LWOV5QMXC1` не использовать)
- Telegram бренда: https://t.me/vargov_design (@vargov_design); личный: https://t.me/AntonVargov
- WeChat: Vargov_Design
- YouTube: https://www.youtube.com/channel/UCKvjqNdKMn4fk95wNc765MA · RuTube: https://rutube.ru/channel/38329605/
- `sameAs` в Organization JSON-LD — 35 адресов (сверено 05.09.2026): оба Telegram, YouTube, RuTube, https://vargov.design/, 3ddd/3dsky, Instagram https://www.instagram.com/vargov_design/, Pinterest https://www.pinterest.com/Vargov_Design/ (7e9a8e5; видимая ссылка в подвале), Facebook https://www.facebook.com/vargovdesign (2ff2d36, только sameAs), Wikidata https://www.wikidata.org/wiki/Q141301076, Google Карты https://www.google.com/maps?cid=2970420474499935128 и Яндекс Карты https://yandex.ru/maps/org/vargov_design/199433674369/ (59a3ef6), GitHub vargov-ai-kb и страницы победителей премий. Видимой ссылки на Instagram в подвале нет (решение владельца); MAX на новом сайте не публикуется.

## Упаковка/защита при доставке (текст прежней версии сайта — на новом не сверено)
Плёнка, плотный поролон, фирменные картонные вкладыши, фирменный скотч, деревянный каркас, фанерные ящики, джутовая обёртка, финальный защитный слой плёнки. Подтверждено llms.txt: «Delivery: worldwide, in branded crating».

## Монтаж и подключение (кратко)
Пять этапов, схема 1:1 на баннерной ткани, закладные из фанеры от 9 мм, отверстия 8–14 мм, сценарии 12–24 В и 220 В, маркировка проводов бирками-ограничителями высоты, три варианта монтажа, услуга шеф-монтажа. PDF-инструкция: https://vargov.ru/pdf/vargov-installation.pdf. Подробно — [[installation-guide]].

## Параметры элементов (граница, действует с 06.09.2026)

Композиция набирается из повторяющихся элементов. **Параметры ЭЛЕМЕНТА публикуются:** габариты на каждый размер ряда одной строкой, вес и мощность. Владелец разрешил отдать их и людям (строка «Параметры элементов» в карточке сайта), и машинам. Источник один — выгрузка конфигуратора `element-specs.generated.json`, 336 артикулов из 605; у остальных ряда размеров нет.

**Параметры ИЗДЕЛИЯ не публикуются никогда:** размер композиции считается под помещение, поэтому у `Product` нет и не должно быть `width`, `height`, `depth`, `size`, `weight`, `material`, `offers`, `price`. Элементные числа живут только в `additionalProperty` (`Element size <ряд>` строкой, `Element weight <ряд>` числом с `KGM`, `Power per element` с `WTT`) — свойство описывает элемент, а не изделие, путать нельзя. То же правило записано в шапке фида сайта (`src/app/catalog.jsonld/route.ts`).

Материал элемента в выгрузке есть, но ни сайт, ни база его не отдают: правило «материалы не называем» продолжает действовать.

В графе базы это зеркало фида сайта, сверенное побайтово 06.09.2026: 974 габарита, 974 веса, 218 значений мощности, расхождений с `vargov.ru/catalog.jsonld` — ноль.

## Домены и площадки
- https://vargov.ru — сайт (RU + 7 языков), каталог, llms.txt.
- https://vargov.design/ — генеративный 3D-конфигуратор (EN); https://configurator.vargov.ru/ — RU.
  - **Политика конфигуратора обратна политике сайта и базы знаний (подтверждено агентом конфигуратора 06.09.2026):** логика композиций и данные проприетарные, поэтому в `robots.txt` конфигуратора поимённо закрыты все ИИ-краулеры (GPTBot, ClaudeBot, anthropic-ai, CCBot, Google-Extended, PerplexityBot, Bytespider, Meta-External*, cohere-ai, Diffbot и другие), `llms.txt` там намеренно нет. Закрыты именно модели и краулеры данных, а не индексация: страницы артикулов `/sku/<sku>/` (934 адреса, RU и EN) открыты обычным поисковикам и несут Product-разметку, то есть в органическом поиске бренд ими представлен. Для ИИ-видимости конфигуратор источником не считается — в корпуса языковых моделей его страницы не попадают. Единственная точка правды о бренде — сайт и эта база.
  - В разметке страниц `/sku/<sku>/` конфигуратора производитель указан ссылкой на ту же сущность, что и на сайте: `"brand": {"@id": "https://vargov.ru/#organization"}` (правка агента конфигуратора 06.09.2026, коммит 0856dcb3; выкладка — по слову владельца). Отдельной Organization у конфигуратора нет и не должно быть.
  - В открытых текстах о конфигураторе называем только результат и адреса страниц; внутреннее устройство (форматы данных, имена файлов, механика раскладки) не публикуем — просьба агента конфигуратора от 06.09.2026.
- Каналы: Telegram, YouTube, RuTube, Pinterest (аккаунт Vargov_Design), 3ddd.ru (аккаунт vargov, 3D-модели).

## Что важно знать контент-команде
Описания всех 605 композиций **согласованы владельцем и существуют на 8 языках** (`product-copy/*.json`) — брать оттуда, не переписывать. Оставшийся пробел — **технические характеристики по каждому изделию** (материалы, размеры, мощность), которые владелец **сознательно не выносит на карточки**: размер — «любой, рассчитывается под пространство», цены не публикуются, материалы в текстах об изделии не называются, в JSON-LD нет `material`/`size`/`price`. Собранные характеристики (анкеты премий, [[specs-intake-README]]) — только для внутренних датасетов и заявок на премии.
