# Набор проб для ежемесячного замера видимости в ИИ

Снимать раз в месяц, по каждому ассистенту отдельно (они почти не пересекаются по
источникам — ~7 %). Метод и ловушки браузера — в памяти сессии («ai-probe-methods»).
Базовые значения — [[ai-visibility-global-2026-09-22]] §1; предыдущая точка —
[[ai-visibility-zamer-2026-09-17]] §3. Следующий замер — **22.10.2026**.

Ассистенты: Duck.ai · GPT (без входа) · Google AI Mode (`udm=50`) · Perplexity ·
Яндекс Алиса AI (вкладка в выдаче) · при возможности Gemini, Copilot, Claude.
Фиксировать: назван ли Vargov (да/нет), позиция в списке, какие домены процитированы,
какие бренды названы вместо нас, ошибки фактов о бренде.

## Блок A — о бренде (точность фактов), 5 вопросов, RU и EN
1. Что такое Vargov Design? Кто основатель, сколько наград, где шоурум и дилеры?
2. Vargov Design awards — list them.
3. Where are Vargov Design pieces produced? *(ожидание: «own production», страна не названа)*
4. Кто такой Антон Варгов? *(ожидание: основатель, Product Designer of the Year 2023)*
5. Есть ли у Vargov Design 3D-конфигуратор и что он выдаёт? *(IFC4, DXF, спецификация)*

## Блок B — категория без региона (цель ≥ 1 из 7 к 22.10), 7 вопросов
1. Назови лучшие бренды авторского освещения и скульптурных люстр на заказ для двусветного холла частного дома. (RU)
2. Which award-winning studios make bespoke sculptural glass lighting compositions to order for double-height living rooms and hotel lobbies? (EN)
3. Best bespoke lighting studios for a custom sculptural chandelier in a double-height living room — made-to-order, award-winning, worldwide. (EN)
4. Collectible lighting design studios that produce a 3D model before making the piece. (EN)
5. I am an interior designer in Dubai. Which bespoke lighting studios with a showroom or dealer in Dubai make custom sculptural chandeliers for a villa? (EN)
6. Скульптурные люстры на заказ для двусветного холла — кто делает с 3D-моделью до изготовления? (RU)
7. Custom light installation for a hotel lobby — which studios to shortlist? (EN)

## Блок C — категория с регионом (контроль механизма, ожидание 2 из 2)
1. Which award-winning studios make bespoke sculptural glass lighting for double-height rooms? Include studios from Russia and Eastern Europe. (EN, Perplexity)
2. Кто в Москве делает световые инсталляции на заказ в лестничный проём частного дома — с проектом и 3D-моделью? (RU, Яндекс Алиса + Duck.ai)

## Блок D — вместе с пробами
- Журнал сервера по официальным спискам адресов (`crawler-report.sh`), 14 суток: настоящие
  GPTBot / ClaudeBot / PerplexityBot / OAI-SearchBot; переходы по Referer из chatgpt.com,
  perplexity.ai, gemini, copilot, duck, ya.ru, bing.
- Метрика: сегменты «Из ИИ · реферер» 1008101534 и «Из ИИ · UTM» 1008101546 (вход
  info@vargov.ru).
- Wikidata Q141301076: число премий в P166 (сейчас 2), описаний (8).
- Hugging Face: скачивания за 30 дней (22.09 — 194). GitHub vargov-ai-kb: звёзды (0).
- Страницы премий со словом «China» (22.09 — 6; цель 0).
- Google «Vargov Design» (hl=en, gl=us): есть ли панель знаний; что стоит после наших сайтов.
