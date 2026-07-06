"""Runs the full pipeline: scrape vargov.ru -> build RU knowledge base -> build EN mirror.

Usage: python scripts/run_all.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import scrape_products
import build_kb
import translate_en


def main():
    print("== 1/3 scraping vargov.ru ==")
    scrape_products.main()
    print("\n== 2/3 building Russian knowledge base ==")
    build_kb.build()
    print("\n== 3/3 building English mirror ==")
    translate_en.build_en()
    print("\nDone.")


if __name__ == "__main__":
    main()
