from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DocCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.SlugField(max_length=50, unique=True, verbose_name="唯一标识")),
                ("title", models.CharField(max_length=100, verbose_name="分类标题")),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="分类描述")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="排序")),
                ("is_active", models.BooleanField(default=True, verbose_name="是否启用")),
            ],
            options={
                "verbose_name": "文档分类",
                "verbose_name_plural": "文档分类",
                "ordering": ["order", "id"],
            },
        ),
        migrations.CreateModel(
            name="DocPage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(max_length=100, unique=True, verbose_name="Slug")),
                ("title", models.CharField(max_length=200, verbose_name="标题")),
                ("summary", models.CharField(blank=True, max_length=300, verbose_name="摘要")),
                ("source_path", models.CharField(max_length=300, verbose_name="Markdown路径")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="排序")),
                ("is_published", models.BooleanField(default=True, verbose_name="是否发布")),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pages",
                        to="guide.doccategory",
                        verbose_name="分类",
                    ),
                ),
            ],
            options={
                "verbose_name": "文档页面",
                "verbose_name_plural": "文档页面",
                "ordering": ["order", "id"],
            },
        ),
    ]
