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
поимённо. Снимать в счётчике 111091941 (вход — рабочий аккаунт владельца) отчётом
`/stat/sources?id=111091941&period=month` с группировкой «UTM Source», плюс тот же отчёт
с группировкой «Домен реферера» — часть переходов приходит без метки. Считаются
`chatgpt.com`, `perplexity.ai`, `gemini.google.com`, `copilot.microsoft.com`.

База, 11 августа — 10 сентября 2026: **chatgpt.com — 18 визитов по метке и 10 по рефереру,
глубина 5,22, время 3 м 27 с; gemini.google.com — 1; perplexity.ai — 1.** Для сравнения,
Instagram за тот же месяц — 15 визитов при глубине 2,67. То есть ответы ИИ уже приводят
на сайт не меньше людей, чем соцсеть, и людей более заинтересованных. Это первая
измеримая связь между этой работой и сеансами; подробности — `traffic-utm-2026-09.md`.

---

## 2026-11-02 (плановый прогон `vargov-ai-serp-monthly`)

Снято 02.11.2026 автоматическим прогоном, без человека. Выдача — WebSearch (выдача США), 10 запросов из 10,
по одному вызову, без повторов. Обращений к vargov.ru — ноль. Раздел вставлен сверху, как и прежние:
журнал ведётся от новых к старым, хотя в задаче написано «в конец».

| Запрос | Кто выдаётся | Vargov | Источники |
|---|---|---|---|
| best luxury designer lighting brands | Visual Comfort, FLOS, Baccarat, Sonneman, Tom Dixon, Corbett, Arhaus, Louis Poulsen, Artemide, Lindsey Adelman | нет | yahoo.com/aol.com «18 Luxury Lighting Brands», residencesupply.com, archute.com/high-end-lighting-brands, rclite.com, interiorinsider.com (серия «brands like …») |
| sculptural chandeliers designer brands | Brand van Egmond, Visual Comfort Signature, 101 Copenhagen, Martinelli Luce, Barratt & Maxine | нет | dezeen.com (Bella, Brand van Egmond), hoog.design (четыре страницы о Brand van Egmond), luxe.outlookindia.com, lightingnewyork.com, 1stdibs.com |
| collectible lighting design studios | Lambert & Fils, In Common With, Lindsey Adelman, Studio Lampent, klove Studio, Evokar | нет | scp.co.uk, dezeen.com/2020/03/12/collectible-2020-lighting, indiadesignid.com, designwanted.com, surfacemag.com |
| custom art lighting installations brands | Brand van Egmond, Sogani, Fine Art Handcrafted Lighting, Alan Mizrahi, O'Neill Illuminates, Gabriel Scott | нет | brandvanegmond.com/customised, architizer.com/blog/practice/materials/luminaires-as-art, theinteriorsaddict.com, interiorinsider.com |
| дизайнерские световые композиции премиум бренд | LOFT IT, Lightstar, GALAKTIKA (SWG), Premium Lamps, Huda Lighting, klove | нет | каталоги PDF (mosplitka.ru, vamsvet.ru, eurosvet.ru, swgshop.ru), companies.rbc.ru |
| авторские люстры на заказ бренд | Brand van Egmond, Bec Brittain, Luminaire Authentik, Aggio Light, Aqua Creations, Brokis | нет | lampadario.ru/fabrics/bec-brittain, luminaire.com/ru, everythingbutordinary.co.uk, artemest.com |
| Russian lighting design brand sculptural | GORKOVENKO (Grigorii Gorkovenko), Emelianova Studio, Kuzma Kuznetsov (ZAHA LIGHT), Bezhko, Гармония Света | **нет** (в 09.2026 — 7-я позиция) | 1stdibs.com (семь карточек Gorkovenko), galerie-philia.com, archilovers.com, zeelproject.com, brabbu.com |
| award-winning sculptural lighting designer | Michael Anastassiades, Lindsey Adelman, Niamh Barry, Bec Brittain, Willowlamp, Cole Gerst | нет | galeriemagazine.com «7 Sculptural Lighting Options» (две ссылки), litawards.com, incollect.com, dwell.com, competition.adesignaward.com |
| MUSE Design Awards lighting winner | Michael Grubb Studio, Lighting Design International, Inhabit, Blass Nova, DuraGreen | нет | michaelgrubbstudio.com, lightingdesigninternational.com, madeinbritain.org, interempresas.net, designers.org |
| Anton Vargov lighting | **Vargov®Design — первым** | **есть, 1–7-я ссылки** | d5mag.com (две), ad-c.org (две: Platinum и Gold 2023), loopdesignawards.com, nydesignawards.com, idesignawards.com |

