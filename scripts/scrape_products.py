"""
Scans vargov.ru's sitemap for product URLs and scrapes each product page's
embedded `var product = {...}` JSON block (Tilda store data).

Output: scan/products.jsonl (one JSON object per product, deduped by URL).
Also writes scan/product_urls.txt and scan/failed_urls.txt for visibility.

Safe to re-run: fully re-scans and overwrites, so it always reflects the
current live catalog rather than incrementally patching stale data.
"""
import json, re, subprocess, time, os, html as htmlmod
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIR = ROOT / "scan"
SCAN_DIR.mkdir(exist_ok=True)

SITEMAP_URL = "https://vargov.ru/sitemap-store.xml"
PRODUCT_RE = re.compile(r'var product = (\{.*?\});', re.S)
TAG_RE = re.compile(r'<[^>]+>')


def curl(url, out_path=None, max_time=25):
    cmd = ["curl", "-sS", "--max-time", str(max_time), "-A", "Mozilla/5.0", url]
    if out_path:
        cmd += ["-o", str(out_path)]
        r = subprocess.run(cmd, capture_output=True, timeout=max_time + 5)
        return r.returncode == 0
    r = subprocess.run(cmd, capture_output=True, timeout=max_time + 5)
    return r.stdout.decode("utf-8", errors="replace") if r.returncode == 0 else None


def fetch_sitemap():
    data = curl(SITEMAP_URL)
    if not data:
        raise SystemExit("Could not fetch sitemap-store.xml")
    urls = re.findall(r"<loc>([^<]+)</loc>", data)
    (SCAN_DIR / "product_urls.txt").write_text("\n".join(urls), encoding="utf-8")
    return urls


def clean_text(s):
    if not s:
        return ""
    s = TAG_RE.sub(" ", s)
    s = htmlmod.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def fetch_product(url, tries=5):
    for attempt in range(tries):
        data = curl(url, max_time=20)
        if data and len(data) > 1000:
            return data
        time.sleep(1.5 * (attempt + 1))
    return None


def parse_product(url, data):
    m = PRODUCT_RE.search(data)
    if not m:
        return None
    try:
        obj = json.loads(m.group(1))
    except Exception:
        return None
    category = url.split("vargov.ru/")[1].split("/")[0]
    return {
        "url": url,
        "category": category,
        "uid": obj.get("uid"),
        "sku": obj.get("sku"),
        "title": obj.get("title"),
        "description": clean_text(obj.get("text")),
        "gallery": [g.get("img") for g in obj.get("gallery", []) if g.get("img")],
        "price": obj.get("price"),
        "editions": obj.get("editions", []),
        "characteristics": obj.get("characteristics", []),
        "properties": obj.get("properties", []),
    }


def worker(url):
    data = fetch_product(url)
    if not data:
        return ("fail", url, None)
    prod = parse_product(url, data)
    if not prod:
        return ("noparse", url, None)
    return ("ok", url, prod)


def main():
    urls = fetch_sitemap()
    print(f"Found {len(urls)} product URLs in sitemap")

    results = {}
    failed = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        futures = {ex.submit(worker, u): u for u in urls}
        done = 0
        for fut in as_completed(futures):
            status, url, prod = fut.result()
            done += 1
            if status == "ok":
                results[url] = prod
            else:
                failed.append(url)
            if done % 50 == 0 or done == len(urls):
                print(f"progress: {done}/{len(urls)} ok={len(results)} fail={len(failed)}")

    # one retry pass for failures, lower concurrency, more patience
    if failed:
        print(f"Retrying {len(failed)} failed URLs...")
        still_failed = []
        with ThreadPoolExecutor(max_workers=2) as ex:
            futures = {ex.submit(worker, u): u for u in failed}
            for fut in as_completed(futures):
                status, url, prod = fut.result()
                if status == "ok":
                    results[url] = prod
                else:
                    still_failed.append(url)
        failed = still_failed

    with open(SCAN_DIR / "products.jsonl", "w", encoding="utf-8") as f:
        for prod in results.values():
            f.write(json.dumps(prod, ensure_ascii=False) + "\n")

    (SCAN_DIR / "failed_urls.txt").write_text("\n".join(failed), encoding="utf-8")

    print(f"DONE: {len(results)} ok, {len(failed)} still failed (see scan/failed_urls.txt)")


if __name__ == "__main__":
    main()
