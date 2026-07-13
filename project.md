# 项目说明书 (project.md)

> [!NOTE]
> 本文件定义了当前项目的核心背景、目标、设计规范与任务看板。助理每次开启新会话时会优先加载此文件，以获取最新的项目上下文。

---

## 🎯 1. 项目背景与目标

*   **项目愿景**：针对江苏省（苏州市）小学 K-12 教学大纲与小升初分班考进度，提供自适应诊断和 3D 图谱导览系统。通过酷炫、高端的 Web 端 3D 漏斗形图谱和树状视图，让家长直观记录孩子的通关进度，并为六年级核心节点配套历年真题及变式出题训练。
*   **项目来源**：基于开源仓库 [withmarbleapp/os-taxonomy](https://github.com/withmarbleapp/os-taxonomy) 深度定制开发，目前作为独立项目托管于个人仓库 [shinelee2014/Marble3D](https://github.com/shinelee2014/Marble3D)。
*   **当前核心任务**：
    1.  持续进行 2025/2026 小升初/分班考仿真真题的智能生成与结构化注入。
    2.  确保 3D 视图下“垂直年级轴”锁定与“漏斗螺旋结构”稳定工作，黄金依赖路线发光显著。
    3.  保证多账号家庭档案与 SQLite 数据库（taxonomy.db）无缝通信。

## 🛠️ 2. 技术栈与核心依赖

*   **运行环境**：Windows 操作系统，Python 3.10+ (server.py)，现代 Web 浏览器。
*   **核心库/框架**：
    *   **后端**：Python `http.server` & `sqlite3`。通过 `/api/generate-questions` 接口，支持调用本地大模型进行真题仿真题及变式训练题的实时推理与生成。
    *   **前端**：Vanilla HTML5 Canvas（2D 渲染上下文模拟 3D 投影旋转），Vanilla CSS3 现代化暗色毛玻璃（Glassmorphism）UI。
*   **数据存储**：
    *   `data/topics_cn.json` / `dependencies_cn.json`：静态学科图谱节点与拓扑前置连线关系（仿真真题挂载在此 JSON 的节点下）。
    *   `data/taxonomy.db`：SQLite 本地轻量数据库，保存活跃 Profile、学生各节点掌握状态（mastery）以及翻译缓存。

## 🏗️ 3. 架构设计与模块分工

*   **目录分层**：
    *   `data/`：核心数据源，包括大纲拓扑 JSON 与 SQLite 数据库。
    *   `scripts/`：后台维护工具，例如 `generate_synthetic_exams.py`（仿真真题自动生成注入）。
    *   `server.py`：本地 Web 服务器与 API 路由处理中心。
    *   `explorer.html`：主前端界面，包含 3D 渲染器、列表搜索、详情卡片和仿真出题交互。
*   **核心数据流/组件关系**：
    *   初始化时，`server.py` 启动，加载 `data/taxonomy.db` 及 JSON 数据并服务于端口 `8000`。
    *   `explorer.html` 通过 HTTP API 向后端拉取当前孩子（profile）的学习进度与节点掌握状态。
    *   3D 引擎使用 `requestAnimationFrame` 进行坐标转换（从 3D 圆锥漏斗投影至 2D 物理像素），并在 Canvas 绘制节点与霓虹关系线。

## 📋 4. 交付合格标准 (Definition of Done)

*   **开发验收标准**：
    *   [x] 代码无任何 JavaScript 报错或 Console 输出冗余。
    *   [x] 物理像素对齐算法完整启用，支持 DPR 高分屏下的超清文字呈现。
*   **Reality Checker 专项清单**：
    *   [x] **禁止文字重影**：阴影必须采用物理像素单位进行高精偏移，普通标签需通过垂直碰撞检测引擎实现垂直错开避让。
    *   [x] **垂直年级轴防翻转**：拖拽俯仰角受严格范围控制，绝不允许星空发生天地倒转。
    *   [x] **金黄色高亮**：选中的前置路线必须使用外发光的霓虹金黄，解锁路线使用紫色，未激活的普通连线保持灰暗。

## 📅 5. 开发任务与看板 (TODO List)

- `[x]` 2025/2026 年仿真考题挂载至六年级大纲节点
- `[x]` 3D 星空标签防重叠与 subpixel 抗锯齿重影消除
- `[x]` 重置视图后 overlay 默认指引文本恢复功能
- `[x]` 工具栏功能分组优化与学科树状自适应隐藏
- `[x]` 3D 星云圆柱螺旋升级为“漏斗形知识树”及 Y 轴锁定自转
- `[ ]` 进阶：引入更多苏州小升初真题原卷进行切分与挂载
- `[ ]` 进阶：实现家长端诊断报告一键导出与 PDF 打印
