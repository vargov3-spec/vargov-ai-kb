# Куда подать конфигуратор без оплаты + как обойти оплату CSSDA/FWA

*Подготовлено 2026-07-28, после подачи на Awwwards. CSSDA и FWA не прошли по оплате (Stripe/PayPal не принимают российские карты).*

---

## 1. Как всё-таки оплатить CSSDA и FWA

Три рабочих варианта, по возрастанию хлопот:

**Запросить инвойс.** Написать в поддержку (CSSDA — `hello@cssdesignawards.com`, FWA — через форму на сайте) и попросить invoice для оплаты банковским переводом от юрлица. Обе премии регулярно так работают с агентствами. Формулировка: *«Our card issuer does not support your payment provider. Could you issue an invoice for a bank transfer? We are a manufacturer submitting our own product.»* Дальше платёж возможен со счёта иностранного контрагента, если он у вас есть.

**Оплатить картой партнёра за рубежом.** Премии не проверяют совпадение плательщика и автора работы — оплатить может кто угодно. Это самый быстрый путь, если есть знакомый дизайнер или клиент в ЕС.

**Через дилера/представителя.** Если у вас есть партнёр-салон за границей, подача от его имени с указанием вас в credits — обычная практика, а заодно и его маркетинг.

---

## 2. Бесплатные публикации — подавать прямо сейчас

Все ниже принимают заявки без оплаты. По совокупности они дают больше трафика от целевой аудитории (архитекторы, дизайнеры, разработчики), чем одна платная премия.

| Площадка | Что это | Как подать |
|---|---|---|
| **Siteinspire** | эталонная кураторская галерея веб-дизайна | ⚠️ только из личного кабинета (siteinspire.com/signin) |
| **Godly** | подборка «сайты уровня выше среднего» | ⚠️ переехал на recent.design, открытой формы нет |
| **Land-book** | галерея лендингов и продуктовых сайтов | ⚠️ только из личного кабинета (land-book.com/register) |
| **Httpster** | неформальная, но с большим охватом | ⛔ «Submissions are currently closed» |
| **Muzli** | лента Muzli в Chrome — десятки тысяч дизайнеров ежедневно | ⚠️ формы нет: лента собирается автоматически |
| **Codrops Collective** | еженедельная подборка для фронтенд-разработчиков; WebGL-проекты берут охотно | tympanus.net/codrops — форма «Submit» |
| **three.js Showcase** | официальная витрина three.js на threejs.org | PR в репозиторий three.js (файл `files/showcase.json`) |
| **Product Hunt** | запуск продукта, приводит первых пользователей | producthunt.com — нужен аккаунт с историей или «хантер» |
| **Hacker News (Show HN)** | техническая аудитория, ценит движок и математику | news.ycombinator.com — заголовок «Show HN: …» |
| **Reddit** | r/threejs, r/webgl, r/InteriorDesign, r/Design | пост со ссылкой и коротким описанием |
| **Behance** | портфолио-кейс с картинками; попадание в Curated Gallery даёт охват | behance.net |

---

## 3. Готовые тексты для быстрой подачи

**Одна строка (для галерей):**
> A generative 3D configurator that turns hand-blown glass into buildable light installations — in the browser, in real time, in AR.

**Абзац (для Siteinspire / Godly / Land-book):**
> Vargov®Design's configurator turns artisan glass lighting into a real-time design tool. Architects set the ceiling dimensions, pick one of twenty cloud shapes and a density — a generative engine arranges up to 1500 hand-blown glass elements, guarantees that no element or suspension cable ever intersects another piece of glass, and exports AutoCAD drawings, a spec sheet and an AR model that hangs the composition from the client's own ceiling.

**Заголовок для Show HN:**
> Show HN: A browser configurator that packs 1500 hand-blown glass elements without collisions

**Первый комментарий для Show HN / Reddit (техническая аудитория ценит именно это):**
> I build lighting installations from hand-blown glass. Every composition used to be laid out manually by our engineer. This tool does it in the browser: a packing engine places up to 1500 elements under a hard manufacturing constraint — no two pieces of glass may intersect, and no suspension cable may pass through another element. Placement is calibrated against 436 archived factory orders, so the on-screen result is manufacturable as drawn. Exports go out as DXF, a PDF spec with a QR code, a shareable URL and an AR model (USDZ/GLB). Happy to answer questions about the packing math.

**Product Hunt tagline (60 знаков):**
> Design a glass light installation for your ceiling in 60 seconds

---

## 4. Проверка площадок 2026-07-28

Прошёл по всем пяти адресам. Итог: **ни одну заявку нельзя отправить без входа в аккаунт**, а две площадки в принципе закрыты:

- **Httpster** — на сайте прямым текстом «Submissions are currently closed». Подать нельзя никому.
- **Godly** — редиректит на `recent.design`: проект переименован, ленту куратор собирает из X и Instagram, формы подачи нет. Путь один — выложить кейс в свои соцсети и отметить их.
- **Muzli** — формы подачи нет и не было: лента наполняется автоматически из Behance, Dribbble, Awwwards и подобных. Работает косвенно — попадание туда приходит само после публикации на других площадках.
- **Siteinspire** — `/submit` отдаёт 404, подача живёт внутри кабинета (`/signin`). Нужен аккаунт.
- **Land-book** — то же самое: в шапке только Sign in / Sign up, подача из кабинета.

Регистрировать аккаунты и заводить пароли от вашего имени я не могу — это делается вручную. На Siteinspire и Land-book регистрация занимает минуту, дальше нужен только URL и абзац из раздела 3.

## 5. Порядок действий

1. Siteinspire и Land-book — зарегистрироваться (почта + пароль) и подать: URL + абзац из раздела 3. По две минуты каждая.
2. Codrops Collective и three.js Showcase: техническая аудитория, приводит разработчиков и партнёров.
3. Ролик на английском готов (`promo-video/out/configurator-promo-en-1080p.mp4`) — можно идти в Show HN, Reddit и LinkedIn.
4. Параллельно — письмо в CSSDA и FWA с просьбой об инвойсе. Ответ обычно за пару дней.

Результат Awwwards стоит дождаться: если дадут Honorable Mention или Site of the Day, это отдельный инфоповод для всех площадок выше и хороший аргумент в письме к CSSDA.
