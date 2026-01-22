import pytest
from django.urls import reverse
from django_starter.contrib.docs.registry import get_doc_pages
from django_starter.contrib.docs.views import _render_markdown

class TestDocsViews:
    def test_docs_index(self, client):
        """文档首页返回成功"""
        url = reverse("djs_docs:index")
        response = client.get(url)
        assert response.status_code == 200

    def test_docs_detail(self, client):
        """文档详情返回成功，包含渲染后的内容和 TOC"""
        pages = get_doc_pages()
        if not pages:
            pytest.skip("No doc pages found")
        page = pages[0]
        url = reverse("djs_docs:detail", kwargs={"slug": page.slug})
        response = client.get(url)
        assert response.status_code == 200
        assert page.title in response.content.decode()

    def test_docs_search(self, client):
        """文档搜索返回成功"""
        url = reverse("djs_docs:index")
        response = client.get(f"{url}?q=Django")
        assert response.status_code == 200

    def test_doc_404(self, client):
        """访问不存在的文档应返回 404"""
        url = reverse("djs_docs:detail", kwargs={"slug": "non-existent-slug-12345"})
        response = client.get(url)
        assert response.status_code == 404

    def test_markdown_render_logic(self):
        """测试 Markdown 渲染逻辑"""
        md_text = "# Title\n\n```python\nprint('hello')\n```"
        html, toc = _render_markdown(md_text)
        assert "Title" in html
        assert "<ul>" in toc
