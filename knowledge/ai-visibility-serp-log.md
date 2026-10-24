# Журнал замеров категорийной выдачи

Ежемесячный замер: называют ли поисковые и языковые системы Vargov® Design, когда спрашивают
не про бренд по имени, а про категорию — «лучшие бренды дизайнерского освещения», «скульптурные
люстры», «коллекционные световые студии». По имени бренд находится идеально; вопрос в том,
попадает ли он в ответ, когда имя не названо.

Метод один и тот же от замера к замеру, иначе цифры не сравнить: десять запросов через веб-поиск,
по каждому фиксируется, кто выдаётся, есть ли среди них мы, и какие страницы кормят эту выдачу.
Сайт vargov.ru при этом не сканируется. Регулярный прогон — задача `vargov-ai-serp-monthly`,
1-го числа каждого месяца.

**С 10.09.2026 к замеру добавлен второй, количественный показатель — переходы из ИИ на сайт.**
Языковые модели дописывают свою метку к ссылкам в ответах, поэтому визиты видны в Метрике
поимённо. Снимать в счётчике 111091941 (логин info@vargov.ru) отчётом
`/stat/sources?id=111091941&period=month` с группировкой «UTM Source», плюс тот же отчёт
с группировкой «Домен реферера» — часть переходов приходит без метки. Считаются
`chatgpt.com`, `perplexity.ai`, `gemini.google.com`, `copilot.microsoft.com`.

База, 11 августа — 10 сентября 2026: **chatgpt.com — 18 визитов по метке и 10 по рефереру,
глубина 5,22, время 3 м 27 с; gemini.google.com — 1; perplexity.ai — 1.** Для сравнения,
Instagram за тот же месяц — 15 визитов при глубине 2,67. То есть ответы ИИ уже приводят
на сайт не меньше людей, чем соцсеть, и людей более заинтересованных. Это первая
измеримая связь между этой работой и сеансами; подробности — `traffic-utm-2026-09.md`.

---

## 2026-10-22 (полный замер)

Плановая точка 22.10; задача сработала с опозданием, снято **24.10.2026, 11:05–12:10 UTC**, браузер владельца (Chrome).
Вопросы — из [[ai-probe-set]] дословно (блоки A, B, C, E) плюс контрольный «Do Vargov Design compositions support DALI?».

**Что удалось снять, что нет:**
- Google AI Mode (`udm=50&hl=en`) — все 17 вопросов.
- Яндекс Алиса AI (вкладка в выдаче ya.ru) — 5 вопросов (A1, B1, B6, C2, E2); капчи не было.
  Оговорка: в Яндексе браузер вошёл под учётной записью бренда, ответы могут быть персонализированы.
- **Perplexity — не снят:** без входа на любой вопрос отвечает «Sign up and repeat your request» (проверено на B2 и E1).
  15.10 открывался без входа. Входить не стали.
- **Duck.ai — не снят:** отправка вопроса означает принятие условий («Нажимая «Запрос», вы принимаете наши условия») — по правилу замера не принимали.
- **Bing Webmaster → AI Performance — не снят:** в этом Chrome нет входа владельца в Bing.

### Пробы

