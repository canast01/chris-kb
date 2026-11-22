"""Adjust sitemap.xml / sitemap.xml.gz after build: add standalone HTML pages, drop noindex pages,
and use each page's last git commit date as <lastmod> instead of the build date."""
import gzip
import os
import re

EXTRA_PATHS = ["about.html"]
# Internal dashboards (also marked noindex in overrides/main.html)
REMOVE_PATHS = ["site-quality/", "usage-metrics/"]


# canonical URL -> last git revision date (YYYY-MM-DD), filled during the build
_LASTMOD = {}


def on_page_context(context, page, config, nav, **kwargs):
    date = page.meta.get("git_revision_date_localized_raw_iso_date")
    if date and page.canonical_url:
        _LASTMOD[page.canonical_url] = date
    return context


def _set_lastmod(match):
    loc = match.group(1)
    date = _LASTMOD.get(loc)
    if not date:
        return match.group(0)
    return re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{date}</lastmod>", match.group(0))


def on_post_build(config, **kwargs):
    site_dir = config["site_dir"]
    base = config["site_url"].rstrip("/") + "/"
    path = os.path.join(site_dir, "sitemap.xml")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        xml = f.read()
    entries = "".join(
        f"    <url>\n         <loc>{base}{p}</loc>\n    </url>\n"
        for p in EXTRA_PATHS
        if f"<loc>{base}{p}</loc>" not in xml
    )
    for p in REMOVE_PATHS:
        xml = re.sub(
            r"\s*<url>\s*<loc>" + re.escape(base + p) + r"</loc>.*?</url>",
            "", xml, flags=re.S)
    xml = re.sub(r"<url>\s*<loc>([^<]+)</loc>.*?</url>", _set_lastmod, xml, flags=re.S)
    xml = xml.replace("</urlset>", entries + "</urlset>")
    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)
    with gzip.open(path + ".gz", "wb") as f:
        f.write(xml.encode("utf-8"))
