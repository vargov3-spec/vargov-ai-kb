# Пакет агенту сайта: видимость для ИИ, 22.09.2026

Источник задач — [[ai-visibility-global-2026-09-22]], пункты 3, 4, 5 рекомендаций.
Всё бесплатно; правила бренда: без цен, материалов, IP, CE, гарантии, сроков (кроме
«15–20 рабочих дней» для готовых элементов со склада), страна производства не называется.
Выкладка — по слову владельца.

## A. Страницы «по пространству» (/for/…, 10 × 8 языков): блок «Как это делается»

Зачем. По вопросу «кто делает световые инсталляции в лестничный проём с 3D-моделью»
Duck.ai цитирует sk-glass.ru, romatti.ru, svetholl.ru — их страницы говорят словами задачи:
«3D-макет», «монтаж», «ТЗ на потолок». Perplexity уже берёт наши /for/ в шорт-лист — нужен
текст под сам вопрос. Один блок на все десять страниц, с одной переменной — типом
пространства; ставить после вступления, до подборки композиций.

**RU**

### Как это делается

1. **Задача.** Вы присылаете план и высоту помещения, фото или рендер, точку подвеса —
   или просто описываете, что должно получиться. Для {пространства} обычно важны: высота
   проёма, где стоит зритель, что видно с верхних уровней.
2. **3D-модель до изготовления.** Композиция собирается в конфигураторе бренда: число и
   размер элементов, форма облака, высота подвесов, узлы крепления. Дизайнер получает
   ссылку на модель, спецификацию в PDF, чертёж DXF и модель IFC4 для проекта.
3. **Согласование.** Правки вносятся в модель, а не в готовую вещь; масса композиции и
   нагрузка на точки подвеса считаются по составу — это нужно конструктору потолка.
4. **Изготовление.** Каждый элемент делается под эту композицию на собственном
   производстве бренда; готовые элементы для быстрых решений есть на складе.
5. **Монтаж.** К композиции идёт инструкция по монтажу и схема узлов; в Москве монтаж
   выполняет шоурум, у дилеров в Дубае и Ханое — их бригады.

**Что получает дизайнер:** 3D-модель и ссылку на неё, PDF-спецификацию, DXF, IFC4, схему
подвеса, снимки композиции для презентации заказчику. Всё это можно показать в шоуруме в
Москве (Нахимовский пр., 24) или у дилеров.

**EN**

### How it is done

1. **Brief.** Send the floor plan and ceiling height, a photo or a render, and the
   suspension point — or simply describe the result you want. For {space} what matters
   most is the height of the void, where the viewer stands and what is seen from above.
2. **A 3D model before production.** The composition is assembled in the brand's
   configurator: number and size of elements, cloud shape, drop lengths, fixing points. The
   designer receives a link to the model, a PDF specification, a DXF drawing and an IFC4
   model for the project.
3. **Approval.** Changes are made to the model, not to a finished piece; the weight of the
   composition and the load per suspension point are calculated from its composition —
   the ceiling engineer needs exactly this.
4. **Production.** Every element is made for this composition at the brand's own
   production; ready-made elements for fast solutions are kept in stock.
5. **Installation.** Each composition comes with installation instructions and a node
   diagram; in Moscow the showroom team installs, in Dubai and Hanoi — the dealers' crews.

**What the designer gets:** the 3D model and a link to it, a PDF specification, DXF, IFC4,
a suspension diagram, images of the composition for the client presentation. All of it can
be seen at the showroom in Moscow (Nakhimovsky Prospekt 24) or at the dealers.

Подстановка {пространства}: hotel-lobby — «лобби отеля / a hotel lobby»; double-height —
«двусветной гостиной / a double-height living room»; stairwell — «лестничного проёма / a
stairwell»; restaurant, dining, bedroom, retail, spa, atrium, banquet — по названию страницы.
Переводы на de/fr/it/es/vi/ar — по вашему обычному конвейеру с EN-версии.

Проверка после выкладки: у страницы без JS должно быть ≥ 1 500 знаков текста (NBS: ИИ и
спецификаторы читают HTML, не JSON).