| Вопрос | Ассистент | Vargov | Что в ответе и процитированные адреса |
|---|---|---|---|
| A1: What is Vargov Design? founder, awards, showroom, dealers (EN) | Google AI Mode | да | верно: основатель, «25 to 26 international jury awards», шоурум в Москве и три официальных дилера (как на /en/official-dealers). Адреса: vargov.ru/en/designer, /en, /awards, /about, /faq, /showroom, /en/official-dealers, /en/projects, /en/journal/russian-lighting-design; также online.gefera.ru (каталог Interlight 2025), threads.com, design.museaward.com |
| A2: Vargov Design awards — list them (EN) | Google AI Mode | да | «over 25»; MUSE 2026/2023, NYPDA 2026/2023, EPDA 2026/2023, IDA, LIT, LOOP, ADC, London, BLT, SIT, Awwwards Nominee 2026, Interlight 2022, ADD — всё есть в [[awards-verified]]; SIT назван только за 2023 (есть и 2025). Адреса: vargov.ru/awards, /en/awards, /about, /en/journal/epda-2026, /en/journal/loop-2025, /en/journal/russian-lighting-design, /journal/vysokoe-zhyuri; nydesignawards.com, idesignawards.com, ad-c.org, loopdesignawards.com |
| A3: Where are Vargov Design pieces produced? (EN) | Google AI Mode | да | **ОШИБКА: «own full-cycle factory located in China»** — единственный источник утверждения: online.gefera.ru/eng/info/IL25/catalog/… (карточка участника Interlight 2025 у Gefera Media). Прочие адреса: vargov.ru/en/official-dealers, /en/projects |
| A4: Кто такой Антон Варгов? (RU) | Google AI Mode | да | верно: основатель, Product Designer of the Year 2023, MUSE 2026, жюри ADD Awards. Адреса: vargov.ru/about, /designer, /journal/vysokoe-zhyuri; xprojectlight.ru/cat/vargov.html, facebook.com, instagram.com |
| A5: Есть ли 3D-конфигуратор и что он выдаёт? (RU) | Google AI Mode | да | верно: IFC4, PDF-спецификация, тендерный лист, ссылка на проект, монтажная схема 1:1; DXF не упомянут. Адреса: vargov.ru/configurator, **vargov.ru/configurator/ifc4**, vargov.design, instagram.com |
| Контроль: Do Vargov Design compositions support DALI? (EN) | Google AI Mode | да | «Yes… support DALI dimming» плюс фазовое диммирование, G4, mini LED, IFC4 — верно (подтверждено владельцем 15.10); упомянуто ещё «optical fiber» — не сверялось. Адреса: vargov.ru/en, /en/decorative, vargov.design, mbtm.ru (PDF), instagram.com |
| B1: лучшие бренды авторского освещения, двусветный холл (RU) | Google AI Mode | нет | Lasvit, Ochre, Boca do Lobo, Apparatus, Christopher Boots, Henge; ссылки не показаны |
| B2: award-winning studios, bespoke sculptural glass, double-height / hotel lobbies (EN) | Google AI Mode | нет | Lasvit, Preciosa, WonderGlass, Nikolas Weinstein, Rocco Borghese; clartes.com, galeriemagazine.com, roccoborghese.com, nikolas.net, kolektiv.cz |
| B3: best bespoke lighting studios, custom sculptural chandelier, worldwide (EN) | Google AI Mode | нет | Lasvit, Bocci, Christopher Boots; ссылки не показаны |
| B4: collectible lighting studios that produce a 3D model before making (EN) | Google AI Mode | **да, 3-м** | Rollo Studio, MIOS, **Vargov®Design** («thousands of free 3D models… visualize… prior to production»), Lightinup, Lumina Forge AI, Rarify x Gantri. Наш адрес: **vargov.ru/en** |
| B5: interior designer in Dubai, studios with showroom/dealer in Dubai (EN) | Google AI Mode | нет | Bespoke Lighting, Huda Lighting, Occhio (карточки карт) |
| B6: скульптурные люстры на заказ, 3D-модель до изготовления (RU) | Google AI Mode | нет | CustomLustra, SVETHOLL, ТТК Свет, 2К Светомастерская; customlustra.ru, svetholl.ru, ttclight.ru, 2klw.ru |
| B7: custom light installation for a hotel lobby, shortlist (EN) | Google AI Mode | нет | Studio Drift, teamLab, Serip, Ochre, Glass Masters; ссылки не показаны |
| C1: … sculptural glass lighting, include Russia and Eastern Europe (EN) | Google AI Mode | нет | Glassburg, Fresh Glass, SK-Glass, Lasvit, Expolight, Sans Souci, Zavadski Atelier; glassburg.com, fresh-glass.ru, sk-glass.ru, zavadski.co |
| C2: кто в Москве делает световые инсталляции в лестничный проём (RU) | Google AI Mode | нет | InsertDesign, Graphicson House, Zodiak Свет, LedexPro, LIGHT HOUSE; profi.ru, uslugi.yandex.ru |
| E1: online lighting configurator that exports IFC for architects (EN) | Google AI Mode | **да, первым** | «Yes, VargovDesign offers… configurator built to export IFC4 models»; PDF-спецификация, тендерный лист; дальше DIALux, RELUX. Адреса: **vargov.ru/en/configurator, vargov.ru/en/configurator/ifc4**. 15.10 — нет |
| E2: конфигуратор с выгрузкой IFC для Revit/ArchiCAD (RU) | Google AI Mode | **да, единственный** | «инструмент от российской премиальной светотехнической компании Vargov Design»; IFC4, PDF, тендерный лист; Arlight, Центрсвет, Donolux — только как контраст. Адрес: **vargov.ru/configurator/ifc4** |
| A1: Что такое Vargov Design? основатель, награды, шоурум, дилеры (RU) | Алиса AI | да | верно: основатель, «около 605 артикулов», первые работы 2018, «около 25 международных наград» (с 19.10 их 26 — индекс не догнал), список премий из [[awards-verified]]. Адреса: vargov.ru (+3), maps.yandex.ru |
| B1 (RU) | Алиса AI | нет | Dio D'Arte и др.; pro-luce.ru, lustrazdes.ru, lucterra.ru, sferon.ru, 3000k.ru |
| B6 (RU) | Алиса AI | **да, 4-м из 4** | SVETHOLL, O-Luce, ImperiumLoft, **Vargov®Design** («арт-объект с акцентом на скульптурность»). Адрес: vargov.ru |
| C2 (RU) | Алиса AI | нет | СитиЛайт, InsertDesign и др.; ct-light.ru, insertdesign.ru, i-rembrand.ru, growzone.ru. **22.09 — было «да»** |
| E2 (RU) | Алиса AI | **да, первым** | «Такой инструмент действительно есть — это конфигуратор от Vargov®Design»; кнопка «Документы», три файла. Адреса: vargov.ru (+2) |

