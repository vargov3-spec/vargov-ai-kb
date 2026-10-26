# Светильник, который не доезжает до модели

*Эссе для архитекторов и проектировщиков: что должно лежать в файле, чтобы декоративный светильник вообще мог участвовать в координации. Опубликовано 26.10.2026. Английская версия — ниже.*

Модель здания знает о потолке много. Она знает плиту, инженерию над ней, отделку под ней, где садятся спринклеры и где конструктив не примет ещё один анкер. Чего она обычно не знает — так это того единственного предмета, на который смотрят все, кто входит в комнату.

Декоративный свет доезжает до модели последним. Он приходит блоком с верным силуэтом и пустотой внутри, рендером, вставленным в лист, или подписью «люстра, по согласованию». Координация, которая действительно нужна, случается потом — на объекте.

## Что светильник должен нести, чтобы быть полезным

Если спросить, что модели на самом деле нужно от светильника, список выходит короткий и совсем не парадный.

Нужно знать, **где предмет крепится** — не одна точка под центром, а все точки в том положении, которое изделие действительно займёт: именно это конструктор сверяет с плитой.

Нужно знать, **что несёт каждая из них**. Композиция из двадцати семи элементов на двадцати семи отдельных креплениях нагружает потолок неравномерно, и инженер, видящий один ком массы в центре тяжести, проверяет выдумку. Пример настоящий: артикул LC0102 выгружается двадцатью семью элементами и двадцатью семью точками крепления.

Нужно, чтобы объект **вёл себя как объект** — был классифицирован так, чтобы его видели спецификации, проверка коллизий и подсчёт объёмов.

И нужна **опознаваемость, переживающая сведение моделей**. Если три варианта одного артикула висят в трёх комнатах, модель обязана их различать; при общих опознавателях они сольются в один, как только модели соберут вместе.

Ничего экзотического здесь нет. Просто это больше того, что может нести картинка.

## Что лежит в нашем файле

Конфигуратор собирает композицию под конкретное помещение прямо в браузере, и посетитель выгружает результат моделью IFC4. Четыре вещи в этом файле стоит назвать.

**Точки крепления — отдельные объекты.** Каждая точка, где композиция встречается с потолком, выходит своим объектом `IfcDiscreteAccessory` на своём месте. На каждой записано число элементов, которые на ней висят, и, когда масса известна, расчётная нагрузка — распределение, а не среднее.

**Светящиеся и несветящиеся элементы разведены.** Признак берётся по элементу, а не по артикулу: то, что светит, выгружается как `IfcLightFixture`, то, что не светит, — как `IfcFurnishingElement`. Спецификации после этого ведут себя так, как положено.

**Файл строится под заданный потолок.** Высота задаётся перед выгрузкой — по умолчанию 2700 мм, и это высота помещения, а не размер изделия. Композиция встаёт под этот потолок, точки крепления садятся на его плоскость, начало координат остаётся на полу, и файл попадает в модель комнаты без ручного сдвига по вертикали.

**Опознаватели берутся из конфигурации.** GUID строятся из артикула и отпечатка самой конфигурации, поэтому две разные композиции одного артикула остаются двумя разными объектами при сведении моделей. Это не теория: до того как это починили, две конфигурации одного артикула делили все опознаватели, и часть из них указывала в одном файле на светильник, а в другом — на точку подвеса.

Вместе с моделью тот же шаг отдаёт спецификацию и тендерный лист для закупки.

## Где файл заканчивается

Четыре границы, названные прямо, — потому что архитектор, обжигавшийся на обещаниях поставщиков, читает сначала их.

**Это координационные данные, а не цеховой чертёж.** Расчёт концептуальный, финальную спецификацию подтверждает конструктор бренда; в самой выгрузке это написано. Файл годится, чтобы поставить изделие на место, проверить габариты и внести нагрузки в разговор с конструктором, — но не чтобы сверлить по нему как по подписанному документу.

**Точки крепления выгружаются не у всех.** Композиции на каркасе и готовые сцены висят на каркасе, а не на плите: крепить к потолку нечего, и точек в файле нет. Это пять артикулов из трёхсот шестидесяти, выгружаемых полностью.

**В эти триста шестьдесят входит не весь каталог.** Полностью выгружаются 360 композиций из 605. Остальное — смешанная группа: настенные и напольные предметы, скульптурные объекты и вещи шоурума, которых конфигуратор не собирает вовсе, и подвесные композиции, считающиеся индивидуально.

**Семейства Revit нет.** Формат `.rfa` — закрытый двоичный, собрать его без самого Revit нельзя, библиотечного семейства у бренда нет. Поставляется файл IFC4, и он открывается в приложениях с импортом IFC4 — среди них Revit, ArchiCAD, Allplan, Tekla и Navisworks. Приложение, читающее только IFC2x3, его не откроет.

Цеховые чертежи остаются внутренними: они для собственного производства бренда и его дилеров.

## Суть

