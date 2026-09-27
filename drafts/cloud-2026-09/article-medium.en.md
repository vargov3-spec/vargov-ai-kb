---
title: "Why a lighting studio exports IFC4 before you place an order"
subtitle: "What an architect gets from our configurator, scene by scene — and what the file does not do"
author: Anton Vargov, founder and lead designer, Vargov® Design
channel: Medium (long version of the LinkedIn article)
target_length: 1000–1300 words
status: draft — first-person text, owner must read and approve every sentence; resolve [уточнить …] marks first (see README.md)
---

# Why a lighting studio exports IFC4 before you place an order

*What an architect gets from our configurator, scene by scene — and what the file does not do.*

## The question that arrives before the order

Every project that reaches our studio starts with a picture and ends with a drawing. In between there is a question that architects ask early and that we, for years, answered late: "What does this do to my ceiling?"

The old order was the usual one. An architect sends a sketch, we agree on a composition, the contract is signed, and only then our engineer draws the mounting scheme with the fixing points and the loads. It worked. It also had a flaw that I only saw from the other side of the table: the drawing arrived after every decision that depended on it had already been made. The ceiling had been closed, the structural engineer had signed off, the tender had gone out. Our drawing was correct and useless.

## What "IFC4 before the order" means

In September 2026 we moved that step to the front. The configurator at vargov.design builds a lighting or decorative composition for a specific room, in the browser. Once the composition is calculated, the Documents block offers three files: an IFC4 model, a PDF specification and a tender sheet. No account, no request form, no waiting for us. Projects are kept in the visitor's browser.

The IFC4 file is assembled per composition, not per article. It is not a catalogue object; it is the exact set of elements you configured for this room, with its own fixing points and its own loads. Configure the same article twice for two rooms and you get two different files.

Inside, lit articles are IfcLightFixture and decorative articles are IfcFurnishingElement. Ceiling fixing points are separate objects, one per point, each with its own load value. The properties — article code, number of elements and suspension points, mass, power, a link back to the configuration — sit in two property sets, Vargov_Design and Vargov_Mount, which a BIM application shows in its property panel after an IFC import.

Here are the scenes that convinced me it was worth doing.

## Scene one: the ceiling section

An architect is working on a stairwell. The composition she wants is a cloud of elements, each hanging on its own cable. Her ceiling section already has a beam, a duct and two sprinkler lines. Her question is not whether the composition will look good — she can see that — but where exactly the cables land and which of them meet the duct.

A rendering cannot answer that. A model in which every fixing point is a separate object can, in her own file, with her own clash check, on the day she asks. A composition of twenty-seven elements exports as twenty-seven light fixtures and twenty-seven fixing points; we opened an exported file and counted them, because a claim about a file should be checked in the file.

## Scene two: the engineer's e-mail

It always says the same thing: "What is the load on the ceiling?"

With a single-body fitting the answer is easy: the whole mass arrives at one node. A composition on cables is different. Each element hangs on its own line, so the load is spread across as many points as there are elements — a few articles are exceptions, and we list them by code in a guide on the site. In the export each fixing point carries its own load, and the documents state the number of points with the average and the highest load [уточнить у агента конфигуратора: в каком документе]. The engineer receives numbers to check rather than a request to "have a look at the ceiling".

## Scene three: the bill of quantities

A quantity surveyor needs a schedule, and a schedule needs categories. Because lit articles come out as IfcLightFixture and decorative ones as IfcFurnishingElement, the lighting schedule counts what emits light and nothing else, without anyone sorting rows by hand. The tender sheet is the same composition written the way a tender wants it, so it goes into the documents without retyping.

## Scene four: Thursday's change

The reception desk moves, and the space above it that the composition may occupy changes with it. In the old order that meant a call to us, a wait and a new drawing. Now it means reopening the configuration, adjusting the composition to the new space and exporting again. The change is cheap because it happens before anything has been ordered, and that is the whole point of moving the export to the front.

## What the file does not do

I would rather list the limits myself than have you find them.

The numbers in the export are a concept-level calculation [уточнить у агента конфигуратора: формулировка]; the final specification for a project is confirmed by our engineer [уточнить у агента конфигуратора]. Treat the file as coordination data, not as a signed shop drawing.

We do not issue a Revit family. The .rfa format is proprietary, and I would rather hand over an open format that Revit, ArchiCAD, Allplan, Tekla and Navisworks read through their IFC import than promise something we cannot make properly.

Today 360 of our 605 compositions open with a full calculation and therefore with the export. The rest — some pendant articles that are calculated individually, plus sconces, floor and wall pieces — we configure with you directly.

The DXF drawing exists but stays with production, dealers and partners of the brand. The visitor's three files are the IFC4 model, the PDF specification and the tender sheet.

## Two things from the launch week

Every number in the file is computed from the 3D model and checked automatically before each release of the configurator.

First, one of those checks flagged thirty-four decorative articles whose cable load was above the limit we publish [уточнить у агента конфигуратора: чем это закончилось для 34 артикулов — исправлены или закрыты от расчёта]. A studio would rather not mention such a finding; a check that catches its own product is the only kind worth having.

Second, the first version of the export named its property sets with the Pset_ prefix, which the IFC standard reserves for its own sets. A validator rejected the file, and some applications would have hidden exactly the properties that make the export useful. We renamed the sets to Vargov_Design and Vargov_Mount the same day and added that validator to the checks that run before every release. I mention it because "we export IFC4" is easy to say and easy to get subtly wrong.

## Why a studio bothers

I will not pretend this is altruism. An architect who already has the composition sitting in the model is less likely to swap it for something else when the budget is trimmed: the swap costs work. That is our interest.

The architect's interest is that the fixing points are in the model before the ceiling is closed, that the structural engineer gets numbers, and that the tender goes out with a schedule that counts correctly. The file serves both interests at once, and I think that is the only reason it works. A file that served only ours would not be opened twice.

## How to try it

Open any composition in the configurator — for example vargov.design/?sku=LC0173 [уточнить у агента конфигуратора: LC0173 входит в 360 открытых с расчётом] — build it for your room, open Documents and download the IFC4 model. Import it into your BIM application with the IFC import or link command, place it at its ceiling position and run your clash check. If the article you need does not open with a calculation yet, write to us at info@vargov.ru and we will configure it with you.

*Anton Vargov is the founder and lead designer of Vargov® Design — author's lighting and decorative compositions, own production, made to order; 605 compositions in the catalogue, 25 international awards.*