Ни в одном ответе не процитированы huggingface.co, medium.com, github.com, wikidata.org. Год основания «2022» не прозвучал ни разу.

### Итог по блокам

| Блок | Google AI Mode | Алиса AI | Perplexity / Duck.ai |
|---|---|---|---|
| A — о бренде | 5 из 5 названы; 1 грубая ошибка (A3, Китай) | 1 из 1, без ошибок | не сняты |
| B — категория без региона | **1 из 7** (B4) | 1 из 2 (B6) | не сняты |
| C — с регионом | 0 из 2 | 0 из 1 | не сняты |
| E — IFC4 | **2 из 2** | 1 из 1 | не сняты |
| DALI (контроль) | да, верно | — | — |

Цели к 22.10 из [[ai-probe-set]]: блок B «≥ 1 из 7» — **выполнена у Google AI Mode и у Алисы**; блок E «≥ 1 из 2» — **выполнена у Google AI Mode (2 из 2) и у Алисы**.

### Сравнение с 22.09 и 15.10

- **Google AI Mode:** 22.09 — 0 из 1 по категории, 15.10 — 0 из 2 (B2, E1), сейчас — 3 из 11 (B4, E1, E2). Главный сдвиг — ниша IFC4: страница /configurator/ifc4 теперь прямой источник ответа и в EN, и в RU.
- **Perplexity:** 15.10 — 2 из 3 (B2, E1 первым); 22.09 — C1 первым. Сейчас без входа не отвечает — сравнить нельзя.
- **Алиса:** 22.09 — C2 да; сейчас C2 нет (откат), но появились B6 и E2.
- **Ошибка о стране производства** держится с 22.09: тогда — со ссылкой на International Design Awards, сейчас — на каталог Interlight 2025 у Gefera Media (online.gefera.ru, IL25). Источник новый — нужна правка карточки участника у организатора.
- Число наград: Google «25 to 26», Алиса «около 25»; верное — 26 (`awardsCount()`, с 19.10).

### Прочие показатели на 24.10

- **Google Search Console → «Функции на основе генеративного ИИ» (бета), sc-domain:vargov.ru, 26.07–22.10:** 2,32 тыс. показов, 743 страницы
  (точка 26.07–12.10: 1,8 тыс., 617). Больше всего: / (528), /en (259), /lighting (135), /journal/sertifikat-podlinnosti (101), /catalog (90).
  **Страницы /for появились:** 29 показов, 11 страниц за весь период, из них **16 показов за 16–22.10** (после выкладки 15.10):
  /en/for/atrium 5, /en/for/hotel-lobby 3, /for/double-height 3, /for/hotel-lobby 3. **/configurator/ifc4 — 0 показов**, хотя AI Mode цитирует его в E1 и E2 (отчёт отстаёт или такие ответы туда не попадают).
