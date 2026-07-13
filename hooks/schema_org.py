"""
MkDocs hook: build a schema.org JSON-LD block for each page's render
context (docs/overrides/main.html reads context.schema_jsonld).

Built here rather than via raw Jinja string interpolation in the template
because JSON needs real escaping (a literal '"' in a page title must become
\" for valid JSON, not &quot; the way Jinja's HTML autoescape would render
it), and naive interpolation risks a title/description containing
"</script>" breaking out of the <script type="application/ld+json"> tag
entirely. json.dumps() handles the former; the explicit "</" replace below
handles the latter (JSON strings don't otherwise require escaping "/").
"""
import json


def on_page_context(context, page, config, nav, **kwargs):
    site_url = config.get('site_url') or ''
    data = {
        '@context': 'https://schema.org',
        '@type': 'TechArticle',
        'headline': page.title or config.get('site_name'),
        'url': site_url + str(page.url),
        'isPartOf': {
            '@type': 'WebSite',
            'name': config.get('site_name'),
            'url': site_url,
        },
    }
    description = page.meta.get('description') or config.get('site_description')
    if description:
        data['description'] = description
    date_modified = page.meta.get('git_revision_date_localized_raw_iso_date')
    if date_modified:
        data['dateModified'] = date_modified
    date_published = page.meta.get('git_creation_date_localized_raw_iso_date')
    if date_published:
        data['datePublished'] = date_published

    encoded = json.dumps(data, ensure_ascii=False)
    encoded = encoded.replace('</', '<\\/')
    context['schema_jsonld'] = encoded
    return context
