---
title: "Why a lighting studio exports IFC4 before you place an order"
subtitle: "What an architect gets from our configurator, scene by scene — and what the file does not do"
author: Anton Vargov, founder and lead designer, Vargov® Design
channel: Medium (long version of the LinkedIn article)
target_length: 1000–1300 words
status: approved by the owner 28.09.2026 ("норм") — publish not before the configurator release of 1 October 2026; who posts on Medium is the owner's call (see README.md)
---

# Why a lighting studio exports IFC4 before you place an order

*What an architect gets from our configurator, scene by scene — and what the file does not do.*

## The question that arrives before the order

Every project that reaches our studio starts with a picture and ends with a drawing. In between there is a question that architects ask early and that we, for years, answered late: "What does this do to my ceiling?"

The old order was the usual one. An architect sends a sketch, we agree on a composition, the contract is signed, and only then our engineer draws the mounting scheme with the fixing points and the loads. It worked. It also had a flaw that I only saw from the other side of the table: the drawing arrived after every decision that depended on it had already been made. The ceiling had been closed, the structural engineer had signed off, the tender had gone out. Our drawing was correct and useless.

## What "IFC4 before the order" means

In September 2026 we moved that step to the front. The configurator at vargov.design builds a lighting or decorative composition for a specific room, in the browser. Once the composition is calculated, the Documents block offers three files: an IFC4 model, a PDF specification and a tender sheet. No account, no request form, no waiting for us. Projects are kept in the visitor's browser.

The IFC4 file is assembled per composition, not per article. It is not a catalogue object; it is the exact set of elements you configured for this room, with its own fixing points and its own loads. Configure the same article twice for two rooms and you get two different files.

Inside, lit articles are IfcLightFixture and decorative articles are IfcFurnishingElement. Ceiling fixing points are separate objects, one per point, each with its own load value. The properties — article code, elements and suspension points, mass, power, a link back to the configuration — sit in two property sets, Vargov_Design and Vargov_Mount.

Here are the scenes that convinced me it was worth doing.

## Scene one: the ceiling section

An architect is working on a stairwell. The composition she wants is a cloud of elements, each hanging on its own cable. Her ceiling section already has a beam, a duct and two sprinkler lines. Her question is not how the composition looks but where exactly the cables land and which of them meet the duct.

A rendering cannot answer that. A model in which every fixing point is a separate object can, in her own file, with her own clash check, on the day she asks. When we checked the export in September, a composition of twenty-seven elements came out as twenty-seven light fixtures and twenty-seven fixing points; we opened the file and counted them, because a claim about a file should be checked in the file.

## Scene two: the engineer's e-mail

It always says the same thing: "What is the load on the ceiling?"

With a single-body fitting the answer is easy: the whole mass arrives at one node. A composition on cables is different. The load is spread across many points, and a lit element hangs on a wire while a decorative one hangs on a cable. In the export each fixing point carries its suspension type and its own load in kilograms, and the specification — in the configurator, the PDF and the tender sheet — states the number of points with the average and the highest load. The engineer receives numbers to check rather than a request to "have a look at the ceiling".

## Scene three: the bill of quantities

A quantity surveyor needs a schedule, and a schedule needs categories. Because lit articles come out as IfcLightFixture and decorative ones as IfcFurnishingElement, the lighting schedule counts what emits light and nothing else, without anyone sorting rows by hand. The tender sheet is the same composition written the way a tender wants it, so it goes into the documents without retyping.

## Scene four: Thursday's change

The reception desk moves, and the space above it that the composition may occupy changes with it. In the old order that meant a call to us, a wait and a new drawing. Now it means reopening the configuration, adjusting it and exporting again. The change is cheap because nothing has been ordered yet — the whole point of moving the export to the front.

## What the file does not do

I would rather list the limits myself than have you find them.

The numbers are a concept-level calculation, and every PDF and tender sheet says so in its footer: "Calculations are conceptual; the final specification is confirmed by the brand engineer." Treat the file as coordination data, not as a signed shop drawing.

We do not issue a Revit family. The .rfa format is proprietary, and I would rather hand over an open format that Revit, ArchiCAD, Allplan, Tekla and Navisworks read through their IFC import than promise what we cannot make properly.

Today 360 of our 605 compositions open with a full calculation and therefore with the export. The rest — some pendant articles that are calculated individually, plus sconces, floor and wall pieces — we configure with you directly.

The DXF drawing exists but is for internal use only: the brand's production and dealers. The visitor's three files are the IFC4 model, the PDF specification and the tender sheet.

## Two things from the launch week

Every number in the file is computed from the 3D model and checked automatically before each release of the configurator.

First, one of those checks flagged thirty-four decorative articles whose cable load was above the limit we publish. We did not raise the limit: since 17 September a heavy element gets several lines of the same type instead of one line beyond its limit. A studio would rather not mention such a finding; a check that catches its own product is the only kind worth having.

Second, the first version of the export named its property sets with the Pset_ prefix, which the IFC standard reserves for its own sets. A validator rejected the file, and some applications would have hidden exactly the properties that make the export useful. We renamed the sets to Vargov_Design and Vargov_Mount the same day and added that validator to the checks that run before every release. I mention it because "we export IFC4" is easy to say and easy to get subtly wrong.

## Why a studio bothers

I will not pretend this is altruism. An architect who already has the composition sitting in the model is less likely to swap it for something else when the budget is trimmed: the swap costs work. That is our interest.

The architect's interest is that the fixing points are in the model before the ceiling is closed, that the structural engineer gets numbers, and that the tender goes out with a schedule that counts correctly. The file serves both interests at once, and I think that is the only reason it works. A file that served only ours would not be opened twice.

## How to try it

Open any composition in the configurator — for example vargov.design/?sku=LC0173 — build it for your room, open Documents and download the IFC4 model. Import it into your BIM application with the IFC import or link command, place it at its ceiling position and run your clash check. If the article you need does not open with a calculation yet, write to info@vargov.ru and we will configure it with you.

*Anton Vargov is the founder and lead designer of Vargov® Design — author's lighting and decorative compositions, own production, made to order; 605 compositions in the catalogue, 25 international awards.*