- Bing AI Performance — не снят (нет входа).
- Hugging Face `vargov-design-catalog`: **1948 скачиваний** за 30 дней (15.10 — 1712, 02.10 — 463), лайков 0.
- Wikidata Q141301076: P166 — 2, описаний — 10, меток — 7 (без изменений с 15.10).
- GitHub vargov-ai-kb: 0 звёзд, 0 форков.
- Журнал сервера и Метрика «Из ИИ» в этой точке не снимались.

---

## 2026-10-15 (промежуточная точка: пробы ассистентов)

Снято 15.10.2026, 02:38–02:45 UTC, браузер владельца, без входа в Perplexity; Google AI Mode — `udm=50&hl=en`.
Вопросы — из [[ai-probe-set]] (блоки B и E), дословно. Это не полный замер: полный — 22.10.

| Вопрос | Ассистент | Vargov | Что в ответе |
|---|---|---|---|
| B2: award-winning studios, bespoke sculptural glass lighting, double-height / hotel lobbies (EN) | Perplexity | **да, первым** | «Vargov Design — bespoke sculptural luminaires…», EPDA названа; источник vargov.ru; дальше Shakúff, Illuminata, Shimale Peleg. 22.09 на тот же вопрос — нет |
| B3: best bespoke lighting studios, custom sculptural chandelier, double-height, worldwide (EN) | Perplexity | нет | Lindsey Adelman, Willowlamp, Shakúff, Lightart |
| E1: online lighting configurator that exports IFC for architects (EN) | Perplexity | **да, первым** | «Yes. Vargov® Design is an online 3D configurator… exports an IFC4 model»; PDF-спецификация, лист закупки, ссылка; DIALux — как альтернатива. 27.09 — 0 из 2 |
| B2 (тот же) | Google AI Mode | нет | Lasvit, Shakúff…; galeriemagazine.com |
| E1 (тот же) | Google AI Mode | нет | VividWorks, DIALux и пр. |

Итог: Perplexity — 2 из 3 (цель блоков B и E к 22.10 — «≥ 1» — у Perplexity уже выполнена); Google AI Mode — 0 из 2.
Прочие показатели на 15.10: Hugging Face `vargov-design-catalog` — 1712 скачиваний за 30 дней (02.10 — 463);
Wikidata Q141301076 — P166 2, описаний 10, меток 7; GitHub vargov-ai-kb — 0 звёзд.
Не снималось: Duck.ai (GPT), Яндекс Алиса, журнал сервера и Метрика «Из ИИ» — в полном замере 22.10.

---

## 2026-10-03

Внеочередная точка вместо планового прогона: задача `vargov-ai-serp-monthly` 01–02.10 четыре раза
подряд завершилась без результата, замер снят вручную 03.10 05:30–05:36 UTC пятью агентами.
**Метод — веб-поиск (WebSearch, выдача США)**, как в точках 09.09 и 17.09 этого журнала; базовые
значения 22.09 из [[ai-visibility-global-2026-09-22]] снимались у ассистентов (Duck.ai, GPT, Google
AI Mode, Perplexity, Алиса) — это другой метод, поэтому блок C с ними напрямую не сравнивается.
Второй движок (DuckDuckGo html) на всех запросах отдал CAPTCHA, обходить не стали — вся картина
с одного движка. Четыре контрольных запроса «Vargov Design awards» положительные (бренд в 8–10
ссылках из 10), значит нули ниже настоящие, а не сбой поиска. Два русских запроса блока B (1 и 6)
в этот прогон не вошли — только шесть английских; следующий замер 22.10 снимать по полному набору
[[ai-probe-set]] и у ассистентов.

| Блок | Результат | Кого выдают вместо бренда |
|---|---|---|
| A — о бренде, 5 запросов | **5 из 5**. HF-датасет первый в 4 из 5; из брендовых адресов показаны только HF, vargov.design (старые Tilda-страницы и /tpost), vargov.ru/en и YouTube; configurator.vargov.ru, GitHub, Medium, LinkedIn, Wikidata не появились ни разу | по «Anton Vargov» рядом Victoria Yakusha и Svitlana Antonovych из Википедии |
| B — категория без региона, 6 запросов (+6 вариантов) | **0 из 6**. Единственное попадание — вариант со словами «3D configurator»: vargov.design на 5-м месте, с русским заголовком в английской выдаче | Shakúff, Cinimod, Cuslux, LightArt, Willow Lamp, Blackcanvas, Hammerton; Дубай — Rocco Borghese, BOLD Bespoke, Antonovich Group |
| C — категория с регионом, 2 запроса (+2 варианта) | **0 из 2** | EN: Blurries (Прага), Studio Lloyd, Shakúff — ни одной российской студии; RU: Яндекс Услуги, VikArtGlass, Art-Puls, Магналюкс — «световая композиция» уводит выдачу в фасадный и новогодний декор |
| E — IFC4, 2 запроса (+2 варианта) | **0 из 2** | DIALux, LAMILUX, ARCHLine.XP, LIGMAN, ARCAT, справки Graphisoft и Autodesk; RU — bimlib.pro, openbim.ru, tangl.cloud |

