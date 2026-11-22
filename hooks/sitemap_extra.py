"""Add standalone HTML pages (not built by MkDocs) to sitemap.xml and sitemap.xml.gz."""
import gzip
import os

EXTRA_PATHS = ["about.html"]


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
    if not entries:
        return
    xml = xml.replace("</urlset>", entries + "</urlset>")
    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)
    with gzip.open(path + ".gz", "wb") as f:
        f.write(xml.encode("utf-8"))
