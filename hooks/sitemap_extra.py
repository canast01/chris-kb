"""Adjust sitemap.xml / sitemap.xml.gz after build: add standalone HTML pages, drop noindex pages."""
import gzip
import os
import re

EXTRA_PATHS = ["about.html"]
# Internal dashboards (also marked noindex in overrides/main.html)
REMOVE_PATHS = ["site-quality/", "usage-metrics/"]


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
    xml = xml.replace("</urlset>", entries + "</urlset>")
    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)
    with gzip.open(path + ".gz", "wb") as f:
        f.write(xml.encode("utf-8"))