### Что изменилось с прошлого замера

- **Единственная ниша с присутствием пропала.** «Russian lighting design brand sculptural» — в 09.2026 vargov.ru/en
  был 7-м, теперь его нет. Выдачу заняли 1stdibs (семь карточек GORKOVENKO) и архитектурные каталоги. Возможно,
  дело в разбросе выдачи, а не в провале: по одному прогону этого не различить. Если в декабре бренда снова не будет,
  это уже тенденция.
- По категориям, как и 09.09 и 03.10, — **0 из 9**. Новый общий лидер EN-выдачи — **Brand van Egmond**: три запроса из
  четырёх категорийных, плюс русский «авторские люстры на заказ». Это ближайший к нам по сути бренд (ручная работа,
  световые скульптуры, заказ), и его выдачу кормят hoog.design, dezeen.com, theinteriorsaddict.com и его собственный сайт.
- Источники: interiorinsider.com (серия «N brands like X») появился в двух запросах. Galerie («7 Sculptural Lighting
  Options») держится — теперь по «award-winning sculptural lighting designer». azuremagazine.com в выдаче больше нет.
  Магазинные SEO-блоги (residencesupply, rclite) никуда не делись.
- По имени: выдача теперь начинается с **d5mag.com**, а не с HF-датасета, как было 03.10. В сводке движка
  сайтом бренда назван **vargov.design**, а не vargov.ru. Фраза о стране производства по-прежнему приходит из
  d5mag (дословно — только в приватной `scan/`).
- В брендовой выдаче — **MUSE ни разу**: по «MUSE Design Awards lighting winner» о нас нет ни одной страницы,
  хотя MUSE 2026 Gold и 2023 у бренда есть.

### Переходы из ИИ (Метрика 111091941)

Прогон данных не снял: отчёт `/stat/sources?id=111091941&period=month` во встроенном браузере ушёл на
passport.yandex.ru — входа под info@vargov.ru там нет, а вводить пароль прогон не вправе (первый прогон во
встроенном браузере, а не в Chrome владельца). **Дописано 02.11 вручную** в Chrome владельца (вход
info@vargov.ru есть): «Источники, сводка», период 01.10–31.10.2026, без семплирования, сохранённые сегменты.

| Сегмент | Визиты | Посетители | Отказы | Глубина | Время |
|---|---|---|---|---|---|
| «Из ИИ · реферер» (1008101534) | 3 | 2 | 33,3 % | 3,33 | 2 мин 40 с |
| «Из ИИ · UTM» (1008101546) | 20 | 19 | 5,0 % | 3,35 | 1 мин 59 с |

Всего визитов за октябрь — 5 238. Один визит (переход по ссылке, 2 мин 40 с) есть в обоих сегментах, так что
из ИИ за октябрь около **22 визитов**. В UTM-сегменте 19 визитов из 20 Метрика относит к «прямым заходам»: ссылку
с меткой ассистента открыли без реферера. Разбивку по ассистентам (chatgpt / perplexity / gemini) не снимал —
для неё нужна группировка «UTM Source» в интерфейсе. База для сравнения: 17.09 за 30 дней — 16 (реферер) и 32
(UTM); 18.08–17.09 — 52 перехода всего. Октябрь ниже обеих точек. Эти цифры — до выхода фильма (02.11), то есть
вторая часть точки отсчёта T0 кампании.

### Обращения краулеров

