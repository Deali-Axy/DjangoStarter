from django.test import TestCase
from django.urls import reverse


class AboutViewsTestCase(TestCase):
    """about 应用视图与 HTMX 片段渲染测试。"""

    def test_about_index_renders(self):
        """关于我们主页面可正常渲染。"""
        resp = self.client.get(reverse('djs_about:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'id="mission"')
        self.assertContains(resp, 'id="milestones"')
        self.assertContains(resp, 'id="team"')
        self.assertContains(resp, 'id="faq"')

    def test_milestones_partials_pagination(self):
        """里程碑 HTMX 端点返回追加内容与按钮 OOB 更新。"""
        url = reverse('djs_about:partials_milestones')
        resp = self.client.get(url, {'offset': 0}, HTTP_HX_REQUEST='true')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'hx-swap-oob="outerHTML"')
        self.assertContains(resp, 'id="milestoneLoadMore"')

    def test_team_partials_pagination(self):
        """团队 HTMX 端点返回追加内容与按钮 OOB 更新。"""
        url = reverse('djs_about:partials_team')
        resp = self.client.get(url, {'offset': 0}, HTTP_HX_REQUEST='true')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'hx-swap-oob="outerHTML"')
        self.assertContains(resp, 'id="teamLoadMore"')

    def test_faq_partials_pagination(self):
        """FAQ HTMX 端点返回追加内容与按钮 OOB 更新。"""
        url = reverse('djs_about:partials_faq')
        resp = self.client.get(url, {'offset': 0}, HTTP_HX_REQUEST='true')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'hx-swap-oob="outerHTML"')
        self.assertContains(resp, 'id="faqLoadMore"')

    def test_policy_pages_have_no_inline_css(self):
        """隐私政策与服务条款页面不包含原生 CSS style 标签。"""
        privacy = self.client.get(reverse('djs_about:privacy_policy'))
        self.assertEqual(privacy.status_code, 200)
        self.assertNotContains(privacy, '<style', html=False)

        terms = self.client.get(reverse('djs_about:terms_of_service'))
        self.assertEqual(terms.status_code, 200)
        self.assertNotContains(terms, '<style', html=False)
