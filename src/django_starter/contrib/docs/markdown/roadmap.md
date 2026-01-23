# AI+全栈脚手架 路线图与里程碑

面向独立开发者与小团队的 AI+全栈脚手架的务实规划，强调可维护、可部署、可商业化。遵循向后兼容与增量启用原则（FeatureFlag），以最简数据结构与统一抽象消除特殊情况与重复复杂度。

## 里程碑（Roadmap）

### M0 基础稳固（1–2周）
- 结构化日志（JSON）与统一错误码/错误响应体
- 健康（`/health`）与就绪（`/ready`）探针
- Prometheus 指标闭环（`/metrics` + 中间件），附基础告警建议
- 配置分层与 FeatureFlag 基础设施
- 管理后台视图：Usage/Job/FeatureFlag/Audit 面板

### M1 认证与身份接入（SSO）
- 统一身份接入层：保留现有微信/企微 OAuth2 能力，并可选集成 `django-allauth`
- JWT 与 API Key（作用域与过期）
- 设备与会话管理，支持登出全部设备

### M2 AI 核心能力
- `LLMProvider` 适配层（OpenAI、Azure OpenAI、Gemini、Ollama），统一接口
- 流式输出抽象（SSE/WebSocket），支持函数/工具调用
- Prompt Store（版本化/审计/回滚），会话持久化与响应缓存（Redis）

### M3 RAG 与数据管线
- `pgvector` 优先，兼容 Qdrant/Milvus；检索器与组合器接口
- 文档摄入管线（分块/索引/元数据），评估与 A/B 测试
- 示例：知识库问答与项目文档检索

### M4 任务与作业
- Django Tasks（内置）集成、定时任务与重试策略（后端可配置）
- 通知中心（站内/邮件）与任务通知
- 可选：Celery 集成（需要分布式队列时）
- Job 进度上报与取消，前端进度条与重试按钮
- 队列监控面板（失败任务审计）

### M5 产品化与支付
- 支付集成（Stripe/微信/支付宝），订阅计划与权限映射
- 用量配额/超用处理与冻结策略，告警与邮件通知
- 账单与发票、计量报表导出

### M6 开发者体验（DX）
- CLI 扩展：生成器、种子数据 DSL、LLM 连接性测试
- 预提交钩子与质量栈：ruff/isort/mypy/pytest/commitlint
- 语义化版本与自动发布，Changelog 自动生成

### M7 观测与安全
- OpenTelemetry（trace/metrics）与 Sentry 集成
- 速率限制、CSP、密钥轮换、依赖与镜像安全扫描
- 数据导出与隐私工具（会话/提示/索引），合规基础

### M8 前端与样例
- HTMX/Alpine 流式模式组件化，统一 Loading/错误态
- PWA（可选）、Dark Mode、国际化前端资源
- 示例应用：聊天助理、RAG 知识库、工单助理（含 SSE/WebSocket）

### M9 部署与一键可用
- Docker 镜像与 Compose 栈：Nginx/Redis/Postgres
- 一键部署模板：Railway/Fly.io/Render，环境变量与默认限额
- 生产就绪清单与回滚策略

## TODO 清单（执行项）

- [ ] Prometheus 指标闭环（/metrics + 中间件启用）与告警建议
- [ ] 统一身份接入层：现有微信/企微 OAuth2 + 可选 `django-allauth`
- [ ] LLMProvider 适配层（OpenAI/Azure/Gemini/Ollama），统一接口
- [ ] 流式响应抽象（SSE/WebSocket），支持函数/工具调用
- [ ] Prompt Store（版本化/变更审计/A/B 测试）
- [ ] 会话与消息持久化，结构化存储与清理策略
- [ ] 响应缓存与幂等性设计（Redis，键空间规范）
- [ ] pgvector 集成与向量检索接口（可插拔后端）
- [ ] 文档摄入管线（分块/索引/元数据），管理后台操作
- [ ] RAG 评估框架（正确率/覆盖率/延迟），基线数据集
- [ ] Django Tasks 集成与任务进度上报（后台与前端），可选 Celery 升级
- [ ] 队列监控面板与失败任务重试策略
- [ ] API Key（作用域）与使用量配额/限流策略
- [ ] （Deferred）Org/Team/Project 多租户与 RBAC，审计日志
- [ ] （Deferred）高级审计事件中心、合规导出与数据保留策略
- [ ] 支付集成（Stripe/微信/支付宝），订阅与权限映射
- [ ] 计量与账单报表（Usage 统计/导出/告警）
- [ ] 安全策略：CSP/速率限制/密钥轮换/依赖扫描
- [ ] OpenTelemetry（trace/metrics）与 Sentry 集成
- [ ] 结构化日志与统一错误码/错误响应体
- [ ] CLI 子命令：生成器扩展、种子数据 DSL、LLM 连接测试
- [ ] 预提交钩子：ruff/isort/mypy/pytest/commitlint
- [ ] 版本语义化发布与 Changelog 自动生成
- [ ] HTMX/Alpine 流式 UI 组件库与错误态统一
- [ ] 示例应用：聊天助理、RAG 知识库、工单助理
- [ ] 一键部署模板（Railway/Fly.io/Render）与生产就绪清单
- [ ] FeatureFlag 框架与增量启用策略
- [ ] 数据导出与隐私工具（会话/提示/索引），合规基础
- [ ] 文档完善：架构图、扩展点、运维与故障排除
- [ ] 可选关闭前端，仅暴露 API 与 CLI 模式
- [ ] 软删除与审计（关键模型：Prompt/Conversation/Job/Usage）

## 优先级建议

- 第一优先：LLMProvider 适配层、流式抽象、Prompt Store、会话持久化
- 第二优先：pgvector/RAG 管线、Django Tasks/Celery 与进度机制、API Key/配额
- 第三优先：支付与订阅、观测与安全、CLI 与开发者体验
- 第四优先：前端示例与一键部署、文档与合规

## 兼容性与风险控制

- 公共 API 与生成器输出版本化；默认稳定，新增能力通过 FeatureFlag 启用
- 数据迁移保持可回滚，严禁破坏既有表语义（Never break userspace）
- 流式抽象与 Job 模型作为统一“正常情况”，避免分散的自定义分支

## 下一步

- 先落地 M2 的适配层与流式抽象，提供最小可运行示例与接口约定
- 在 README 的 `## TODO` 段添加本路线图链接，保持主入口简洁