Запрос агенту сайта (сессия «vargov.ru») отправлен 02.11: вывод `crawler-report.sh` за 01–31.10, оба журнала,
раздел «1б» по маскам CIDR, коды ответов, ChatGPT-User своих — отдельной строкой. На момент записи прогона ответа
не было. **Дописано 02.11 по ответу агента сайта** (срез снят 13:25 UTC, только строки «/Oct/2026:»; журнал
vargov.ru — весь октябрь, 01.10–31.10; общий журнал — только 19.10–31.10, раньше копий нет).

Свои — адрес попадает в маску CIDR из списка владельца подписи (openai.com, claude.com, perplexity.ai), чужие —
нет. Строки журнала, октябрь 2026:

| Обходчик | Всего | Свои | Свои: коды | Чужие: коды |
|---|---|---|---|---|
| GPTBot | 4361 | 4255 (98 %) | 200:4156, 301:93, 404:3, 503:2 | 404:93, 429:4, 500:4 |
| OAI-SearchBot | 2477 | 2348 (95 %) | 200:2280, 301:67, 503:1 | 404:109, 429:6, 500:4 |
| ChatGPT-User | 632 | **515** (81 %) | **200:502**, 301:12, 499:1 | 404:102, 429:3, 500:2 |
| ClaudeBot | 7675 | 7574 (99 %) | 200:7467, 301:106, 404:1 | 404:92, 429:2 |
| Claude-User | 355 | 52 (15 %) | 200:47, 301:5 | 200:191, 404:95 |
| Claude-SearchBot | 104 | 0 | — | 404:94 |
| PerplexityBot | 1214 | **1100** (91 %) | **200:1067**, 301:33 | 404:99, 429:3 |
| Perplexity-User | 108 | 0 | — | 404:101, 429:4 |

Без проверки по адресу (списков нет): Googlebot 8655 (200:7017), bingbot 11364 (200:11018), YandexBot 11010
(200:10789), Applebot 829, Google-Extended 33 (все 404), meta-externalagent 539159 (200:517021). Всего строк
1 419 536, из них vargov.ru 1 321 104; кодов 429 за месяц — 4732.

- **Отказов настоящим обходчикам ИИ нет:** у своих адресов OpenAI, Anthropic и Perplexity за октябрь ни одного 403
  и ни одного 429. Все 429 и почти все 404 под этими именами — сканеры с арендованных адресов (34.81.69.18,
  35.243.75.227, 34.24.212.235 и др.), которые прикидываются ботами.
- **ChatGPT-User — 515 заходов со своих адресов, 502 с ответом 200.** Это не обход, а чтение страниц по запросу
  пользователя ChatGPT в моменте; база для сравнения после запуска фильма 02.11.
- **meta-externalagent — 539 тысяч строк, 41 % всего журнала vargov.ru.** Это обходчик Meta для обучения ИИ.
- **Снимки:** журнал `img.log` отсутствует, учёт /img/ выключен; /_next/image — 1087 обращений.

**Поправка к записи 24.10 о Perplexity (ниже, раздел 2026-10-24): вывод неверен.** Тогда по журналам за 11–24.10
вышло «PerplexityBot за 14 суток — один запрос, /robots.txt конфигуратора» и «за двое суток ClaudeBot 64, Googlebot
54». Агент сайта 02.11 подтвердил: 24.10 читались только общие `access.log`, `access.log.1` и `access.log.*.gz`
ручными grep, а журнал самого сайта `vargov.ru.access*` (vargov.ru пишет туда с 17.09) не открывался.
Пересчёт 02.11 13:57 UTC по обоим журналам (vargov.ru.access* — 539 688 строк за 11–24.10; общий хранится
14 суток и есть только с 19.10), свой/чужой — по 13 адресам из perplexity.ai/perplexitybot.json:

- **PerplexityBot со своих адресов на vargov.ru — 271 строка за 11–24.10**, коды 200:255 и 301:16, ни одного
  403, 429 или 5xx; чужих под той же подписью — 56 (404:45). По дням, свои/чужие: 11.10 2/0 · 13.10 20/0 ·
  14.10 3/0 · 15.10 36/0 · 16.10 3/0 · 17.10 0/5 · 18.10 5/25 · 19.10 0/20 · 21.10 198/1 · 22.10 2/0 ·
  24.10 2/5 (12, 20 и 23.10 — ни одной строки).
