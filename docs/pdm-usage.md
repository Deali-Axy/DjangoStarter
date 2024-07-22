# 扩展阅读：pdm 基本使用方法

PDM (Python Development Master) 一个现代化的包管理和项目管理工具，它专为 Python 项目设计，提供了诸如依赖解析、包安装以及虚拟环境管理等功能。下面是一些建议和最佳实践，帮助你更好地利用 PDM 来管理你的 DjangoStarter v3 项目。

## 初始化 PDM 项目

如果你的项目还未使用 PDM，可以通过以下步骤初始化：

1. 确保已安装 PDM。如果未安装，可以通过 pip 安装：

   ```
   bashCopy code
   pip install pdm
   ```

2. 在项目根目录下运行以下命令初始化项目：

   ```
   bashCopy code
   pdm init
   ```

这一步会创建一个 `pyproject.toml` 文件，这是 PDM（和其他使用 pyproject.toml 的工具）用来存储项目配置和依赖信息的。

## 添加依赖

为了将 Django 和 Django Ninja 添加到你的项目中，你可以使用以下命令：

```
bashCopy codepdm add django
pdm add django-ninja
```

PDM 会自动解析这些包的依赖并将它们添加到 `pyproject.toml` 文件中，同时更新 `pdm.lock` 文件来锁定这些依赖的版本，确保项目的可重复性。

## 管理开发依赖

如果你有一些只在开发时需要的依赖（比如 linters、测试框架等），可以将它们添加为开发依赖：

```
bashCopy code
pdm add --dev pytest django-debug-toolbar
```

## 使用虚拟环境

PDM 默认使用项目本地的 `__pypackages__` 目录来存放依赖，而不是创建一个虚拟环境。这意味着你可以直接运行命令来执行你的应用，而无需激活虚拟环境。例如：

```
bashCopy code
pdm run python manage.py runserver
```

或者，你可以配置 PDM 使用传统的虚拟环境。详情请查阅 PDM 文档。

## 更新依赖

要更新项目的依赖，可以使用：

```
bashCopy code
pdm update
```

这会根据 `pyproject.toml` 中指定的依赖范围，更新 `pdm.lock` 文件，并安装这些依赖的最新版本。