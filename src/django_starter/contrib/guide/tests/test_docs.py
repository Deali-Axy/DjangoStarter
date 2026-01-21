from django.test import TestCase
from django.urls import reverse

from django_starter.contrib.docs.registry import get_doc_pages


class DocsViewTests(TestCase):
    """文档模块视图测试。"""

    def test_docs_index(self):
        """文档首页返回成功。"""
        response = self.client.get(reverse("djs_docs:index"))
        self.assertEqual(response.status_code, 200)

    def test_docs_detail(self):
        """文档详情返回成功。"""
        page = get_doc_pages()[0]
        response = self.client.get(reverse("djs_docs:detail", kwargs={"slug": page.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, page.title)

    def test_docs_search(self):
        """文档搜索返回成功。"""
        response = self.client.get(f"{reverse('djs_docs:index')}?q=Tailwind")
        self.assertEqual(response.status_code, 200)