- **Конфигуратор он читал** — пять заходов со своих адресов, все 200: 15.10 13:56 `/en/configurator/ifc4`,
  16.10 08:33 `/configurator/ifc4`, 21.10 03:43 `/en/configurator/ifc4`, 21.10 06:36 `/configurator/ifc4`,
  21.10 14:38 `/en/configurator` (последний). С 21.10 14:38 до конца 24.10 — ни одного захода на конфигуратор.
- Правка /configurator ушла на бой 24.10 в 16:31 UTC, поэтому ответ Perplexity 24.10 про «DXF, PDF, MAX, FBX»
  собран со снимка не позднее 21.10. Верной была первая гипотеза записи 24.10 — дело в возрасте снимка, а не в
  том, что Perplexity нас не читает. Его можно и нужно использовать как измеритель правок, учитывая задержку.
- Полные сутки 23–24.10, строки vargov.ru / общий журнал: ClaudeBot 3102 / 76, Googlebot 616 / 63, bingbot
  364 / 31, GPTBot 14 / 4, PerplexityBot 7 / 0 (подписи без проверки по адресу, кроме PerplexityBot). Названные
  тогда 64 / 54 / 25 / 3 — только часть общего журнала.

Урок: счёт обходчиков — только по обоим наборам файлов (`vargov.ru.access*` и `access.log*`), с названием
прочитанных файлов и их границ в ответе; `crawler-report.sh` читает оба.

**Что PerplexityBot читал после правки 24.10** (срез агента сайта 02.11 14:29 UTC, vargov.ru.access*, только свои
адреса по perplexitybot.json, журнал до 02.11 14:28 UTC): за 25.10–02.11 своих строк 105 (26.10 — 19, 27.10 — 32,
28.10 — 7, 29.10 — 3, 31.10 — 8, 01.11 — 31, 02.11 — 5). Из конфигуратора — только `/en/configurator/ifc4`,
31.10 02:46 и 01.11 11:48 UTC, оба 200. Правленую `/en/configurator` (на бою 24.10 16:31 UTC) и `/configurator`
он с 21.10 14:38 не перечитывал — больше 8 суток 22 часов. Для `/en/configurator/ifc4` (заголовок с IFC4 на бою
24.10 ~16:40 UTC) первое чтение после правки — через ~6 суток 10 часов.

### Пробы Perplexity, блок E (02.11.2026, ~14:30 UTC)

Chrome владельца, perplexity.ai/search?q=…, бесплатная модель, аккаунт владельца с историей прошлых проб (в
боковой панели те же вопросы — возможна поправка на историю, проверить в чистом окне при следующем замере).

| Вопрос | Vargov | Что в ответе | Источник Vargov |
|---|---|---|---|
| E1 (EN, дословно из [[ai-probe-set]]) | **назван первым, верно** | «Yes. Vargov®Design offers exactly that: … exports the assembled composition as an IFC4 model … alongside a PDF specification and tender sheet»; IfcLightFixture / IfcFurnishingElement, высота потолка перед выгрузкой; вторым — DIALux evo Pro | vargov.ru/configurator/ifc4 |
| E2 (RU, дословно) | **назван первым, верно** | «под ваше описание точнее всего подходит Vargov®Design … самостоятельная выгрузка IFC4, PDF-спецификации и тендерного листа»; в таблице — «полное совпадение»; дальше IEK, Ledel, Fereks, Arlight как «не то же самое» | vargov.ru/configurator/ifc4 |

**Блок E — 2 из 2** (27.09 — 0 из 2, 24.10 — E1 назван с ошибкой «not IFC», E2 — нет). Ошибка «DXF, PDF, MAX, FBX —
not IFC» исчезла. Но задержкой правки это не измерить: Perplexity теперь берёт не правленую `/en/configurator`, а
русскую `/configurator/ifc4`, которую его обходчик последний раз читал 21.10 06:36 — ещё до правки, и IFC4 на ней
был всегда. Изменился выбор страницы-источника, а не её снимок. Вопрос «через сколько суток Perplexity видит
правку» остаётся открытым до первого чтения `/en/configurator` после 24.10.

