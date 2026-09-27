---
title: "Why a lighting studio exports IFC4 before you place an order"
author: Anton Vargov, founder and lead designer, Vargov® Design
channel: LinkedIn article (founder's profile)
target_length: 600–800 words
status: draft — first-person text, owner must read and approve every sentence; not before the configurator release of 1 October 2026 (see README.md)
---

# Why a lighting studio exports IFC4 before you place an order

For years the order of things in our studio was the usual one. An architect sends a sketch, we agree on a composition, a contract is signed, and only then our engineer draws the mounting scheme with the fixing points and the loads. It worked. It also had a flaw I only noticed from the other side of the table: the drawing arrived after every decision that depended on it had already been made.

In September 2026 we moved that step to the front. The configurator at vargov.design now exports an IFC4 model of the composition you build in it — before any contact with us and before any order. Alongside it come a PDF specification and a tender sheet. Here is what convinced me, scene by scene.

**The ceiling section.** An architect is working on a stairwell. The composition she wants is a cloud of elements, each hanging on its own cable. Her ceiling section already has a beam, a duct and two sprinkler lines. Her question is not how it looks but where exactly the cables land and which of them meet the duct. A rendering cannot answer that. A model in which every fixing point is a separate object can — in her own file, with her own clash check, on the day she asks. In the IFC4 export the fixing points are exactly that. When we checked the export in September, a composition of twenty-seven elements came out as twenty-seven light fixtures and twenty-seven fixing points — we opened the file and counted.

**The engineer's e-mail.** It always says the same thing: "What is the load on the ceiling?" A single-body fitting brings its whole mass to one node; easy. A composition on cables is different: the load is spread across many points. Each fixing point in the model carries its own load in kilograms, and the specification states how many points there are, with the average and the highest load. The engineer gets numbers to check, not a request to "have a look at the ceiling".

**The bill of quantities.** A quantity surveyor needs a schedule, and a schedule needs categories. In the export, lit articles are IfcLightFixture and decorative ones are IfcFurnishingElement. The lighting schedule then counts what emits light and nothing else, without anyone sorting rows by hand. The tender sheet is the same composition written the way a tender wants it.

**Thursday's change.** The reception desk moves, and the space above it that the composition may occupy changes with it. In the old order that meant a call to us, a wait, and a new drawing. Now it means reopening the configuration, adjusting it and exporting again. Projects are kept in the browser; there is no account and nothing to wait for.

**What I will not claim.** The numbers are a concept-level calculation, and every PDF and tender sheet says so in its footer: "Calculations are conceptual; the final specification is confirmed by the brand engineer." Treat the file as coordination data, not as a signed shop drawing. We do not issue a Revit family: .rfa is proprietary, and I would rather hand over an open format that Revit, ArchiCAD and others import than promise what we cannot make properly. Today 360 of our 605 compositions open with a full calculation and therefore with the export; the others we configure with you. The DXF drawing stays with production, dealers and partners.

**One more thing I would rather say myself.** Every number in the file is computed from the 3D model and checked automatically before each release. In the launch week one of those checks flagged thirty-four decorative articles whose cable load was above the limit we publish. We did not raise the limit: since 17 September a heavy element gets several lines of the same type instead of one line beyond its limit. A studio would rather not mention such a finding. I do: a check that catches its own product is the only kind worth having, and I would rather you heard it from me.

**Why we do it.** I will not pretend it is altruism. An architect who already has the composition sitting in the model is less likely to swap it for something else when the budget is trimmed — the swap costs work. That is our interest. The architect's interest is that the fixing points are in the model before the ceiling is closed. The file serves both, and that is the only reason it works.

Try it on any composition: vargov.design/?sku=LC0173. If the article you need does not open with a calculation yet, write to me.

*Anton Vargov, founder and lead designer, Vargov® Design — author's lighting and decorative compositions, own production, made to order.*
