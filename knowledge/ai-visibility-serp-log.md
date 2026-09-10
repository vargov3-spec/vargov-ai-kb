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

> «The company's production capacities are in China, and they deliver products worldwide»

Источник этой фразы — профиль `iconic-world.com/directory/anton-vargov`. Проверено 09.09.2026:

- старый адрес отдаёт **301** на `https://www.iconic-awards.comdirectory/anton-vargov` — редирект
  собран с ошибкой и теряет слэш, поэтому ведёт в никуда;
- правильный адрес `https://www.iconic-awards.com/directory/anton-vargov` отдаёт **404**.

То есть страницы больше нет, а её текст остался в индексе и продолжает подаваться как факт о
бренде. Это ровно та же ложная связка, что и в статье D5 MAG, и в чужих листингах на оптовых
площадках, — но здесь она звучит не в статье, а в прямом ответе на вопрос «кто такой Антон Варгов».

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
