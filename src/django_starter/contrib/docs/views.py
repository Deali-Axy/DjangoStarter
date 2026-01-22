from pathlib import Path
from typing import Dict, List, Optional, Tuple

import markdown
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render, reverse

from .registry import DocCategory, DocPage, get_categories, get_doc_pages


def _load_markdown(path: Path) -> str:
    """Load markdown content from disk."""
    if not path.exists():
        raise Http404("文档未找到")
    return path.read_text(encoding="utf-8")


def _render_markdown(content: str) -> Tuple[str, str]:
    """Render markdown content to HTML and return (html, toc)."""
    md = markdown.Markdown(
        extensions=[
            "fenced_code",
            "tables",
            "toc",
            "sane_lists",
            "admonition",
            "codehilite",
            "attr_list",
            "nl2br",
        ],
        extension_configs={
            "toc": {
                "permalink": True,
            },
            "codehilite": {
                "css_class": "highlight",
                "guess_lang": False,
            },
        },
    )
    html = md.convert(content)
    return html, md.toc


def _build_categories(pages: List[DocPage], categories: List[DocCategory]) -> List[Dict[str, object]]:
    """Build category tree with pages."""
    pages_by_category: Dict[str, List[DocPage]] = {category.key: [] for category in categories}
    for page in pages:
        pages_by_category.setdefault(page.category, []).append(page)
    return [
        {
            "category": category,
            "pages": sorted(pages_by_category.get(category.key, []), key=lambda item: item.order),
        }
        for category in sorted(categories, key=lambda item: item.order)
    ]


def _find_page(slug: str, pages: List[DocPage]) -> DocPage:
    """Find a page by slug."""
    for page in pages:
        if page.slug == slug:
            return page
    raise Http404("文档未找到")


def _search_pages(query: str, pages: List[DocPage]) -> List[DocPage]:
    """Search pages by query in title, summary and content."""
    keyword = query.lower().strip()
    if not keyword:
        return []
    matched: List[DocPage] = []
    for page in pages:
        if keyword in page.title.lower() or keyword in page.summary.lower():
            matched.append(page)
            continue
        content = _load_markdown(page.path).lower()
        if keyword in content:
            matched.append(page)
    return matched


def _get_prev_next_pages(current_slug: str, pages: List[DocPage]) -> Tuple[Optional[DocPage], Optional[DocPage]]:
    """Get previous and next pages."""
    for i, page in enumerate(pages):
        if page.slug == current_slug:
            prev_page = pages[i - 1] if i > 0 else None
            next_page = pages[i + 1] if i < len(pages) - 1 else None
            return prev_page, next_page
    return None, None


def _get_template_name(request: HttpRequest) -> str:
    """Determine template name based on HTMX request."""
    if request.headers.get("HX-Request") == "true":
        return "django_starter/docs/htmx_response.html"
    return "django_starter/docs/index.html"


def docs_index(request: HttpRequest) -> HttpResponse:
    """Render documentation index with default or search result."""
    pages = get_doc_pages()
    categories = get_categories()
    query = request.GET.get("q", "").strip()
    search_results = _search_pages(query, pages) if query else []
    
    active_page = None
    active_html = ""
    toc = ""
    prev_page = None
    next_page = None

    # Only show active page if it is a search result
    if search_results:
        active_page = search_results[0]
        
    if active_page:
        active_html, toc = _render_markdown(_load_markdown(active_page.path))
        prev_page, next_page = _get_prev_next_pages(active_page.slug, pages)

    context = {
        "page_title": "文档中心",
        "breadcrumbs": [
            {"text": "首页", "url": "/"},
            {"text": "文档中心", "url": None},
        ],
        "categories": _build_categories(pages, categories),
        "active_page": active_page,
        "active_html": active_html,
        "toc": toc,
        "prev_page": prev_page,
        "next_page": next_page,
        "search_query": query,
        "search_results": search_results,
    }
    return render(request, _get_template_name(request), context)


def docs_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Render documentation page by slug."""
    pages = get_doc_pages()
    categories = get_categories()
    active_page = _find_page(slug, pages)
    active_html, toc = _render_markdown(_load_markdown(active_page.path))
    prev_page, next_page = _get_prev_next_pages(slug, pages)
    
    context = {
        "page_title": active_page.title,
        "breadcrumbs": [
            {"text": "首页", "url": "/"},
            {"text": "文档中心", "url": reverse("djs_docs:index")},
            {"text": active_page.title, "url": None},
        ],
        "categories": _build_categories(pages, categories),
        "active_page": active_page,
        "active_html": active_html,
        "toc": toc,
        "prev_page": prev_page,
        "next_page": next_page,
        "search_query": "",
        "search_results": [],
    }
    return render(request, _get_template_name(request), context)