**Ошибка числа в E2.** Perplexity пишет, что с IFC4 «полностью рассчитываются и выгружаются 2 360 из 6 050
композиций». На странице — «360 из 605» (сборочные: open-skus = 360, каталог = 605). Агент сайта нашёл причину:
номер шага «02» стоит отдельным span прямо перед числом, и в тексте без разметки выходит «02 360 из 605». Попросил
скрыть номера шагов от извлечения текста (aria-hidden или разделитель) на /configurator/ifc4 и похожих страницах;
после выкладки повторить E2. Урок для вёрстки: всё, что ИИ может прочитать подряд, проверять по `textContent`,
а не по виду страницы.

**Исправлено на бою 02.11 15:41 UTC** (сайт 4032a11): номер шага рисуется через `::before` с aria-hidden, цифр в
тексте HTML нет. По 358 страницам карты сайта склейка «номер шага + число» нашлась в четырёх местах, все
исправлены на всех языках: /configurator/ifc4 («02» + «360 из 605»), /in-stock ×8 («01» + «15–20 рабочих дней»),
/en/in-stock и /en/production («03»/«04» + «1:1»), /architects ×8 («03» + «3D и визуализация»). «6 050» на боевой
странице нет — это додумка Perplexity.
**Повтор E2 в 15:44 UTC:** Vargov первым, источник тот же; число теперь «2360 из 605» — склейка «02 360» ещё в
снимке Perplexity, «6 050» исчезло. Это чистая проверка задержки: правка 02.11 15:41 UTC, страница
/configurator/ifc4. Ждём первого чтения её PerplexityBot после правки (дату даст агент сайта) и повторяем E2.

### Официальный каталог MCP

`ru.vargov/vargov-design` 1.0.0 опубликован в registry.modelcontextprotocol.io 02.11.2026 15:43 UTC (агент сайта):
status active, isLatest, remote streamable-http `https://vargov.ru/api/mcp`, websiteUrl vargov.ru, описание
«Read-only MCP server with Vargov®Design public data: compositions, answers, configurator, dealers.»
Проверено мной GET `/v0.1/servers?search=ru.vargov` в 15:45 UTC. Домен подтверждён по HTTP
(`/.well-known/mcp-registry-auth` — 200). Каталог пока в режиме предпросмотра, по его документации данные могут
сбросить — проверять запись при каждом ежемесячном замере.

### Карточки на картах

Сверено **18 из 18**; совпадает 11, расходится 7 (из них в 3 случаях виден лишь один телефон из двух).
Дубль Яндекса 199433674369 по-прежнему ведёт на 102611426185 (canonical — 102611426185), пометки
«Больше не работает» нет — тревоги нет. Яндекс и Google прочитаны встроенным браузером: WebFetch на Яндексе
упирается в цепочку гео-редиректов yandex.ru → .eu → .com, у Google получает пустую оболочку. 2ГИС прочитан
через WebFetch: карточка настоящая, id 70000001110317147 в тексте есть. Дату обновления не отдаёт ни одна карточка:
у Яндекса стоит «Обновлено 17 сентября», но это блок товаров, у 2ГИС — «давно не обновляла данные».

