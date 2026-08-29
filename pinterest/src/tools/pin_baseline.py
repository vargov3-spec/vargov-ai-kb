# -*- coding: utf-8 -*-
"""Базовая линия Pinterest: показы, переходы на сайт, сохранения по неделям.

Считаем понедельно, а не подённо: дневные числа скачут в разы из-за
расписания публикаций, и по ним нельзя отличить рост от совпадения.
"""
import io
import json
from collections import defaultdict
from datetime import date

RAW = json.load(io.open("pin_rows.json", encoding="utf-8"))["rows"]

# строка: [показы, переходы на сайт, сохранения, YYYYMMDD]
days = {}
for imp, out, sav, d in RAW:
    dt = date(int(d[:4]), int(d[4:6]), int(d[6:]))
    days[dt] = (float(imp), float(out), float(sav))

weeks = defaultdict(lambda: [0.0, 0.0, 0.0, 0])
for dt, (imp, out, sav) in days.items():
    monday = dt.toordinal() - dt.weekday()
    w = weeks[date.fromordinal(monday)]
    w[0] += imp
    w[1] += out
    w[2] += sav
    w[3] += 1

out_lines = []
out_lines.append("неделя с   | дней | показы    | на сайт | сохран. | показ/день | CTR на сайт")
out_lines.append("-" * 84)
ordered = sorted(weeks.items())
for wk, (imp, outc, sav, n) in ordered:
    ctr = (outc / imp * 100) if imp else 0.0
    out_lines.append(
        "%s | %4d | %9.0f | %7.0f | %7.0f | %10.0f | %.4f%%"
        % (wk.isoformat(), n, imp, outc, sav, imp / n, ctr)
    )

# сравнение: первый полный месяц данных против последних 14 дней
first = [v for k, v in sorted(days.items())][:30]
last = [v for k, v in sorted(days.items())][-14:]
def avg(rows, i):
    return sum(r[i] for r in rows) / len(rows)

out_lines.append("")
out_lines.append("СРАВНЕНИЕ")
out_lines.append("  первые 30 дней наблюдений: показы/день %8.0f | на сайт/день %5.1f | сохран./день %5.1f"
                 % (avg(first, 0), avg(first, 1), avg(first, 2)))
out_lines.append("  последние 14 дней:         показы/день %8.0f | на сайт/день %5.1f | сохран./день %5.1f"
                 % (avg(last, 0), avg(last, 1), avg(last, 2)))
if avg(first, 0):
    out_lines.append("  рост показов: x%.1f" % (avg(last, 0) / avg(first, 0)))
if avg(first, 1):
    out_lines.append("  рост переходов на сайт: x%.1f" % (avg(last, 1) / avg(first, 1)))

out_lines.append("")
out_lines.append("ВСЕГО дней с данными: %d, с %s по %s"
                 % (len(days), min(days).isoformat(), max(days).isoformat()))

io.open("baseline.txt", "w", encoding="utf-8").write("\n".join(out_lines))
print("\n".join(out_lines[-8:]))