Ошибки о бренде в сводках движка и их источники:

- «23 design awards» — во всех четырёх контролях. Источник найден: био на
  wescover.com/creator/vargov-design (написано 09.09, когда наград было 23). HF-карточка и
  профиль productdesignaward.eu уже говорят 25. Владелец 03.10 решил био Wescover не править
  («забей на Wescover») — число 23 там остаётся; в следующих замерах это известный источник, не новая находка.
- фраза об «exclusive Vargov®Design factory» с названием страны и почтовым адресом — старая Tilda-страница
  `vargov.design/branded_products_vargovdesign` всё ещё в индексе; редиректы от 02.10 до индекса
  не дошли. Проверить 22.10, при повторе — просить удаление из индекса через Search Console.
- «founded in 2022» — год регистрации знака выдан за основание; страница-источник не найдена.
  На сайте и в Wikidata — «первые работы — 2018».
- Счётчики «495 / 341 / 154 / 371» — сниппет vargov.design от прежней версии шапки.
- Движок по запросу о конфигураторе сам не знает, что он выдаёт: IFC4, PDF и ссылка не
  названы, страница /configurator/ifc4 и статья Medium (01.10) в индекс ещё не попали.
- **Не ошибки** (агенты пометили как «не подтверждено», но они в [[awards-verified]]):
  MUSE Design Awards 2026 Gold за «Oceanic Illumination» (№ 1, подтверждено 04.09) и
  Awwwards Nominee 2026 за конфигуратор.

К проверке отдельно: cgtrader.com — три модели под именем «Vargov Design» и
3dsky.org/…/droplight_vargov_design_117 (3dsky — зарубежное зеркало 3ddd, свои загрузки; CGTrader —
чьи, неизвестно). ~~romedesignawards.com/our-judge.php — связь с брендом не подтверждена~~ — **исправлено 03.10.2026:**
это подтверждённая страница жюри IAA (карточка «Vargov Anton · CEO, Vargov Design»), одна из пяти, внесённых 07.09;
раздел в [[external-references]] был случайно удалён 07.09 (9b8641f) и восстановлен 03.10.

Вывод тот же, что 17.09: по имени — находится полностью, по категории и по нише IFC4 — ноль.
Что изменилось: HF-датасет стал первым брендовым адресом в выдаче (четыре запроса из пяти),
а «23 награды» теперь имеют один установленный источник, который можно поправить.

## 2026-09-17

Полный замер по пяти вопросам агента сайта — [[ai-visibility-zamer-2026-09-17]]. Коротко: переходов из ИИ 52 за 18.08–17.09 (chatgpt 33 по метке + 15 по рефереру, perplexity 3, gemini 1); подлинных обходов за 14 суток — GPTBot 6 374, ClaudeBot 5 459, PerplexityBot 2 154; по имени бренд называют 5 из 5, по категории 0 из 5; без веб-поиска модели о бренде не знают ничего.

## 2026-09-09

Внеплановый замер по просьбе владельца. База для сравнения — сентябрьский аудит: по всем
категорийным запросам бренда не было, единственная ниша с присутствием — «Russian lighting design
brand sculptural», vargov.ru/en на 7-й позиции.