## B. Страницы дилеров: /en/dealers/dubai и /en/dealers/hanoi (+ ru, + остальные языки)

Зачем. По «designer in Dubai: bespoke studios with showroom in Dubai» ни один ассистент
не находит нас: дилер существует только строкой на /dealers, домен vargovdesign.com не
отвечает. Нужны отдельные адреса с LocalBusiness-разметкой и текстом под вопрос.

Данные — те, что уже стоят на vargov.ru/dealers (сверить с владельцем перед выкладкой):
- **Dubai** — Vargov Design International, Showroom 1, Al Asmawi Building, Sheikh Zayed
  Road, PO Box 24710, Dubai, UAE; +971 56 787 8789; sales@vargovdesign.com; регионы —
  Персидский залив, Ближний Восток, Америка, Европа, Азия, Африка.
- **Hanoi** — VITRILUX SPACE CO., LTD, 4th Floor, No. 2 Thang Long Avenue, Tu Liem Ward,
  Hanoi; Zalo/WhatsApp +84 901 153 999; vitrilux.vn@gmail.com; Вьетнам, Лаос, Камбоджа,
  Таиланд, Малайзия, Сингапур.

Текст (EN, шаблон): «Vargov Design in Dubai — official dealer. Bespoke lighting and
decorative compositions by Vargov®Design for villas, hotel lobbies and restaurants in the
UAE and the Gulf: made to order, a 3D model before production, installation by the dealer's
crew. See the pieces at the showroom on Sheikh Zayed Road or request the 3D model of a
composition for your project.» Далее — часы, карта, контакты, подборка 6–8 композиций для
пространств региона (лобби, вилла, ресторан), ссылка на конфигуратор.

Разметка: `LocalBusiness` (name, address, telephone, email, areaServed, parentOrganization
→ Organization Vargov®Design, sameAs → страница дилера), в Organization — `subOrganization`
или `location` на оба адреса. В llms.txt — строка «Dealers: Moscow (showroom), Dubai
(Sheikh Zayed Road), Hanoi (Thang Long Avenue)». Дилерам — завести бесплатные Google
Business Profile «Vargov Design International — Dubai» и «Vargov Design — Hanoi» (это
владелец/дилеры; тексты дам).

## C. Гигиена обхода

1. **robots.txt** — явные группы (сейчас Claude-User и Claude-SearchBot покрыты только
   `*`; при любой будущей правке `*` их заденет):
   ```
   User-agent: Claude-User
   Allow: /
   User-agent: Claude-SearchBot
   Allow: /
   User-agent: Meta-WebIndexer
   Allow: /
   ```
   Остальные (GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, PerplexityBot,
   Google-Extended, Applebot, Amazonbot, CCBot, YandexBot, bingbot) — уже открыты.
2. **llms.txt** — ссылка из HTML в `<head>`: `<link rel="alternate" type="text/plain"
   href="/llms.txt" title="LLM-friendly summary">`; в тексте llms.txt заменить «605
   compositions, each with … dimensions» на «…; element dimensions where the brand
   publishes them». Файл держим, но рычагом не считаем (97 % llms.txt не запрашиваются).
3. **IndexNow** — ключ-файл в корне и пинг `api.indexnow.org/indexnow` при каждой выкладке
   для изменившихся адресов (Bing/Copilot и Яндекс берут; Bing — второй источник переходов
   из ИИ, 24 за две недели). Бесплатно.
4. **Сниппеты** — убедиться, что на каталоге и гайдах нет `nosnippet` / `max-snippet`:
   Google для AI Overviews требует только индекс и право на сниппет.
5. **Хвост Tilda** — GPTBot просит `/sitemap-store.xml` и `/sitemap-feeds.xml` (по 3 раза):
   можно отдать 301 на `/sitemap.xml`, не обязательно.
6. **Bing Webmaster Tools** и **Яндекс Вебмастер → «Видимость сайта в Алисе AI»** — подключить
   как бесплатные измерители (вход владельца).

## D. Что не делать

Product JSON-LD «ради ИИ» (Ahrefs: цитирований не прибавляет), платные листинги, страну
производства в любом тексте, сроки и материалы в блоках «как это делается».
