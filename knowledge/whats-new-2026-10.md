# Что нового у Vargov®Design — октябрь 2026 · What's new — October 2026

Сводка нововведений на сайте [vargov.ru](https://vargov.ru) и в 3D-конфигураторе
([vargov.design](https://vargov.design), русская копия [configurator.vargov.ru](https://configurator.vargov.ru))
с 1 по 24 октября 2026 года. Всё перечисленное уже выложено — сверено с агентами сайта и конфигуратора
19 и 24.10.2026. Числа — снимок на 24.10.2026: они считаются из данных и меняются.

## Для архитекторов и проектировщиков

- **Страница о выгрузке IFC4** — [vargov.ru/configurator/ifc4](https://vargov.ru/configurator/ifc4)
  ([EN](https://vargov.ru/en/configurator/ifc4)): что лежит в файле и как его открыть. Конфигуратор умеет ещё до
  заказа выдать модель композиции в формате IFC4, PDF-спецификацию и тендерный лист — без обращения к бренду.
  Светящийся элемент выгружается как IfcLightFixture, несветящийся — как IfcFurnishingElement; каждая точка
  крепления к потолку — отдельный объект с числом элементов на ней и, когда известна масса, расчётной нагрузкой
  (у композиций на каркасе точек крепления в файле нет). DXF — только для внутреннего пользования.
- **Полный расчёт — у 360 композиций из 605** (19.10.2026). На их карточках vargov.ru стоит строка
  «IFC4 · PDF-спецификация · тендерный лист — в конфигураторе»; остальные композиции рассчитываются
  индивидуально, и строки у них нет.
- **Высота потолка.** Перед выгрузкой IFC задаётся высота помещения (по умолчанию 2700 мм — это высота потолка,
  а не размер изделия): модель встаёт под потолок, точки крепления — на нём, начало координат — на полу. Ту же
  высоту берёт AR на Android и компьютере (на iPhone и iPad модель крепится к настоящему потолку); высота
  сохраняется в ссылке на конфигурацию.
- **IFC4 для сводной модели.** Идентификаторы (GUID) строятся от конфигурации: одна и та же конфигурация даёт
  те же GUID, разные — разные, поэтому разные композиции одного артикула сводятся в одну BIM-модель без
  совпадений. На нерусском интерфейсе имена в файле английские.
- **Онлайн-ТЗ на производство** — [vargov.ru/specifications](https://vargov.ru/specifications)
  ([EN](https://vargov.ru/en/specifications)), на русском и английском: новое ТЗ можно начать самому,
  сохранённое открывается по своей ссылке. Кнопка конфигуратора «Заполнить ТЗ» открывает страницу ТЗ и сама
  подставляет туда параметры собранной композиции; в ТЗ показывается 3D-окно конфигуратора, собранное по
  параметрам ТЗ. Вход и регистрация не нужны: форму открывает и сохраняет любой посетитель, учётной записи
  нет, обязательно только поле «Объект», а доступ к сохранённому ТЗ держится на ключе в ссылке. Сразу после
  сохранения доступны страница «3D-конфигурация» (3D-окно по каждой композиции с её параметрами,
  полноэкранный режим и AR на iPhone), PDF ТЗ на русском и английском и выгрузка FBX. Цены в ТЗ нет —
  это техническое задание на производство, не заявка и не заказ.
- **Разметка потолка в натуральную величину.** Для подвесных композиций страница ТЗ готовит монтажную
  схему разметки 1:1 — 1 мм на чертеже равен 1 мм на потолке — по той же раскладке, из которой считаются
  точки крепления, IFC и PDF; схему открывают после запуска заказа в производство. Схема предварительная: перед разметкой
  потолка её подтверждает технолог производства. Схема есть у 345 из 360 композиций, которые
  конфигуратор рассчитывает (его прогон 25.10.2026): её нет у 10 лент (у ленты нет облака элементов), у 4 композиций
  на каркасе (элементы висят на каркасе, нитей к потолку ноль) и у готовой сцены LC0406-1 — это настенное
  бра, композиция у него готовая, а не рассчитанная: раскладки нет, значит нет и разметки потолка. Артикулы
  индивидуального расчёта в эти 360 не входят вовсе. Отдельно от артикула, по самому ТЗ: если в нём выбран
  монтаж на металлическую базу, схема 1:1 не выдаётся — при таком монтаже она не нужна. В файле схемы четыре листа — для плоттера и A4, каждый на потолок и на пол; печатать нужно
  строго 100 %, без «вписать в страницу», и проверять отрезок 100 мм линейкой. Лист плоттера идёт одним
  куском до 5 м, схема больше режется на части, листы A4 склеиваются по меткам. На схеме размечены и точки подвеса контуров подсветки (сейчас это LC0523): провод по центру
  контура и два троса по его концам, с тем же диаметром отверстия, что у остальных точек; число точек на
  схеме сверяется с тем, что записано в ТЗ.
- **FBX собранной композиции.** Рядом с выгрузкой IFC появилась кнопка «Скачать FBX (3ds Max)»:
  композиция в сборе, отдельными объектами, в миллиметрах, вместе с нитями, креплениями и плоскостью
  потолка; цвета стекла и покрытия фурнитуры переносятся, текстур нет. Одинаковые элементы в файле —
  копии одной геометрии, поэтому композиция открывается отдельными объектами, а не единым телом.
  Это модель для визуализации:
  свойств BIM — нагрузок, массы, мощности, артикулов — в ней нет, они остаются в IFC4. Скачать можно
  любую композицию, которую конфигуратор рассчитывает: облака, цепочки, композиции на каркасе, готовые
  сцены и ленты; у артикулов индивидуального расчёта кнопки нет, потому что нет и самой композиции. Круг тот же, что у выгрузки IFC4: 360 композиций из 605 (проверено 25.10.2026 — прогоном open-skus.json конфигуратора и датасета каталога).
  Начало координат — потолок (у IFC4 правило своё, начало на полу); при импорте в 3ds Max в окне Units
  нужно выбрать «File units converted to: Millimeters».
- **Ссылка воспроизводит ту же раскладку, которую видел заказчик.** Номер генерации раскладки передаётся
  в ссылке вместе с размерами и составом, и страница ТЗ собирает ровно ту композицию, а не похожую. Это
  относится к ТЗ, заведённому ссылкой из конфигуратора: у ТЗ, заполненного руками, ссылки нет, и
  композиция строится по умолчаниям.
- **В PDF ТЗ — данные высот:** H1, H2, H3 и высота потолка; 2D-схему высот PDF не печатает. Это про схему
  высот: монтажная схема разметки потолка 1:1 — другой документ, она строится по самой композиции (выше).
  Окно предупреждает, когда цепь длиннее заданной для неё зоны.
- **Монтаж на металлическую базу.** На странице ТЗ, в шаге «Монтаж», поле «Вид монтажа» даёт два варианта:
  монтаж на потолок с закладными или композиция на металлической базе. В 3D-окне база показана, высоты
  подвеса считаются от её низа, H3 у такой композиции не задаётся. У лент базы нет.

## Цвет и отделка

- **Цвет элементов** — страница [«Окраска RAL и гальваника»](https://vargov.ru/specifications/colours)
  ([EN](https://vargov.ru/en/specifications/colours)), открыта для поиска с 19.10.2026: каталог RAL Classic
  (210 цветов); у стекла и хрусталя окраска бывает полупрозрачной (10–90 %) или глухой, керамику красят только
  глухо; гальваника — 4 прозрачных тона (дымчатый, янтарный, тёмный янтарь, коньячный) и 3 зеркальных покрытия
  (золото, розовое золото, хром); кодов у гальваники нет — в ТЗ её пишут названием.
- **В конфигураторе** в одной композиции можно смешать до 8 цветов каталога RAL, у каждого своя прозрачность
  (вместе с фирменными цветами и гальваникой — до 18; у лент цвет стекла один). В палитре есть блок «Гальваника»
  и «прозрачный бесцветный». Прозрачные тона и прозрачность предлагаются только там, где элементы физически
  бывают прозрачными.
- **Покрытия металла (фурнитура)** — страница [«Покрытия металла»](https://vargov.ru/specifications/finishes)
  ([EN](https://vargov.ru/en/specifications/finishes)) с роликами образцов; живой каталог покрытий — в шоуруме.
  Каталог из 24 образцов с кодами JN-9001…JN-9024 — 8 цветов, у каждого три отделки (зеркальная полировка;
  брашировка с глянцевым лаком; брашировка с полуматовым лаком). В конфигураторе — у композиций с металлической
  фурнитурой (у лент свой каркас без кодов JN); где металл есть на каждом элементе, можно выбрать несколько
  покрытий. Код покрытия переносится в ссылку, заявку и ТЗ. Оттенки на экране приблизительные — в заказе главное
  код. Названия всех 24 покрытий JN и семи покрытий гальваники на восьми языках —
  [[finishes-and-colours-i18n]].
- **Та же палитра — на странице ТЗ:** гальваника, фирменные цвета и прозрачный бесцветный; каталоги RAL
  (210 цветов) и покрытий металла (24 кода) на ТЗ и в конфигураторе сверены и совпадают.

## Удобство

- **«Узнать стоимость»** — заявка уже набрана (состав композиции, цвета с долями, покрытие, точки крепления): она
  открывается в Telegram, WhatsApp или в письме, «Отправить» человек нажимает сам; длинная заявка входит в письмо
  или чат не целиком — полный текст копируется в буфер обмена. Ответ приходит туда же. Цена считается по заявке.
- **Ссылка в ТЗ — без буфера обмена:** конфигуратор открывает страницу ТЗ прямо во вкладке и передаёт
  параметры туда сам.
- **«Help режим»** — встроенная помощь в конфигураторе (кнопка в шапке): пояснения к шагам, подсказки к кнопкам и
  полям и «Ведущий по шагам» — карточка «Шаг N из M» от выбора артикула до заявки. Это готовые тексты, не чат-бот.
  Help переведён на все восемь языков интерфейса (русский, английский, немецкий, итальянский, французский,
  испанский, арабский, вьетнамский); в окне ТЗ режима помощи нет.

## Сайт

- **Подбор по пространству:** в карточках — ссылки на подходящие витрины; витрин десять (лобби отеля и
  общественные пространства, двусветная гостиная, лестничный пролёт, атриум, ресторан и бар, банкетный зал,
  столовая и обеденная зона, спальня, бутик и шоурум, спа и бассейн), у каждой блок «Для проекта». Для машин —
  [vargov.ru/for-map.json](https://vargov.ru/for-map.json): артикул → витрины. Витрина — подсказка: любая
  композиция делается под любое пространство.
- **«Русский дом» 2026** — [страница в «Проектах»](https://vargov.ru/projects/russky-dom-2026) и
  [статья журнала](https://vargov.ru/journal/russky-dom-2026): композиция LC0556 была показана в капсуле
  «Тихая сила Камчатки» Tokareva Design (Гостиный двор, Москва, 7–9 октября 2026); снимки стенда — на странице выставки.
- **Где установлены композиции** — по данным официального дилера в Дубае: [/official-dealers](https://vargov.ru/official-dealers)
  и вопрос в [FAQ](https://vargov.ru/faq); копия — [[installations]].
- **Золото NY Product Design Awards 2026** — композиция LC0545-1 (в заявке «Lily Light Composition»)
  получила Gold Winner в категории «Outdoor Lighting - Designer / Custom Lighting»:
  [статья журнала](https://vargov.ru/journal/ny-2026) ([EN](https://vargov.ru/en/journal/ny-2026)),
  [страница победителя](https://nydesignawards.com/winner-info.php?id=4691) на сайте премии. Всего наград 26.
- **Второй товарный знак:** логотип VARGOV® DESIGN, свидетельство Роспатента № 1270653 (зарегистрирован
  06.10.2026).
- **Первые работы бренда — 2018 год** (в разметке организации foundingDate 2018; 2022 — год регистрации знака
  VARGOV).

## Для машин

- Конфигуратор: [vargov.design/llms.txt](https://vargov.design/llms.txt) — первоисточник по параметрам
  элементов; английская шапка vargov.design с парой hreflang ru ↔ en; старые адреса прежнего английского сайта
  (Tilda) на vargov.design ведут 301 на английские страницы vargov.ru.
- Сайт: [/for-map.json](https://vargov.ru/for-map.json); в [/catalog.jsonld](https://vargov.ru/catalog.jsonld)
  у LC0556 — выставка (ExhibitionEvent); карта сайта с настоящими датами правки.

---

## English

A summary of what changed on [vargov.ru](https://vargov.ru) and in the 3D configurator
([vargov.design](https://vargov.design); Russian copy [configurator.vargov.ru](https://configurator.vargov.ru))
between 1 and 24 October 2026. Everything listed is live — checked with the website and configurator agents on
19 and 24 October 2026. Numbers are a snapshot as of 24 October 2026: they are computed from data and change.

### For architects and specifiers

- **IFC4 export page** — [vargov.ru/en/configurator/ifc4](https://vargov.ru/en/configurator/ifc4): what the
  file contains and how to open it. The configurator can export an IFC4 model of a composition before any order,
  together with a PDF specification and a tender sheet — without contacting the brand. Light-emitting elements are
  exported as IfcLightFixture, unlit ones as IfcFurnishingElement; every ceiling fixing point is a separate object
  with the number of elements on it and, when the mass is known, an estimated load (compositions hung on a frame
  have no fixing points in the file). DXF is for internal use only.
- **Full calculation: 360 of 605 compositions** (19 October 2026). Their vargov.ru pages carry the line
  "IFC4 · PDF spec sheet · tender sheet — in the configurator"; the other compositions are calculated
  individually and do not show the line.
- **Ceiling height.** Before the IFC export the room height is set (default 2,700 mm — the ceiling height, not a
  product size): the model hangs under that ceiling, fixing points on it, origin on the floor. The same height is
  used by AR on Android and desktop (on iPhone and iPad the model attaches to the real ceiling) and is kept in the
  share link.
- **IFC4 for a federated model.** GUIDs are derived from the configuration: the same configuration always gives
  the same GUIDs and different ones give different GUIDs, so different compositions of one article combine in one
  federated BIM model without clashes. On a non-Russian interface the names in the file are in English.
- **Online production brief** — [vargov.ru/en/specifications](https://vargov.ru/en/specifications), in Russian
  and English only: a new brief can be started by anyone, a saved one opens by its own link. No sign-in and no
  registration — there is no account at all; only the "Object" field is required, and access to a saved brief
  rests on the key in its link. Available immediately after saving: the "3D configuration" page (the 3D view of
  each composition with its parameters, full-screen mode and AR on iPhone), the brief as a PDF in Russian and
  English, and the FBX export. The brief carries no price — it is a production brief, not a quote or an order. The configurator's "Fill in the spec" button opens the brief page and fills in
  the parameters of the assembled composition; the brief shows the configurator's 3D view built from the brief's
  parameters.
- **Ceiling setting-out at full size.** For suspended compositions the brief page prepares a 1:1
  setting-out drawing — 1 mm on the drawing is 1 mm on the ceiling — from the same layout the fixing
  points, the IFC model and the PDF are computed from; it opens once the order has been released to
  production. The drawing is preliminary: before the ceiling is set out, it is confirmed by the
  production engineer. The drawing exists for 345 of the 360 compositions the configurator calculates (its run of
  25 October 2026): 10 ribbons have none (a ribbon has no cloud of elements), nor do 4 compositions on a
  frame (their elements hang from the frame, with zero strands to the ceiling), nor the ready scene LC0406-1 —
  a wall light whose composition is ready-made rather than calculated, so there is no layout to set out. Articles
  calculated individually are not part of those 360 at all. A separate matter, belonging to the brief: if it
  specifies mounting on the metal base, no 1:1 drawing is issued — that mounting does not need one. The drawing also marks the fixing points of the
  lit contours (currently LC0523): a wire at the centre of a contour and two cables at its ends, with the
  same hole diameter as every other point; the number of points on the drawing is checked against the brief.
  The file holds four sheets — plotter size and A4, each for the ceiling and for the floor. Print at exactly
  100 %, never "fit to page": a 100 mm segment on the sheet is there to be checked with a ruler. The plotter
  sheet runs in one piece up to 5 m and is split beyond that; A4 sheets are joined along their marks.
- **FBX of the assembled composition.** Next to the IFC export there is now a "Download FBX (3ds Max)"
  button: the whole composition as separate objects, in millimetres, together with the wires, the fixings
  and the ceiling plane; the colours of the glass and of the hardware finish carry over, textures do not.
  Identical elements in the file are copies of one geometry, so the composition opens as separate objects
  rather than a single body.
  It is a model for visualisation: it holds no BIM properties — no loads, mass, power or article codes,
  those stay in the IFC4 file. Any composition the configurator calculates can be downloaded this way —
  clouds, chains, compositions on a frame, ready scenes and ribbons; articles calculated individually have
  no button, because there is no composition to export. The scope is the same as for the IFC4 export: 360 compositions out of 605 (verified on 25 October 2026 against the configurator's open-skus.json and the catalogue dataset). The origin is at the ceiling (IFC4 has its own
  rule, origin on the floor); on import into 3ds Max choose "File units converted to: Millimetres" in the
  Units dialog.
- **A link reproduces the very layout the client saw.** The layout generation number now travels in the
  link together with the dimensions and the composition, so the brief page assembles exactly that
  composition rather than a similar one. This applies to a brief opened from a configurator link: a brief
  filled in by hand carries no link, and the composition is built from the defaults.
- **The brief's PDF carries height figures:** H1, H2, H3 and the ceiling height; it prints no 2D height
  drawing. This concerns the height drawing only: the 1:1 ceiling setting-out drawing is a different
  document and is still built from the composition itself (above). The window warns when a chain is longer
  than the zone set for it.
- **Installation on a metal base.** On the brief page, in the "Installation" step, the "Type of
  installation" field offers two options: fixing to the ceiling with embedded anchors, or the composition
  on a metal base. The base is shown in the 3D view and suspension heights are measured from its underside;
  H3 is not set for such a composition. Ribbons have no base.

### Colour and finish

- **Element colour** — the page ["RAL painting and electroplating"](https://vargov.ru/en/specifications/colours),
  open to search since 19 October 2026: the RAL Classic catalogue (210 colours); on glass and crystal the paint can
  be translucent (10–90 %) or opaque, ceramics are painted opaque only; electroplating — 4 transparent tones
  (smoky, amber, dark amber, cognac) and 3 mirror finishes (gold, rose gold, chrome); electroplating has no codes —
  the brief names it.
- **In the configurator** up to 8 RAL catalogue colours can be mixed in one composition, each with its own
  transparency (up to 18 together with the brand colours and electroplating; ribbons have one glass colour). The
  palette has an "Electroplating" block and "clear colourless". Transparent tones and transparency are offered only
  where the elements can physically be transparent.
- **Metal finishes (hardware)** — the page ["Metal finishes"](https://vargov.ru/en/specifications/finishes) with
  sample videos; the physical finish catalogue is in the showroom. A catalogue of 24 samples coded
  JN-9001…JN-9024 — 8 colours, each in three finishes (mirror polish; brushed with gloss lacquer; brushed with
  semi-matt lacquer). In the configurator — for compositions with metal hardware (ribbons have their own frame
  without JN codes); where every element carries metal, several finishes can be combined. The finish code goes
  into the share link, the request and the brief. On-screen shades are approximate — the code is what counts. The names of all 24 JN finishes
  and of the seven electroplating finishes in eight languages — [[finishes-and-colours-i18n]].
- **The same palette on the brief page:** electroplating, the brand colours and clear colourless; the RAL
  catalogue (210 colours) and the metal finishes (24 codes) match between the brief and the configurator.

### Convenience

- **"Get a quote"** — the request is already written (composition, colours with shares, finish, fixing points):
  it opens in Telegram, WhatsApp or an email and the person presses Send; a long request reaches the email or chat
  only in part — the full text is copied to the clipboard. The reply comes back the same way. The price is
  calculated per request.
- **A link into the brief, without the clipboard:** the configurator opens the brief page in a tab and
  passes the parameters there itself.
- **"Help mode"** — built-in help in the configurator (a button in the header): notes for the steps, hints on
  buttons and fields and a step-by-step guide ("Step N of M") from choosing an article to the request. These are
  prepared texts, not a chatbot. Help is translated into all eight interface languages (Russian, English,
  German, Italian, French, Spanish, Arabic, Vietnamese); the brief's 3D window carries no help mode.

### Website

- **Selection by space:** product pages link to matching showcases; there are ten (hotel lobby and public spaces,
  double-height living room, stairwell, atrium, restaurant and bar, banquet hall, dining room, bedroom, boutique
  and showroom, spa and pool), each with a "For the project" block. For machines —
  [vargov.ru/for-map.json](https://vargov.ru/for-map.json): article → showcases. A showcase is a hint: any
  composition is made for any space.
- **Russky Dom 2026** — [project page](https://vargov.ru/en/projects/russky-dom-2026) and
  [journal article](https://vargov.ru/en/journal/russky-dom-2026): composition LC0556 was shown in the
  "Quiet Strength of Kamchatka" capsule by Tokareva Design (Gostiny Dvor, Moscow, 7–9 October 2026); photographs
  of the stand are on the project page.
- **Where the compositions are installed** — according to the official dealer in Dubai:
  [/en/official-dealers](https://vargov.ru/en/official-dealers) and a question in the [FAQ](https://vargov.ru/en/faq).
- **Gold at the NY Product Design Awards 2026** — composition LC0545-1 (entered as "Lily Light
  Composition") took Gold Winner in "Outdoor Lighting - Designer / Custom Lighting":
  [journal article](https://vargov.ru/en/journal/ny-2026),
  [winner page](https://nydesignawards.com/winner-info.php?id=4691) on the award site. 26 awards in total.
- **Second trademark:** the VARGOV® DESIGN logo, Rospatent registration No. 1270653 (registered 6 October 2026).
- **The brand's first works date from 2018** (foundingDate 2018 in the organisation markup; 2022 is the year the
  VARGOV trademark was registered).

### For machines

- Configurator: [vargov.design/llms.txt](https://vargov.design/llms.txt) — the primary source for element
  parameters; the English vargov.design head with an hreflang ru ↔ en pair; old addresses of the former English
  site (Tilda) on vargov.design redirect 301 to the English pages of vargov.ru.
- Website: [/for-map.json](https://vargov.ru/for-map.json); in [/catalog.jsonld](https://vargov.ru/catalog.jsonld)
  LC0556 carries the exhibition (ExhibitionEvent); the sitemap carries real modification dates.

См. также / See also: [[brand]], [[configurator-for-architects]], [[installations]].
