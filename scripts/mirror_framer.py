#!/usr/bin/env python3
"""Mirror jasminewilson.com (Framer) into a self-hosted static site."""

from __future__ import annotations

import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://www.jasminewilson.com"
SITE_HOSTS = {"www.jasminewilson.com", "jasminewilson.com"}
MIRROR_HOSTS = {
    "framerusercontent.com",
    "fonts.gstatic.com",
}
SKIP_HOSTS = {
    "events.framer.com",
    "framer.com",
    "www.framer.com",
    "www.w3.org",
    "drive.google.com",
    "www.linkedin.com",
}
PAGES = [
    "/",
    "/about",
    "/project",
    "/project/claritea",
    "/project/nevro",
    "/project/arrive-logistics",
    "/project/qualtrics",
    "/project/punchh",
    "/project/vodii-flueid",
    "/project/tripping",
]
EXTRA_URLS = [
    "https://framerusercontent.com/sites/2NKDJ8jabmm6MQSCqmVxsw/searchIndex-Lr6qvCDn43sP.json",
    "https://framerusercontent.com/sites/2NKDJ8jabmm6MQSCqmVxsw/searchIndex-q3t7tq7NkFJ4.json",
]
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
TEXT_SUFFIXES = {".html", ".htm", ".js", ".mjs", ".css", ".json", ".svg", ".txt", ".xml", ".map"}
URL_RE = re.compile(
    r"""(?P<url>https?:\\?/\\?/(?:framerusercontent\.com|fonts\.gstatic\.com)/[^\s"'`<>)]+)"""
)
BARE_RE = re.compile(
    r"""(?P<url>(?:framerusercontent\.com|fonts\.gstatic\.com)/[^\s"'`<>)]+)"""
)
REL_IMPORT_RE = re.compile(
    r"""(?:from|import)\s*\(?\s*["'](?P<rel>\./[^"']+)["']"""
)
PRELOAD_RE = re.compile(r"""href=["'](https://framerusercontent\.com/[^"']+)["']""")
SCRIPT_SRC_RE = re.compile(r"""src=["'](https://framerusercontent\.com/[^"']+\.m?js)["']""")


def log(msg: str) -> None:
    print(msg, flush=True)


def decode_url(raw: str) -> str:
    value = unescape(raw).replace("\\/", "/").rstrip("\\.,);")
    return value.split("#", 1)[0]


def strip_query(url: str) -> str:
    parsed = urlparse(url)
    return urlunparse(parsed._replace(query="", fragment=""))