| Карточка | Поле | На карте | Эталон | Совпадает |
|---|---|---|---|---|
| Яндекс | название | Vargov®Design | Vargov®Design | да |
| Яндекс | адрес | Нахимовский просп., 24, стр. 1 | …24, стр. 1, павильон 2, стенд 212, 117218 | **нет** — нет павильона и стенда |
| Яндекс | комментарий | «этаж 2» | павильон 2, стенд 212 | **нет** |
| Яндекс | телефоны | +7 (916) 537-33-52 | 916 и (925) 888-77-44 | **частично** — линии шоурума нет |
| Яндекс | часы | ежедневно 12:00–20:00 | 12:00–20:00 | да |
| Яндекс | сайт | vargov.ru | vargov.ru | да |
| Google | название | Vargov Design | Vargov Design | да |
| Google | адрес | Nakhimovskiy Ave, 24, стр. 1, павильон 2, стенд 212, Москва, 117218 | то же | да |
| Google | комментарий | отдельного нет, павильон и стенд стоят в адресе | павильон 2, стенд 212 | да |
| Google | телефоны | 8 (925) 888-77-44 | 916 и 925 | **частично** — номера бренда нет |
| Google | часы | 12:00–20:00 (видны пн–чт, пт–вс в окне не поместились) | 12:00–20:00 | да |
| Google | сайт | vargov.ru | vargov.ru | да |
| 2ГИС | название | Vargov®Design | Vargov®Design | да |
| 2ГИС | адрес | «Проспект Нахимовский, 24 пав3», 117218 | …павильон 2, стенд 212 | **нет** — «пав3» |
| 2ГИС | комментарий | «211, 212 стенд; 10D сектор; 2 павильон» | павильон 2, стенд 212 | да (но спорит с адресом) |
| 2ГИС | телефоны | +7 916 537-33-52 (в ссылке звонка) | 916 и 925 | **частично** — линии шоурума нет |
| 2ГИС | часы | ежедневно 10:00–20:00 | 12:00–20:00 | **нет** |
| 2ГИС | сайт | vargov.ru | vargov.ru | **да — исправлено** (03.10 стоял xprojectlight.ru) |

С 03.10 у 2ГИС изменились две вещи: сайт теперь vargov.ru, а часы стали 10:00–20:00 вместо 10:00–21:00.
Часы всё равно не совпадают с эталоном, и «пав3» в адресе остался.

---

## 2026-10-31 (внеплановая точка: пробы ассистентов, GSC, Bing)

Снято **31.10.2026, 14:45–15:10 UTC**, браузер владельца (Chrome). Метод и вопросы те же, что 22–24.10: Google AI Mode `udm=50&hl=en`; Алиса AI через вкладку в выдаче ya.ru, под учётной записью бренда; Perplexity под входом бренда.
Copilot не снят, нужен вход. Вместо него смотрим Bing AI Performance.

| Блок | Google AI Mode | Алиса AI | Perplexity |
|---|---|---|---|
| A — о бренде | 5 из 5 | 1 из 1 | — |
| B — категория без региона | **1 из 7** (B4, теперь **первым**; 24.10 был 3-м) | 0 из 2 (**B6 откатился**: 24.10 был 4-м) | — |
| E — IFC4 | **2 из 2, оба первым** | 1 из 1, первым | **E1: назван первым и верно** |

**Что изменилось с 24.10:**
- **Perplexity по E1 исправился.** 24.10 он утверждал, что IFC мы не отдаём. Теперь называет нас первым и правильно описывает файл: IfcLightFixture и IfcFurnishingElement, кнопка «Документы». Значит, страницу он перечитал. Вывод 24.10 «Perplexity нас не читает» надо сверить с журналом nginx за 25–31.10.
- **Алиса** подхватила ошибку о стране производства (24.10 её не было). Число наград у неё по-прежнему «около 25», верное — 26.
- **Ошибка о стране производства в Google (A3)** держится, источник тот же — карточка участника Interlight 2025 у Gefera Media.
- Google (A2) и Алиса (A1) называют **конкурсное название LC0543-2** со ссылкой на vargov.ru. На /awards и /en/awards его нет (проверено с `?qa=1`). В этой базе оно оставалось в примечании awards-verified.md — убрано 31.10 (26cbd06), сторож check_facts теперь следит и за этим файлом.
- Контроль DALI: «да» держится. Добавились неверные хвосты: «1–10 V и KNX» со ссылкой на сайт дилера и «IFC размечает требования DALI».
- B5 (дизайнер в Дубае): бренда нет, хотя дилер в Дубае есть и Google сам называет его в A1.

**Домены, которые чаще других кормят категорийные ответы Google (B1–B7):**
- litawards.com (B2, B7), hartdesignselection.com (B1, B3), makebespoke.com (B2, B3), svetholl.ru (B1, B6);
- по одному разу: galeriemagazine.com, lasvit.com, camerondesignhouse.com, brandvanegmond.com.

