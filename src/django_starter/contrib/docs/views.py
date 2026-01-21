from pathlib import Path
from typing import Dict, List, Optional

import markdown
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from .registry import DocCategory, DocPage, get_categories, get_doc_pages


def _load_markdown(path: Path) -> str:
    """Load markdown content from disk."""
    if not path.exists():
        raise Http404("文档未找到")
    return path.read_text(encoding="utf-8")


def _render_markdown(content: str) -> str:
    """Render markdown content to HTML."""
    return markdown.markdown(
        content,
        extensions=["fenced_code", "tables", "toc", "sane_lists"],
    )


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


def docs_index(request: HttpRequest) -> HttpResponse:
    """Render documentation index with default or search result."""
    pages = get_doc_pages()
    categories = get_categories()
    query = request.GET.get("q", "").strip()
    search_results = _search_pages(query, pages) if query else []
    active_page = search_results[0] if search_results else pages[0] if pages else None
    active_html = _render_markdown(_load_markdown(active_page.path)) if active_page else ""
    context = {
        "page_title": "文档中心",
        "categories": _build_categories(pages, categories),
        "active_page": active_page,
        "active_html": active_html,
        "search_query": query,
        "search_results": search_results,
    }
    return render(request, "django_starter/docs/index.html", context)


def docs_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Render documentation page by slug."""
    pages = get_doc_pages()
    categories = get_categories()
    active_page = _find_page(slug, pages)
    active_html = _render_markdown(_load_markdown(active_page.path))
    context = {
        "page_title": active_page.title,
        "categories": _build_categories(pages, categories),
        "active_page": active_page,
        "active_html": active_html,
        "search_query": "",
        "search_results": [],
    }
    return render(request, "django_starter/docs/index.html", context)
