---
title: "IFC4 from the configurator: what an architect gets and how to use it"
meta_title: "IFC4 Chandelier Configurator for Architects · Vargov Design"
meta_description: "Online lighting configurator with IFC4 export: build a composition for your room, download the BIM model, PDF specification and tender sheet."
suggested_url: "https://vargov.ru/en/configurator/ifc4"
lang: en
alternate: ifc4-page.ru.md
status: draft — owner approval required before publication; resolve every [уточнить …] mark first (see README.md)
---

# IFC4 from the configurator: what an architect gets and how to use it

The Vargov® Design configurator at [vargov.design](https://vargov.design/) builds a lighting or decorative composition for a specific room, in the browser. When the composition is calculated, the **Documents** block offers three files you can download without contacting us: an IFC4 model, a PDF specification and a tender sheet.

## What you download

**IFC4 model (BIM).** The composition as you configured it — geometry and properties — in the open IFC4 format, ready for the project model. It is assembled per composition, not per article: the set of elements you built for this room, not a generic catalogue item.

**PDF specification.** A printable summary of the composition for the design set and the client, with a link back to the configuration so it can be reopened later. [уточнить у агента конфигуратора: точный состав PDF-спецификации]

**Tender sheet.** The same composition written the way procurement needs it, ready for the tender documents without retyping. [уточнить у агента конфигуратора: формат и состав тендерного листа]

**DXF drawing** — not a visitor download: issued to the brand's production, dealers and partners.

## How to open the IFC4 model in Revit, ArchiCAD and other BIM software

BIM applications read IFC4 through their own IFC import or link command. Dialogs differ between products and versions, so follow your application's documentation; the sequence is the same everywhere:

1. Download the IFC file from the Documents block and keep it with the project.
2. Use the **IFC import** (or **link**) command, not "open as a native file", so your project's units and coordinates are kept.
3. Place the composition at its ceiling position; the file carries its geometry, the position in the room is yours.
4. Select any element and open its properties: the data sits in two property sets, **Vargov_Design** and **Vargov_Mount**.
5. Run your usual clash check against structure, services and the ceiling grid.

We make no promises for third-party software; if a file does not import as expected, write to us with the application name and version.

## What is inside the model

- Lit articles are exported as **IfcLightFixture**, decorative articles as **IfcFurnishingElement**. Schedules count light fixtures separately from decor without manual sorting.
- Ceiling fixing points are **separate objects** (IfcDiscreteAccessory), one per point, and each carries its own load value. [уточнить у агента конфигуратора: имя свойства нагрузки — в задании названо LoadKg, в источниках не подтверждено] A composition on cables has as many points as elements — each hangs on its own line — so the points in the file are the points you will drill (a few exception articles are listed in the [mounting-points guide](https://vargov.ru/en/guides/mounting-points)).
- Properties in Vargov_Design and Vargov_Mount: article code, number of elements and suspension points, mass, power and a link to the configuration. Property names are in English. [уточнить у агента конфигуратора: язык поля Description — по источнику пояснения на русском]
- Every number is computed from the composition's 3D model and checked automatically before each release of the configurator.

## What it is for

**Ceiling coordination.** Fixing points as objects let you check the composition against beams, ducts, sprinklers and the ceiling grid before the ceiling is closed, and move it while moving is still cheap.

**Structural nodes.** Each fixing point carries its own load, and the count of points with the average and the highest load is stated in the documents [уточнить у агента конфигуратора: в каком именно документе — по источнику это «запрос на производство»], so the structural engineer receives numbers rather than a request to "check the ceiling".

**Tender and procurement.** The tender sheet and the IFC schedule describe the same composition in two forms — for the tender documents and for model-based quantity take-off.

## Limits

- The model and its numbers are a concept-level calculation [уточнить у агента конфигуратора: формулировка «концептуальный расчёт»]; the final specification for a project is confirmed by the brand's design engineer [уточнить у агента конфигуратора]. Treat the export as coordination data, not as a signed shop drawing.
- **360 of the 605 compositions** open with a full calculation and therefore with IFC4 export. The rest — some pendant articles that are calculated individually, plus sconces, floor and wall pieces — are configured with us directly.
- There is **no Revit family (.rfa)**. The format is proprietary and we do not issue one; Revit opens the IFC4 model through IFC import or link.
- Projects are saved in your browser; there is no account.
- The suspension node is chosen by the lighting scheme, not by mass. [уточнить у агента конфигуратора: точный смысл и формулировка правила владельца; в шести файлах-источниках его нет]

## Questions and answers

**Do I need an account to export the files?** No. There is no account: the composition is built and exported in the browser, where projects are also stored. Keep the configuration link to reopen it elsewhere.

**Is the IFC file per article or per composition?** Per composition. It describes the set of elements you configured for your room, with its own fixing points and loads. Two different configurations of the same article give two different files.

**Which BIM applications open it?** Any application with IFC import — Revit, ArchiCAD, Allplan, Tekla and Navisworks among them. Use the IFC import or link command; steps vary by product and version.

**Do you provide a Revit family (.rfa)?** No. We do not issue .rfa files. The IFC4 model opens in Revit through IFC import or link.

**Can I use the exported loads for the structural calculation?** Use them for coordination and preliminary sizing of the nodes. The calculation is concept-level [уточнить] and the final specification is confirmed by the brand's engineer [уточнить] before production.

**Why are decorative elements not IfcLightFixture?** Because they do not emit light. Exporting them as IfcFurnishingElement keeps the lighting schedule honest: only lit articles appear in it.

**Can I download the DXF drawing?** DXF drawings are issued to the brand's production, dealers and partners. Visitors export the IFC4 model, the PDF specification and the tender sheet.

## Open the configurator

Start from any composition — for example [vargov.design/?sku=LC0173](https://vargov.design/?sku=LC0173) [уточнить у агента конфигуратора: LC0173 входит в 360 открытых с расчётом] — or from the [catalogue](https://vargov.ru/en/catalog). The Russian version is at [configurator.vargov.ru](https://configurator.vargov.ru/). Project questions: info@vargov.ru.

Related: [How a bespoke project runs](https://vargov.ru/en/architects) · [Mounting points](https://vargov.ru/en/guides/mounting-points) · [Installation guide, PDF](https://vargov.ru/pdf/vargov-installation-en.pdf) · [About the configurator](https://vargov.ru/en/configurator)

Vargov® Design — author's lighting and decorative compositions, own production, made to order; 605 compositions, 25 international awards. The 3D configurator is an Awwwards Nominee 2026.

---

## JSON-LD (FAQPage + WebApplication) — separate block for the page head

Questions and answers below must match the visible text word for word after the [уточнить …] marks are resolved. Page URL is a placeholder until the site agent assigns one.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebApplication",
      "@id": "https://vargov.design/#webapplication",
      "name": "Vargov®Design 3D Configurator",
      "url": "https://vargov.design/",
      "sameAs": ["https://configurator.vargov.ru/"],
      "description": "Online configurator that builds a lighting or decorative composition for a specific room in the browser and exports an IFC4 (BIM) model, a PDF specification and a tender sheet.",
      "applicationCategory": "DesignApplication",
      "operatingSystem": "Web browser",
      "browserRequirements": "Requires JavaScript",
      "inLanguage": ["en", "ru"],
      "featureList": [
        "Composition built for a specific room",
        "IFC4 (BIM) export per composition: IfcLightFixture for lit articles, IfcFurnishingElement for decorative articles, ceiling fixing points as separate objects with a load per point",
        "PDF specification",
        "Tender sheet",
        "Direct launch by article code, e.g. https://vargov.design/?sku=LC0173"
      ],
      "provider": { "@id": "https://vargov.ru#organization" }
    },
    {
      "@type": "FAQPage",
      "@id": "https://vargov.ru/en/configurator/ifc4#faq",
      "url": "https://vargov.ru/en/configurator/ifc4",
      "name": "IFC4 from the configurator: what an architect gets and how to use it",
      "inLanguage": "en",
      "about": { "@id": "https://vargov.design/#webapplication" },
      "publisher": { "@id": "https://vargov.ru#organization" },
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Do I need an account to export the files?",
          "acceptedAnswer": { "@type": "Answer", "text": "No. There is no account: the composition is built and exported in the browser, where projects are also stored. Keep the configuration link to reopen it elsewhere." }
        },
        {
          "@type": "Question",
          "name": "Is the IFC file per article or per composition?",
          "acceptedAnswer": { "@type": "Answer", "text": "Per composition. It describes the set of elements you configured for your room, with its own fixing points and loads. Two different configurations of the same article give two different files." }
        },
        {
          "@type": "Question",
          "name": "Which BIM applications open it?",
          "acceptedAnswer": { "@type": "Answer", "text": "Any application with IFC import — Revit, ArchiCAD, Allplan, Tekla and Navisworks among them. Use the IFC import or link command; steps vary by product and version." }
        },
        {
          "@type": "Question",
          "name": "Do you provide a Revit family (.rfa)?",
          "acceptedAnswer": { "@type": "Answer", "text": "No. We do not issue .rfa files. The IFC4 model opens in Revit through IFC import or link." }
        },
        {
          "@type": "Question",
          "name": "Can I use the exported loads for the structural calculation?",
          "acceptedAnswer": { "@type": "Answer", "text": "Use them for coordination and preliminary sizing of the nodes. The calculation is concept-level and the final specification is confirmed by the brand's engineer before production." }
        },
        {
          "@type": "Question",
          "name": "Why are decorative elements not IfcLightFixture?",
          "acceptedAnswer": { "@type": "Answer", "text": "Because they do not emit light. Exporting them as IfcFurnishingElement keeps the lighting schedule honest: only lit articles appear in it." }
        },
        {
          "@type": "Question",
          "name": "Can I download the DXF drawing?",
          "acceptedAnswer": { "@type": "Answer", "text": "DXF drawings are issued to the brand's production, dealers and partners. Visitors export the IFC4 model, the PDF specification and the tender sheet." }
        }
      ]
    }
  ]
}
```
