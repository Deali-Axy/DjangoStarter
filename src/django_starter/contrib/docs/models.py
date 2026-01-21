from django.db import models


class DocCategory(models.Model):
    """文档分类模型。"""

    key = models.SlugField("唯一标识", max_length=50, unique=True)
    title = models.CharField("分类标题", max_length=100)
    description = models.CharField("分类描述", max_length=200, blank=True)
    order = models.PositiveIntegerField("排序", default=0)
    is_active = models.BooleanField("是否启用", default=True)

    class Meta:
        verbose_name = "文档分类"
        verbose_name_plural = "文档分类"
        ordering = ["order", "id"]

    def __str__(self) -> str:
        """返回分类标题。"""
        return self.title


class DocPage(models.Model):
    """文档页面模型。"""

    category = models.ForeignKey(DocCategory, on_delete=models.CASCADE, related_name="pages", verbose_name="分类")
    slug = models.SlugField("Slug", max_length=100, unique=True)
    title = models.CharField("标题", max_length=200)
    summary = models.CharField("摘要", max_length=300, blank=True)
    source_path = models.CharField("Markdown路径", max_length=300)
    order = models.PositiveIntegerField("排序", default=0)
    is_published = models.BooleanField("是否发布", default=True)

    class Meta:
        verbose_name = "文档页面"
        verbose_name_plural = "文档页面"
        ordering = ["order", "id"]

    def __str__(self) -> str:
        """返回文档标题。"""
        return self.title
