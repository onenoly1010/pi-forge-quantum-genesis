#!/usr/bin/env python3
"""tools/link_check.py — simple, concurrent link checker that writes CSV output

Usage:
  python tools/link_check.py https://example.com --workers 20 --crawl --output results.csv

Dependencies: requests, beautifulsoup4, tqdm
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse, urldefrag
import argparse
import csv
import time
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "data:", "file:")


def normalize_link(base_url, link):
    link = link.strip()
    if not link:
        return None
    if link.startswith(SKIP_SCHEMES):
        return None
    link, _ = urldefrag(link)
    full = urljoin(base_url, link)
    parsed = urlparse(full)
    if parsed.scheme not in ("http", "https"):
        return None
    return full


def check_url(session, url, timeout=10):
    try:
        r = session.head(url, allow_redirects=True, timeout=timeout)
        # fallback to GET if HEAD not allowed
        if r.status_code in (405, 501):
            r = session.get(url, allow_redirects=True, timeout=timeout)
        return (url, r.status_code, None)
    except requests.RequestException as e:
        return (url, None, str(e))


def find_links_from_page(html_text, base_url):
    soup = BeautifulSoup(html_text, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        normalized = normalize_link(base_url, a["href"])
        if normalized:
            links.add(normalized)
    return links


def crawl_and_check(start_url, workers=20, crawl=False, same_domain=True, timeout=10):
    session = requests.Session()
    session.headers.update({"User-Agent": "pi-forge-link-checker/1.0"})
    parsed_base = urlparse(start_url)
    to_visit = {start_url}
    seen = set()
    results = {}
    broken = []

    with ThreadPoolExecutor(max_workers=workers) as ex:
        while to_visit:
            futures = {ex.submit(check_url, session, url, timeout): url for url in list(to_visit) if url not in seen}
            to_visit.clear()
            if not futures:
                break
            for fut in as_completed(futures):
                url = futures[fut]
                seen.add(url)
                u, status, err = fut.result()
                results[u] = (status, err)
                if status is None or (isinstance(status, int) and status >= 400):
                    broken.append((u, status, err))
                if crawl and status and status < 400:
                    try:
                        r = session.get(u, timeout=timeout)
                        if r.ok and 'text/html' in r.headers.get('content-type', ''):
                            for link in find_links_from_page(r.text, u):
                                if same_domain and urlparse(link).netloc != parsed_base.netloc:
                                    continue
                                if link not in seen:
                                    to_visit.add(link)
                    except Exception:
                        pass
    return results, broken


def write_csv(results, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["url", "status", "error"])
        for url, (status, err) in results.items():
            w.writerow([url, status if status is not None else "", err or ""])


def main():
    ap = argparse.ArgumentParser(description="Concurrent Link Checker")
    ap.add_argument("site", nargs="?", help="URL to check. If omitted, uses $LINK_CHECK_SITE or https://quantumpiforge.com/",
                    default=None)
    ap.add_argument("--workers", type=int, default=20)
    ap.add_argument("--crawl", action="store_true")
    ap.add_argument("--timeout", type=int, default=10)
    ap.add_argument("--output", default="link_check_results.csv")
    args = ap.parse_args()

    site = args.site or __import__('os').environ.get('LINK_CHECK_SITE', 'https://quantumpiforge.com/')
    print(f"Checking site: {site}")
    results, broken = crawl_and_check(site, workers=args.workers, crawl=args.crawl, timeout=args.timeout)
    write_csv(results, args.output)
    print(f"Checked {len(results)} URLs; {len(broken)} broken links. Results saved to {args.output}")


if __name__ == '__main__':
    main()
