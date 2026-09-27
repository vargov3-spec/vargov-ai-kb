---
title: "IFC4 from the configurator: what an architect gets and how to use it"
meta_title: "IFC4 Chandelier Configurator for Architects · Vargov Design"
meta_description: "Online lighting configurator with IFC4 export: build a composition for your room, download the BIM model, PDF specification and tender sheet."
suggested_url: "https://vargov.ru/en/configurator/ifc4"
lang: en
alternate: ifc4-page.ru.md
status: draft — owner approval required before publication; not before the configurator release of 1 October 2026, when the list of 360 calculated articles goes live (see README.md)
---

# IFC4 from the configurator: what an architect gets and how to use it

The Vargov® Design configurator at [vargov.design](https://vargov.design/) builds a lighting or decorative composition for a specific room, in the browser. When the composition is calculated, the **Documents** block gives you three documents without contacting us: an IFC4 model, a PDF specification and a tender sheet.

## What you download

**IFC4 model (BIM).** The composition as you configured it — geometry and properties — in the open IFC4 format, ready for the project model. It is assembled per composition, not per article.

**PDF specification.** A printable summary for the design set and the client: a 3D view, a QR code that reopens this configuration, and the specification — article, form, number of elements, dimensions, mass, power, mounting with the load per point. It opens in a new window; your browser saves it as PDF.

**Tender sheet.** The same composition as a dated specification for procurement — item and quantity, technical data, fixing points with the load per point, scope of supply, manufacturer details, customs code, conformity documents — ready for the tender documents without retyping. It also opens in a new window.

**DXF drawing** — not a visitor download: for internal use only, by the brand's production and dealers.

## How to open the IFC4 model in Revit, ArchiCAD and other BIM software

BIM applications read IFC4 through their own import or link command; dialogs differ by product and version, but the sequence is the same:

1. Download the IFC file from the Documents block and keep it with the project.
2. Use **IFC import** (or **link**), not "open as a native file", so your units and coordinates are kept.
3. Place the composition at its ceiling position; the file carries the geometry, the position is yours.
4. Select any element: the data sits in two property sets, **Vargov_Design** and **Vargov_Mount**.
5. Run your usual clash check against structure, services and the ceiling grid.

If a file does not import as expected, write to us with the application name and version.

## What is inside the model

- Lit articles are exported as **IfcLightFixture**, decorative articles as **IfcFurnishingElement**.
- Ceiling fixing points are **separate objects** (IfcDiscreteAccessory), one per point, each with its own **Vargov_Mount** set: `SuspensionType` (on a wire or on a cable), `ElementsAtPoint` and `LoadKg` — the load on that point in kilograms (the unit is in the name: the file's units carry no mass). The points in the file are the points you will drill ([how points are counted](https://vargov.ru/en/guides/mounting-points)).
- The suspension follows the light: a lit element hangs on a wire, a decorative one on a cable; the specification counts wires and cables in its Mounting line.
- Properties in Vargov_Design and Vargov_Mount: article code, number of elements and suspension points, mass, power and a link to the configuration. Property names are in English, their descriptions in Russian.
- Every number is computed from the 3D model and checked automatically before each release.

## What it is for

**Ceiling coordination.** Fixing points as objects let you check the composition against beams, ducts, sprinklers and the ceiling grid before the ceiling is closed, and move it while moving is still cheap.

**Structural nodes.** Each fixing point carries its own load, and the specification states the number of points with the average and the highest load, so the structural engineer receives numbers rather than a request to "check the ceiling".

**Tender and procurement.** The tender sheet and the IFC schedule describe the same composition — one for the tender documents, one for quantity take-off.

## Limits

- The model and its numbers are a concept-level calculation. The footer of every PDF specification and tender sheet says so: "Calculations are conceptual; the final specification is confirmed by the brand engineer." Treat the export as coordination data, not as a signed shop drawing.
- **360 of the 605 compositions** open with a full calculation and therefore with IFC4 export. The rest — some pendant articles calculated individually, plus sconces, floor and wall pieces — we configure with you.
- There is **no Revit family (.rfa)**. The format is proprietary and we do not issue one; Revit opens the IFC4 model through IFC import or link.

## Questions and answers

**Do I need an account to export the files?** No. There is no account: the composition is built and exported in the browser, where projects are also stored. Keep the configuration link to reopen it elsewhere.

**Is the IFC file per article or per composition?** Per composition. It describes the set of elements you configured for your room, with its own fixing points and loads. Two different configurations of the same article give two different files.

**Which BIM applications open it?** Any application with IFC import — Revit, ArchiCAD, Allplan, Tekla and Navisworks among them — through their IFC import or link command.

**Do you provide a Revit family (.rfa)?** No. We do not issue .rfa files. The IFC4 model opens in Revit through IFC import or link.

**Can I use the exported loads for the structural calculation?** Use them for coordination and preliminary sizing of the nodes. The calculation is conceptual, and the final specification is confirmed by the brand engineer before production.

**Why are decorative elements not IfcLightFixture?** Because they do not emit light. Exporting them as IfcFurnishingElement keeps the lighting schedule honest: only lit articles appear in it.

**Can I download the DXF drawing?** DXF drawings are for internal use only: the brand's production and dealers. Visitors export the IFC4 model, the PDF specification and the tender sheet.

## Open the configurator

Start from any composition — for example [vargov.design/?sku=LC0173](https://vargov.design/?sku=LC0173) — or from the [catalogue](https://vargov.ru/en/catalog). The Russian version is at [configurator.vargov.ru](https://configurator.vargov.ru/). Project questions: info@vargov.ru.

Related: [How a bespoke project runs](https://vargov.ru/en/architects) · [Mounting points](https://vargov.ru/en/guides/mounting-points) · [Installation guide, PDF](https://vargov.ru/pdf/vargov-installation-en.pdf) · [About the configurator](https://vargov.ru/en/configurator)

Vargov® Design — author's lighting and decorative compositions, own production, made to order; 605 compositions, 25 international awards. The 3D configurator is an Awwwards Nominee 2026.

---

## JSON-LD (FAQPage + WebApplication) — separate block for the page head

Questions and answers below must match the visible text word for word. Page URL is a placeholder until the site agent assigns one.

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
          "acceptedAnswer": { "@type": "Answer", "text": "Any application with IFC import — Revit, ArchiCAD, Allplan, Tekla and Navisworks among them — through their IFC import or link command." }
        },
        {
          "@type": "Question",
          "name": "Do you provide a Revit family (.rfa)?",
          "acceptedAnswer": { "@type": "Answer", "text": "No. We do not issue .rfa files. The IFC4 model opens in Revit through IFC import or link." }
        },
        {
          "@type": "Question",
          "name": "Can I use the exported loads for the structural calculation?",
          "acceptedAnswer": { "@type": "Answer", "text": "Use them for coordination and preliminary sizing of the nodes. The calculation is conceptual, and the final specification is confirmed by the brand engineer before production." }
        },
        {
          "@type": "Question",
          "name": "Why are decorative elements not IfcLightFixture?",
          "acceptedAnswer": { "@type": "Answer", "text": "Because they do not emit light. Exporting them as IfcFurnishingElement keeps the lighting schedule honest: only lit articles appear in it." }
        },
        {
          "@type": "Question",
          "name": "Can I download the DXF drawing?",
          "acceptedAnswer": { "@type": "Answer", "text": "DXF drawings are for internal use only: the brand's production and dealers. Visitors export the IFC4 model, the PDF specification and the tender sheet." }
        }
      ]
    }
  ]
}
```