def should_mirror(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False
    if parsed.netloc in SKIP_HOSTS:
        return False
    if parsed.netloc not in MIRROR_HOSTS:
        return False
    path = parsed.path.rstrip("/")
    return bool(path) and "." in Path(path).name


def local_path_for(url: str) -> Path:
    parsed = urlparse(strip_query(url))
    path = parsed.path.lstrip("/")
    return ROOT / "vendor" / parsed.netloc / path


def public_url_for(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path
    suffix = f"?{parsed.query}" if parsed.query else ""
    return f"/vendor/{parsed.netloc}{path}{suffix}"


def page_output_path(page: str) -> Path:
    if page == "/":
        return ROOT / "index.html"
    return ROOT / page.strip("/") / "index.html"


def fetch(url: str, retries: int = 3) -> bytes:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            req = Request(
                url,
                headers={
                    "User-Agent": UA,
                    "Accept": "*/*",
                    "Referer": ORIGIN + "/",
                },
            )
            with urlopen(req, timeout=60) as response:
                return response.read()

        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            time.sleep(0.6 * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url}: {last_error}")


def extract_remote_urls(text: str) -> set[str]:
    found: set[str] = set()
    for match in URL_RE.finditer(text):
        url = decode_url(match.group("url"))
        if should_mirror(url):
            found.add(url)
    for match in BARE_RE.finditer(text):
        url = "https://" + decode_url(match.group("url"))
        if should_mirror(url):
            found.add(url)
    for match in PRELOAD_RE.finditer(text):
        url = decode_url(match.group(1))
        if should_mirror(url):
            found.add(url)
    for match in SCRIPT_SRC_RE.finditer(text):
        url = decode_url(match.group(1))
        if should_mirror(url):
            found.add(url)
    return found


def extract_relative_imports(text: str, base_url: str) -> set[str]:
    found: set[str] = set()
    for match in REL_IMPORT_RE.finditer(text):
        found.add(urljoin(strip_query(base_url), match.group("rel")))
    # Dynamic import("./file.mjs") and import(`./file.mjs`)
    for match in re.finditer(r"""import\(\s*["'`](\./[^"'`]+)["'`]\s*\)""", text):
        found.add(urljoin(strip_query(base_url), match.group(1)))
    return found


def inject_overrides(html: str) -> str:
    html = re.sub(
        r'<script type="module" async data-framer-bundle="main"[^>]*></script>',
        "",
        html,
    )
    extras = (
        '<link rel="stylesheet" href="/overrides.css">',
        '<script>window.__framer_disable_appear_effects_optimization__=true;</script>',
    )
    for extra in extras:
        if extra not in html and "</head>" in html:
            html = html.replace("</head>", extra + "\n</head>", 1)
    script = '<script src="/overrides.js" defer></script>'
    if script not in html:
        html = html.replace("</body>", script + "\n</body>", 1) if "</body>" in html else html + script
    return html


def rewrite_text(text: str) -> str:
    text = re.sub(
        r"""<script[^>]+src=["']https://events\.framer\.com[^"']*["'][^>]*></script>""",
        "",
        text,
    )
    replacements = (
        ("https://framerusercontent.com", "/vendor/framerusercontent.com"),
        ("https://fonts.gstatic.com", "/vendor/fonts.gstatic.com"),
        ("https:\\/\\/framerusercontent.com", "/vendor/framerusercontent.com"),
        ("https:\\/\\/fonts.gstatic.com", "/vendor/fonts.gstatic.com"),
        ("https://www.jasminewilson.com/", "/"),
        ("https://www.jasminewilson.com", "/"),
        ("https:\\/\\/www.jasminewilson.com\\/", "/"),
        ("https:\\/\\/www.jasminewilson.com", "/"),
        ("https://events.framer.com/script?v=2", ""),
    )
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def is_text_url(url: str) -> bool:
    path = urlparse(strip_query(url)).path.lower()
    return Path(path).suffix in TEXT_SUFFIXES or path.endswith(".mjs")


def save_bytes(path: Path, data: bytes) -> None:
    if path.exists() and path.is_dir():
        raise ValueError(f"Refusing to overwrite directory: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def main() -> int:
    queued: dict[str, str] = {}
    html_by_page: dict[str, str] = {}

    log("Fetching pages…")
    for page in PAGES:
        url = ORIGIN + page
        log(f"  {url}")
        html = fetch(url).decode("utf-8", errors="replace")
        html_by_page[page] = html
        for asset in extract_remote_urls(html):
            queued[strip_query(asset)] = asset

    for extra in EXTRA_URLS:
        queued[strip_query(extra)] = extra

    downloaded_text: dict[str, tuple[str, str]] = {}
    seen_files: set[str] = set()

    def enqueue(url: str) -> None:
        clean = strip_query(url)
        if clean not in queued and clean not in seen_files:
            queued[clean] = url

    log("Downloading assets and following JS imports…")
    while queued:
        batch = list(queued.items())
        queued.clear()
        with ThreadPoolExecutor(max_workers=12) as pool:
            futures = {pool.submit(fetch, url): (clean, url) for clean, url in batch}
            for future in as_completed(futures):
                clean, url = futures[future]
                try:
                    data = future.result()
                except Exception as exc:
                    log(f"  SKIP {url} ({exc})")
                    continue
                dest = local_path_for(clean)
                seen_files.add(clean)
                if is_text_url(clean):
                    text = data.decode("utf-8", errors="replace")
                    downloaded_text[clean] = (url, text)
                    for asset in extract_remote_urls(text):
                        enqueue(asset)
                    if clean.endswith((".js", ".mjs")):
                        for asset in extract_relative_imports(text, clean):
                            enqueue(asset)
                else:
                    save_bytes(dest, data)
                    log(f"  {dest.relative_to(ROOT)} ({len(data):,} bytes)")

    log("Rewriting text assets…")
    for clean, (url, text) in downloaded_text.items():
        dest = local_path_for(clean)
        save_bytes(dest, rewrite_text(text).encode("utf-8"))
        log(f"  {dest.relative_to(ROOT)}")

    log("Writing pages…")
    for page, html in html_by_page.items():
        dest = page_output_path(page)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(inject_overrides(rewrite_text(html)), encoding="utf-8")
        log(f"  {dest.relative_to(ROOT)}")

    manifest = {
        "origin": ORIGIN,
        "pages": PAGES,
        "files": sorted(str(p.relative_to(ROOT)) for p in (ROOT / "vendor").rglob("*") if p.is_file()),
    }
    (ROOT / "scripts" / "mirror-manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    log(f"Done. {len(manifest['files'])} vendor files, {len(PAGES)} pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