**Прочие показатели на 31.10:**
- **GSC «Генеративный ИИ»**, 30.07–29.10: 2,57 тыс. показов, 785 страниц (22.10 — 2,32 тыс. и 743).
  - Страницы с /configurator — 47 показов.
  - /configurator/ifc4 — 5 (en 3, ru 2); 24.10 было 0.
- **GSC «Эффективность»**, 28 дней (02–29.10): веб — 614 кликов и 8,23 тыс. показов; картинки — 37 и 2,54 тыс.; **видео — 0 и 0**. «Индексирование видео»: проиндексировано 0.
- **Bing AI Performance**, 31.07–29.10:
  - **122 цитаты** (24.10 — 117);
  - grounding query по-прежнему одна, «vargov design» (85, 73,91 %);
  - 16 страниц, /configurator/ifc4 — 0.
- **Метрика, цель 589897394** «Переход в 3D-конфигуратор», 02–31.10: 411 целевых визитов, 568 достижений, конверсия 8,37 %.
  - Целевые визиты по источникам: поиск 167, прямые 132, ссылки 81.

Журнал сервера, Метрика «Из ИИ» и категорийная выдача веб-поиском — в плановом замере 01.11.

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

### Дополнение 24.10.2026, 18:55–19:05 UTC+3 — Perplexity и Bing сняты после входа владельца

Владелец вошёл в обе учётные записи по просьбе из этого замера, поэтому две дыры закрыты.

**Perplexity (вошёл как Vargov Design, бесплатный план).**

| Вопрос | Vargov | Что в ответе |
|---|---|---|
| E1 (EN, дословно из [[ai-probe-set]]) | **назван — и с грубой ошибкой** | «Vargov®Design offers an online generative configurator… but its listed deliverables are **DXF, PDF specification, MAX, and FBX — not IFC**. So… an architect would generally need to convert or rebuild the composition in their BIM environment». Первыми идут DIALux evo / Pro и ReluxDesktop. Источник ошибки назван прямо: **https://vargov.ru/en/configurator** |
| E2 (RU, дословно) | нет | DIALux Pro + Bridge for Revit, ReluxDesktop, Performance in Lighting Light-Performer, Panasonic Lighting BIM, D-LUCE, Eaton; 35 источников |

**Почему это важнее, чем «не назвали».** По E1 модель не промолчала, а **активно утверждает обратное тому, что мы продвигаем**: будто IFC мы не даём. Проверил страницу curl'ом в тот же час: на `/en/configurator` строка `IFC4` встречается 20 раз, «PDF specification» и «tender sheet» по 8. То есть снимок не устарел — модель **слепила список из соседних фрагментов живого текста**: «The DXF drawing for AutoCAD is for internal use only… Ready-made 3D models of the article (max, fbx) on 3ddd.ru and 3dsky.org». Перечисление форматов идёт подряд, а IFC4 упомянут в соседнем блоке — и в список выдачи не попал.

**Отсюда правка, не зависящая от Perplexity:** состав файлов для посетителя должен читаться одной строкой, с IFC4 первым, а DXF (внутренний) и max/fbx (готовые модели на чужих площадках) — отдельно и так, чтобы их нельзя было прочесть как «что отдаёт конфигуратор». Передано агенту сайта.

**Bing Webmaster → AI Performance (Microsoft Copilots and Partners), 29.07–21.10.2026:**
- **Total Citations 117** (точка 11.10 — 94, то есть +23 за десять дней), Avg. Cited Pages 1.
- Всплески: 14.08 — 18, 07.10 — 21, 21.10 — 15; в остальные дни 0–7.
- **Grounding Queries — ровно один: «vargov design»** (Informational / Design), 80 цитат, доля 73,39 %.
  То есть Copilot цитирует нас **только по брендовому запросу**, как и 11.10; категорийной видимости там нет.