| Запрос | Кто выдаётся | Vargov | Что кормит выдачу |
|---|---|---|---|
| best luxury designer lighting brands | Baccarat, Schonbek, Tom Dixon, Flos, Moooi, Kelly Wearstler, Gubi, Haberdashery, Villa Lumi, Pieter Adam | нет | residencesupply.com, lovehappensmag.com, rclite.com, designersmk.com, luxdeco.com — сплошь SEO-блоги магазинов |
| sculptural chandeliers designer brands | Noé Duchaufour-Lawrance × Saint-Louis, Liaigre, Hammerton, Sonneman, Slamp, Ango, Brokis | нет | **galeriemagazine.com «7 Sculptural Lighting Options» — первый результат**, seuslighting.com, casadesigngroup.com |
| collectible lighting design studios | Lindsey Adelman, Workstead, Atelier de Troupe, O'Lampia, Sonneman, Studio Eberwein | нет | design-milk.com, architizer.com, incollect.com, dexigner.com |
| Russian lighting design brand sculptural | 1stDibs, Adorno, Artemest, Victoria Yakusha | **есть, 7-я позиция** | vargov.ru/en; модель называет бренд прямо в ответе и описывает верно |
| award-winning sculptural lighting designer | Lindsey Adelman, Rosie Li, Coil + Drift, Erin Lorek, INDO- | нет | dwell.com, **azuremagazine.com «5 Sculptural Lighting Fixtures That Marry Light and Form»**, cnn.com, три материала dezeen.com про ICFF Look Book |
| дизайнерские световые композиции премиум бренд | Odeon Light, Maytoni, Lightstar, Marset, Vistosi, DCW Editions | нет | lampadia.ru, plushdesign.ru, lab-des.com, bollu.ru — магазины, не редакции |
| Anton Vargov lighting designer | — | **есть, находится полностью** | idesignawards.com, ad-c.org, **iconic-world.com**, nydesignawards.com, vargov.design, YouTube, Instagram, vargov.ru/en |

### Что изменилось с прошлого замера

По категориям — ничего. Бренда по-прежнему нет ни в одном ответе, и состав тех, кого называют
вместо него, тот же. Единственная ниша с присутствием — та же самая, на той же позиции.

Но замер вскрыл то, чего в прошлый раз не увидели.

### Профиль ICONIC отравляет ответы о бренде — подтверждено дословно

На запрос «Anton Vargov lighting designer» языковая модель отвечает, среди прочего:

> фраза о производственных мощностях компании с названием страны и о доставке по всему миру
> (дословная цитата — в приватной папке `scan/`: в открытой базе её не держим, она сама называет страну)

Источник этой фразы — профиль `iconic-world.com/directory/anton-vargov`. Проверено 09.09.2026:

- старый адрес отдаёт **301** на `https://www.iconic-awards.comdirectory/anton-vargov` — редирект
  собран с ошибкой и теряет слэш, поэтому ведёт в никуда;
- правильный адрес `https://www.iconic-awards.com/directory/anton-vargov` отдаёт **404**.

То есть страницы больше нет, а её текст остался в индексе и продолжает подаваться как факт о
бренде. Это та же фраза со страной производства, что была в статье D5 MAG, — но здесь она звучит не в статье, а в прямом ответе на вопрос «кто такой Антон Варгов».

**Следствие для письма в German Design Council:** просить надо не исправление текста, а удаление
мёртвого профиля из поисковых индексов. Исправлять там уже нечего — страницы нет. Письмо
отправлено 07.09, ответа нет; при напоминании 18.09 этот довод нужно привести дословно, вместе
с обоими кодами ответа.

### Два адресата, которые видно прямо в выдаче

Оба уже получили от нас питчи 08.09 и оба ранжируются по нашим целевым запросам — то есть попадание
в них меняет не только охват, но и сам ответ модели:

- **galeriemagazine.com**, «7 Sculptural Lighting Options That Instantly Transform a Space» —
  первый результат по «sculptural chandeliers designer brands»;
- **azuremagazine.com**, «5 Sculptural Lighting Fixtures That Marry Light and Form» — в выдаче по
  «award-winning sculptural lighting designer».

Третий по важности — **dezeen.com**: три разных материала про ICFF Look Book в выдаче по одному
запросу. Look Book — это ежегодная подборка дизайнеров освещения, и попадание в неё даёт сразу
несколько ранжирующихся страниц.

### Наблюдение о том, кто пишет категорийные списки

По англоязычным категорийным запросам выдачу держат не редакции, а SEO-блоги магазинов
(residencesupply, rclite, lovehappensmag, designersmk). По русским — то же самое, только магазины
российские. Это значит, что путь в категорийный ответ идёт двумя разными дорогами: редакционной
(Galerie, Azure, Dezeen, Dwell) и товарной (попасть в каталог площадки, чей блог ранжируется).
Вторая дорога до сих пор не рассматривалась вовсе.
