# Vargov® Design — независимые внешние упоминания (аудит видимости)

Найдено веб-поиском 2026-07-06 — это реальные, проверяемые сторонние источники (не сам vargov.ru/vargov.design). Важно для Wikidata-нотабильности, PR и понимания текущего состояния видимости бренда в открытом вебе.

## Базы данных наград (независимые площадки)
- [International Design Awards — LC0236, Vargov Anton, Vargov® Design-Lighting studio](https://www.idesignawards.com/social/zoom.php?eid=9-46057-22) — победитель, официальная страница IDA.
- [International Design Awards — LC0516](https://www.idesignawards.com/social/zoom.php?eid=9-61165-25) — победитель, сезон 2025 (найдено при аудите 2026-07-07).
- [International Architecture & Design Awards 2026 (ad-c.org) — LC0303](https://ad-c.org/winner/light-composition-vargov-design-lc0303/) — победитель, Architecture & Design Community (найдено при аудите 2026-07-07).
- [New York Product Design Awards — LC0343](https://nydesignawards.com/winner-info.php?id=1296) — победитель, официальная страница NYPDA.
- [Конкурс «Российский светодизайн» 2022 — LC0217](https://online.gefera.ru/contest/rldc-2022/works/?work_id=14012747) — конкурсная площадка gefera.ru. В `awards.ts` премия называется «Interlight Russia · Российский светодизайн» (специальный приз 2022); «RLDC» — обозначение площадки, отдельной премией не является.
- [Конкурс «Российский светодизайн» 2023 — LC0342](https://online.gefera.ru/contest/rldc-2023/works/?work_id=14119182) — конкурсная работа на gefera.ru. Награда за LC0342 в `awards.ts` — 2-е место IX сезона ADD Awards.
- ~~ADD Awards — Антон Варгов, жюри (addawards.ru/jury/293063/)~~ — **страница мертва, 404** (агент по сайту, 05.09.2026); с сайта ссылка снята, сертификат остался. Для Wikidata как источник не годится, пока не найден новый адрес.
- [LOOP Design Awards 2025 — Lighting Composition LC0458](https://loopdesignawards.com/project/lighting-composition-lc0458) — страница победителя на сайте премии (независимая организация). Прежняя ссылка на vargov.design/tpost/ryfpbm1yy1-loop-design-awards-2025 отдаёт 404 с 2026-09-06 и снята.

## Профили и справочники дизайнеров

### Как читать результат проверки внешней страницы
Правило сформулировано агентом сайта 07.09.2026 после трёх случаев за сутки, когда инструмент врал по-своему: 3ddd отдавал 200 на любой адрес карточки; curl на машине владельца перестал ходить куда бы то ни было; `nydesignawards.com` отдал 403 на адрес VPS, хотя с машины владельца страница открывается и содержит семь упоминаний бренда.

**Отрицательный ответ — это утверждение о ПАРЕ «адрес + откуда смотрим», а не о странице.** До вывода «страница мертва» его подтверждают вторым каналом. Положительный ответ такой оговорки не требует. Сюда же: клиент, который сам идёт по редиректам, скрывает 301 — при проверке формы адреса автопереход выключать.

### Страницы жюри IAA (проверены 07.09.2026, все отвечают 200)
Независимые подтверждения членства в жюри — одна и та же карточка «Vargov Anton · CEO, Vargov Design · Russia» на пяти площадках International Awards Associate:
- [MUSE Design Awards — Grand Jury Panel](https://design.museaward.com/our-judge.php)
- [NY Product Design Awards — Grand Jury Panel](https://nydesignawards.com/our-judge.php)
- [Rome Design Awards — Grand Jury Panel](https://romedesignawards.com/our-judge.php)
- [French Design Awards — Grand Jury Panel](https://frenchdesignawards.com/our-judge.php)
- [TITAN Property Awards — Grand Jury Panel](https://thepropertyawards.com/our-judge.php) (домен `thepropertyawards.com`, не `titanpropertyawards.com` — тот не резолвится)

Сама карточка перечисляет шесть программ, включая **Noble World Hotel Awards** — её страницу жюри найти не удалось: `nobleworldawards.com`, `nobleworldhotelawards.com` не резолвятся, `thehotelawards.com/our-judge.php` → 404. Ссылаться на неё нельзя, пока адрес не подтверждён.

⚠️ Текст карточки написан IAA и содержит формулировки, которых владелец избегает: «international brand», «global leader in designing, producing, and selling». Страницы чужие, править нельзя; для наших материалов это не источник формулировок, а подтверждение факта «член жюри пяти программ».

- ~~ICONIC World — Anton Vargov, directory profile~~ (`https://www.iconic-world.com/directory/anton-vargov`) — **страница не открывается, но дело не в профиле: раздел директории потерян при переезде домена** (диагноз уточнён 07.09.2026). German Design Council перевёл `iconic-world.com` на `iconic-awards.com`, и редирект собран с ошибкой — теряется слэш: любой адрес ведёт на `www.iconic-awards.comdirectory/…`, несуществующее имя. Проверено на посторонних профилях: Artemide и Vibia Lighting ломаются точно так же, а на новом домене `/directory/artemide` тоже отдаёт 404 — то есть раздела там нет ни у кого. Живут только `/en/winner` и `/en/the-catalogue` (200). **Искать «новый адрес профиля» бессмысленно — его нет ни у одного участника.**
  ⚠️ **Профиль остаётся в поисковом индексе вместе с фактической ошибкой.** Поиск по домену выдаёт карточку Anton Vargov с текстом про «design and manufacture of lighting and decor in China» — третье место, где живёт та же ложная связка (после D5 MAG и описания Facebook, исправленного 05.09). Страница мертва, но языковые модели читают индекс, а не код ответа. Поэтому задача не «восстановить ссылку», а либо добиться восстановления раздела с исправленным текстом, либо просить об удалении страницы из индекса — письмо в German Design Council готово к отправке, см. [[outreach-tracker]].

### Страницы победителя MUSE (проверены 07.09.2026)
- LC0564 «Oceanic Illumination», 2026 · Professional · Lighting Design — Designer / Custom Lighting · Entrant Vargov Design · Country Russia: [winners-info.php?id=40265](https://design.museaward.com/winners-info.php?id=40265).
  **Канонический адрес — с «s»** (уточнено 07.09.2026 агентом сайта): форма `winner-info.php` отдаёт 301 на `winners-info.php`. Я сначала записал наоборот, потому что проверял клиентом, который сам шёл по редиректу и показывал 200 у обеих форм. На доменах NY и London, наоборот, рабочая форма — без «s»; общего правила по семейству IAA нет, адрес проверять по каждому домену отдельно.
- LC0237, 2023, та же категория: [winners-info.php?id=13101](https://design.museaward.com/winners-info.php?id=13101).
- **Уровень награды на странице не выведен текстом** — ни «Gold», ни «Platinum»; для машины страница подтверждает участие и категорию, но не уровень. Уровень остаётся подтверждён только сертификатом (см. [[awards-verified]]).
- По названию работы страницы не находятся: поиск «Oceanic Illumination MUSE Design Awards Vargov» их не возвращает (в выдаче встречается форма без «s» — она ведёт на каноническую через 301). Это и был вопрос из [[gap-list-2026-09]] — страницы живы, но в категорийную выдачу не попадают.
- ⚠️ На странице LC0237 (2023) опубликованы размер элемента и материал — их владелец в своих материалах не публикует. Это его собственная давняя анкета на чужой площадке; менять нам нечего, но знать стоит: данные открыты и индексируются.

## Редакционные публикации

- [D5 MAG — «This Lighting Piece Looks Different Every Time You Walk Past It»](https://d5mag.com/this-lighting-piece-looks-different-every-time-you-walk-past-it/) — 21.06.2025, автор Tina King (Deputy Editor), о композиции LC0358 и победе на SIT Furniture Design Awards. **Первая независимая редакционная публикация о бренде** (найдена 2026-09-04). Уровень источника средний: у D5 MAG названная редакция и отбор материалов, но есть опция платного спонсирования уже принятой статьи — не Dezeen.
  ⚠️ **Фактическая ошибка в тексте:** «Registered in 2022, the company designs and makes its lighting and decor in China». Это противоречит позиционированию и совпадает по смыслу с чужими листингами на оптовых площадках (материалы по защите знака — вне репозитория). Запрос на исправление отправлен 05.09.2026 (editor@d5mag.com, Tina King); ответа нет, напоминание не раньше 16.09 — см. [[outreach-tracker]]; текст письма в [[gap-list-2026-09]].

## Партнёрства / коллаборации
- ~~Fabli.pro — Design by Vargov, «Фабрика блестящих идей» (https://fabli.pro/design-by-vargov/)~~ — **ссылка мертва с 2026-09-06**: страница отдаёт 404, поиск по сайту fabli.pro по слову «vargov» пуст. Из аргументации снять до появления нового адреса (сохранить как архивное упоминание коллаборации; см. также цветочные бутоны LC0071/similar в каталоге).

## Видео
- [YouTube — Интервью Антона Варгова на INTERLIGHT 2025](https://www.youtube.com/watch?v=_HBECagnlDI) — независимая публикация, интервью с основателем на профильной выставке.

## Соцсети (не источник для нотабильности, но канал присутствия)
- Instagram: @vargov_design — официальный аккаунт бренда. Второй аккаунт в выдаче, @vargovdesign, — аккаунт официального дилера в Дубае (подтверждено владельцем 2026-09-05), не сквоттер.
- Facebook: facebook.com/vargovdesign — страница бренда «vargov_design» (1,2 тыс. подписчиков, телефон +7 916 537-33-52). **Внимание (проверено 05.09.2026):** в описании страницы написано «Производство осуществляется на эксклюзивной фабрике Vargov®Design в Китае», ссылка ведёт на vargov.design, а пост от 04.08.2025 называет xprojectlight.ru «official distributor in Russia» и перечисляет материалы. **Исправлено 05.09.2026 вечером:** краткая биография заменена на формулировку владельца (без страны производства, 23 награды); ссылка в разделе «Ссылки» — https://vargov.ru/; подпись к обложке от 04.12.2025 переписана (фраза про фабрику в Китае удалена, добавлены Product Designer of the Year и 23 награды). Пост от 04.08.2025 (Interlight, «official distributor in Russia — xprojectlight.ru», материалы) был опубликован через Metricool и не редактировался — **удалён владельцем 05.09 ~20:45**. Проверено после удаления: на странице нет ни xprojectlight, ни «Китае», ни «международная компания»; ссылка vargov.ru; подпись к обложке с новым текстом. В sameAs сайта с 05.09 (коммит сайта 2ff2d36), без видимой ссылки в подвале.
- Pinterest: https://www.pinterest.com/Vargov_Design/ — домен vargov.ru подтверждён (p:domain_verify), в sameAs сайта и базы с 05.09.2026 (сайт 7e9a8e5, с видимой ссылкой в подвале на всех языках).
- Google Карты (шоурум): https://www.google.com/maps?cid=2970420474499935128 — подтверждённый профиль, с 05.09.2026.
- Яндекс Карты (шоурум): https://yandex.ru/maps/org/vargov_design/199433674369/ — владение подтверждено 05.09.2026, правки на модерации.

## Обновление 2026-07-07
Проведён полноценный аудит видимости в ИИ — результаты и приоритеты в [[ai-visibility-audit-2026-07]]. Кратко: находимость по имени бренда высокая, по категорийным запросам («посоветуй бренд освещения») — нулевая на английском и последняя позиция на русском. Vargov Design и Anton Vargov отсутствуют в Wikidata, тогда как Moooi, Flos, Ingo Maurer там есть.

## Вывод по аудиту (на 2026-07-06)
- Прямых упоминаний бренда в дизайн-медиа (Dezeen, ArchDaily, Archello, Houzz и т.п.) поиском не найдено — это главный пробел для PR-работы (Приоритет 3).
- Реальные независимые верифицируемые источники ЕСТЬ (базы наград, справочник ICONIC, жюри ADD Awards) — этого достаточно как отправная точка для черновика Wikidata-сущности (see [[wikidata-draft]]), хотя Wikipedia-уровня notability (значимые независимые публикации в СМИ) пока не хватает.
- Реальное видео-интервью с Interlight 2025 существует — можно использовать как VideoObject в Schema.org (см. [[brand]] и references/organization.jsonld).

## Обновление 2026-09-04

Полный список независимых источников по наградам — 23 награды со ссылками на
страницы победителей и сертификаты — теперь ведётся в [[awards-verified]]
(источник `awards.ts` репозитория сайта). Программ пятнадцать: MUSE Design
Awards, IDA Design Awards, LIT Lighting Design Awards, LOOP Design Awards,
SIT Furniture Design Award, Luxury Lifestyle Awards, ADD Awards, European
Product Design Award, NY Product Design Awards, BLT Built Design Awards,
The London Design Awards, International Architecture & Design Awards · ADC,
Houzee Awards, Interlight Russia · Российский светодизайн, Awwwards.

Сентябрьский аудит видимости — [[ai-visibility-audit-2026-09]]. Кратко: по
имени бренда выдача полностью своя, по категорийным запросам («посоветуй бренд
освещения») бренда нет ни на английском, ни на русском. Wikidata-сущности,
отсутствовавшие на момент аудита 04.09, опубликованы 05.09.2026: Vargov Design —
Q141301076, Anton Vargov — Q141300942 ([[wikidata-draft]]).

## Упоминания со знаком минус

- **Маркетплейсы**: найден листинг стороннего поставщика, использующий знак VARGOV (№ 896936). Для ИИ это ядовитая связка бренда с оптовой люстрой. Материалы по защите знака — вне репозитория (подробности — в приватной папке PR владельца).
- ~~Два аккаунта Instagram~~ — закрыто 05.09.2026: `@vargov_design` — бренд, `@vargovdesign` — официальный дилер в Дубае (подтверждено владельцем); из списка «минус» снято.