Модель — это обещание о здании, которого ещё нет. Каждый объект в ней, который своего обещания не держит — без веса, без крепления, без опознаваемости, — это место, где чертёж и здание потом разойдутся.

Декоративный свет был таким местом долго. Так быть не обязано: сведения существуют на стороне производителя, и вопрос лишь в том, записаны они в файл или оставлены в переписке.

*Страница выгрузки — что лежит в файле и как его открыть: [vargov.ru/configurator/ifc4](https://vargov.ru/configurator/ifc4)*

---

# The light fitting that never arrives in the model

*An essay for architects, about what has to be inside a file before a decorative light fitting can take part in coordination at all. Published 26 October 2026.*

A building model knows a great deal about a ceiling. It knows the slab, the services above it, the finish below it, where the sprinklers land and where the structure will not take another anchor. What it often does not know is the one object everybody looks at when they walk into the room.

Decorative lighting tends to reach the model late. It arrives as a block with the right silhouette and nothing behind it, as a render dropped onto a sheet, or as a note that reads *feature pendant, by others, TBC*. The coordination that matters then happens afterwards, on site.

## What a luminaire has to carry to be useful

Ask what the model actually needs from a light fitting, and the list is short and unglamorous.

It needs to know **where the piece attaches** — not one point under the centre of the fixture, but every point, in the position the fixture will really occupy, because that is what the structural engineer checks against the slab.

It needs to know **what each of those points carries**. A composition of twenty-seven elements on twenty-seven separate fixings does not load the ceiling evenly, and an engineer who sees one lump of mass at the centroid is checking a fiction. That is a real example: catalogue item LC0102 exports twenty-seven elements and twenty-seven fixing points.

It needs the object to **behave like an object** — classified so that schedules, clash detection and takeoffs can see it for what it is.

And it needs **identity that survives federation**. If three variants of the same catalogue item hang in three rooms, the model must keep them apart; if they share identifiers, they collapse into one another the moment the models are combined.

None of this is exotic. It is simply more than an image can carry.

## What we put in the file

Our configurator assembles a composition for a given room in the browser, and the visitor exports the result as an IFC4 model. Four things in that file are worth naming.

**Fixing points are separate objects.** Every point where the composition meets the ceiling comes out as its own `IfcDiscreteAccessory` in its own place. Each one carries the number of elements hanging from it and, where the mass is known, an estimated load — a distribution rather than an average.

**Lit and unlit elements are classified apart.** The test is applied to the element, not to the catalogue item: elements that light are exported as `IfcLightFixture`, elements that do not as `IfcFurnishingElement`. Schedules then behave the way they should.

**The file is built for a stated ceiling.** The height is set before export — by default 2,700 mm, which is the height of the room, not a dimension of the piece. The composition is placed under that ceiling, the fixing points sit on its plane, and the origin stays on the floor, so the file lands in the room model without a manual vertical shift.

**Identifiers come from the configuration.** GUIDs are derived from the catalogue item plus a fingerprint of the configuration itself, so two different compositions of the same item stay two different objects when models are federated. This is not theoretical: before it was fixed, two configurations of one item shared every identifier, and some of them pointed at a luminaire in one file and at a suspension point in the other.

Alongside the model, the same step produces a specification and a tender sheet for procurement.

## Where the file stops

Four limits, stated plainly, because an architect who has been burned by supplier promises reads these first.

**It is coordination data, not a shop drawing.** The calculation is conceptual, and the final specification is confirmed by the brand's own engineer. The export says so itself. Use it to position, to check clearances and to carry loads into the structural conversation — not as a signed document to drill from.

**Not every composition exports fixing points.** Compositions built on a frame, and ready-made scenes, hang from the frame rather than from the slab; there is nothing to fix to the ceiling, and the file contains no fixing points. That is five catalogue items of the three hundred and sixty that export in full.

**Not every catalogue item is in that number.** Three hundred and sixty of the six hundred and five compositions export in full. The rest are a mixed group — wall and floor pieces, sculptural objects and showroom items that the configurator does not assemble at all, alongside suspended compositions that are quoted individually.

**There is no Revit family.** The `.rfa` format is a closed binary one; it cannot be built without Revit itself, and the brand holds no library family. The deliverable is the IFC4 file, and it opens in applications that import IFC4 — Revit, ArchiCAD, Allplan, Tekla and Navisworks among them. An application limited to IFC2x3 will not open it.

The internal shop drawings stay internal: they are for the brand's own production and its dealers.

## The point

A model is a promise about a building that has not been built yet. Every object in it that cannot keep its promise — that has no weight, no fixing, no identity — is a place where the drawing and the building will later disagree.

Decorative lighting has been one of those places for a long time. It does not have to stay that way: the information exists on the manufacturer's side, and the question is only whether it is written into the file or left in an email.

*The export page, with what the file contains and how to open it: [vargov.ru/en/configurator/ifc4](https://vargov.ru/en/configurator/ifc4)*
