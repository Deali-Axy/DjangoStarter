from dataclasses import dataclass
from pathlib import Path
from typing import List

from django.conf import settings


@dataclass(frozen=True)
class DocCategory:
    key: str
    title: str
    description: str
    order: int


@dataclass(frozen=True)
class DocPage:
    slug: str
    title: str
    summary: str
    category: str
    path: Path
    order: int


def get_categories() -> List[DocCategory]:
    """Return ordered documentation categories."""
    return [
        DocCategory(key="project", title="项目指南", description="快速了解与上手项目", order=1),
        DocCategory(key="backend", title="后端基础", description="Django 与后端开发指南", order=2),
        DocCategory(key="frontend", title="前端基础", description="前端与模板开发指南", order=3),
        DocCategory(key="planning", title="项目规划", description="路线与演进说明", order=4),
    ]


def get_doc_pages() -> List[DocPage]:
    """Return ordered documentation pages."""
    base_dir = Path(settings.BASE_DIR)
    local_docs_dir = Path(__file__).resolve().parent / "markdown"
    repo_roadmap_path = base_dir.parent / "docs" / "roadmap.md"
    roadmap_path = repo_roadmap_path if repo_roadmap_path.exists() else local_docs_dir / "roadmap.md"
    return [
        DocPage(
            slug="overview",
            title="DjangoStarter 概览",
            summary="项目定位、核心能力与适用场景",
            category="project",
            path=local_docs_dir / "overview.md",
            order=1,
        ),
        DocPage(
            slug="quick-start",
            title="快速开始",
            summary="环境准备、依赖安装与本地启动",
            category="project",
            path=local_docs_dir / "quick-start.md",
            order=2,
        ),
        DocPage(
            slug="architecture",
            title="架构与规范",
            summary="目录结构、组件职责与开发规范",
            category="project",
            path=local_docs_dir / "architecture.md",
            order=3,
        ),
        DocPage(
            slug="deployment",
            title="部署指南",
            summary="生产环境部署与常见注意事项",
            category="project",
            path=local_docs_dir / "deployment.md",
            order=4,
        ),
        DocPage(
            slug="django-basics",
            title="Django 开发基础",
            summary="常用命令、缓存与测试注意事项",
            category="backend",
            path=local_docs_dir / "quick-start.md",
            order=1,
        ),
        DocPage(
            slug="pdm-usage",
            title="PDM 使用指南",
            summary="依赖管理与虚拟环境实践",
            category="backend",
            path=local_docs_dir / "pdm-usage.md",
            order=2,
        ),
        DocPage(
            slug="frontend-basics",
            title="前端开发基础",
            summary="Tailwind、Flowbite 与 HTMX 使用要点",
            category="frontend",
            path=local_docs_dir / "frontend-quick-start.md",
            order=1,
        ),
        DocPage(
            slug="roadmap",
            title="路线图",
            summary="项目里程碑与未来计划",
            category="planning",
            path=roadmap_path,
            order=1,
        ),
    ]