- Цитируемых страниц 16: `/en` 54, `/` 12, `/catalog/lc0358` 11, `/en/catalog` 10, `/en/catalog/lc0358` 7,
  `/designer` 6, `/en/about` 4, `/de` 3, `/en/decorative` 2, далее по одной — `/catalog/lc0340`,
  `/en/catalog/lc0080`, `/catalog/lc0571`, `/it/projects/russky-dom-2026`,
  `/de/journal/russian-lighting-design`, `/en/catalog/lc0333`, `/en/lighting`.
- **`/configurator/ifc4` не цитируется ни разу**, хотя у Google AI Mode это прямой источник ответов E1 и E2.
  Ниша IFC4 пока живёт только в Google.
- Побочное наблюдение: цитируются немецкая и итальянская версии страниц — многоязычие работает на видимость.

**Перезапрос в 19:31 того же дня, через десять минут после правки сайта — ответ не изменился.**
Агент сайта переписал блок «Рабочие документы» на `/configurator` (обе версии): теперь первая фраза
прямая — «конфигуратор отдаёт три документа: модель IFC4 (BIM), PDF-спецификацию и тендерный лист»,
а DXF вынесен отдельным предложением со словами «в выгрузку не входит». Проверено curl'ом на бою
в 19:28. Perplexity на тот же вопрос по-прежнему отвечает таблицей:

> «Vargov®Design configurator … **No** — its listed outputs are DXF, PDF specification, MAX, and FBX;
> IFC is not mentioned.»

Значит дело не в формулировке как таковой, а в **снимке страницы у Perplexity**: он старше правки.
`PerplexityBot` и `Perplexity-User` в `robots.txt` сайта разрешены (проверено: 17 агентов, оба со
своими блоками `Allow: /`), то есть доступ открыт и вопрос только в том, когда краулер придёт.
**Перепроверить через 2–7 дней** и записать, сколько заняло обновление, — это первая у нас измеренная
задержка между правкой страницы и изменением ответа ассистента.

> **Неверно — поправлено 02.11.2026.** Ниже читался только общий журнал (`access.log*`), без журнала сайта
> `vargov.ru.access*`. По обоим журналам за 11–24.10 PerplexityBot со своих адресов взял 271 страницу vargov.ru
> (все 200/301), в том числе `/en/configurator` — последний раз 21.10 в 14:38 UTC, за три дня до правки.
> Цифры и даты — в разделе 2026-11-02, «Обращения краулеров». Выводы абзаца ниже не использовать.

**Через час выяснилось, что мерить этим нечего: Perplexity нашу страницу не читает.** Агент сайта
поднял журналы nginx за 11–24.10.2026 (access.log, access.log.1 и тринадцать сжатых):

- **`PerplexityBot` — ровно один запрос за четырнадцать суток.** 21.10.2026 06:36 UTC, адрес
  18.97.9.100, `GET /robots.txt` → 200, причём на хосте **configurator.vargov.ru**, не vargov.ru.
  Ни одной страницы он не брал — ни `/configurator`, ни `/en/configurator`, ни любой другой.
- Для сравнения за последние двое суток: ClaudeBot 64 запроса, Googlebot 54, bingbot 25, GPTBot 3.

**Что из этого следует для метода замера.** Ответ Perplexity про «DXF, PDF, MAX, FBX» собран не с
нашей страницы, хотя он называет её источником: ссылку он показывает, а содержимое берёт из чужого
индекса. Значит Perplexity нельзя использовать как измеритель наших правок — он измеряет не нас.
Правка формулировки на `/configurator` остаётся верной сама по себе (её читают Google и Bing), но
проверять её Perplexity'ем бессмысленно.

**Что это меняет в работе.** Запрет ни при чём: `robots.txt` он получил с кодом 200, и там у
`PerplexityBot` свой блок с `Allow: /`. Дверь открыта, он просто не ходит. Повлиять на это
напрямую мы не можем — значит путь к Perplexity лежит через источники, которые читает он сам:
чужие страницы, где о бренде написано верно. Это тот же вывод, что и по категорийным запросам,
только теперь он подтверждён журналом сервера, а не догадкой.

`/en/configurator` в индексе Bing — «Indexed successfully» (проверено 24.10); одна ошибка SEO:
«Meta Description too long or too short».




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
