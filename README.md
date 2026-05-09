# George-Skill

这是一个可跨机器部署的 Codex skills 与 MCP 配置打包仓库，目标是把我当前本机已经整理好的：

- 系统级 skills
- 自定义学术与文档类 skills
- MCP 配置模板
- 本地修复过的 CNKI MCP 包装脚本

统一收纳到一个仓库里，方便你在其他电脑上直接拉取和部署。

## 目录结构

- `skills/system`
  - 系统级 skills 快照
- `skills/custom`
  - 当前机器上可复用的自定义 skills 快照
- `mcp-config/codex`
  - 当前 Codex 配置快照与可移植模板
- `mcp-config/templates`
  - Claude / Cursor / Codex 的 MCP 配置模板
- `tools`
  - 本地辅助脚本，包含修复后的 `cnki_mcp_local.py`
- `docs`
  - 部署说明、skills 清单、MCP 清单

## Skill 中文说明表

### 一、System Skills

| Skill 名称 | 作用说明 |
|---|---|
| `imagegen` | 用于生成或编辑位图图像，例如插图、透明底素材、纹理、视觉草图等。 |
| `openai-docs` | 用于查询和引用 OpenAI 官方文档，适合模型选择、API 用法、提示词升级等场景。 |
| `plugin-creator` | 用于创建 Codex 插件目录结构和基础配置。 |
| `skill-creator` | 用于设计、编写、规范化新的 Codex skill。 |
| `skill-installer` | 用于安装本地或远程来源的 Codex skills。 |

### 二、Custom Skills

| Skill 名称 | 作用说明 |
|---|---|
| `academic-search-workflow` | 学术检索工作流 skill，整合 `OpenAlex + Crossref + CNKI fallback`，适合做中英文文献检索、期刊覆盖验证、近年文献筛选、综述资料整理。 |
| `doc` | 面向 Word 文档处理，适合 `.docx` 的读取、结构检查、内容编辑与格式保留。 |
| `ieee-literature-workflow` | 面向 IEEE / IEEE Xplore 文献检索与阅读的工作流 skill，适合找 IEEE 论文、筛选近年文献、形成综述线索。 |
| `journal-figure-router` | 期刊作图路由 skill，用于把“按期刊格式画图”这类请求转发到更合适的作图 skill。 |
| `mineru-document-explorer` | 面向 PDF / DOCX / PPTX / Markdown 等文档的检索、问答、目录定位、内容抽取与知识库化。 |
| `nature-citation` | 用于给论文段落自动补 Nature / CNS 体系风格参考文献，并生成引用对应关系。 |
| `nature-data` | 用于准备 Nature 风格的数据可用性说明、数据仓储方案和 FAIR 元数据检查。 |
| `nature-figure` | 面向 Nature 风格学术图件制作与审查。 |
| `nature-paper2ppt` | 把论文或 PDF 快速转为 Nature 风格中文汇报 PPT。 |
| `nature-polishing` | 把中文或普通英文论文草稿润色成更接近 Nature 风格的学术英语。 |
| `nature-response` | 用于撰写和修订 Nature 体系论文的审稿意见回复信。 |
| `pdf` | 面向 PDF 的读取、抽取、生成与版式检查。 |
| `playwright` | 用于浏览器自动化操作，例如网页检索、表单填写、页面抓取和 UI 调试。 |
| `scientific-figure-making` | 面向 matplotlib 学术绘图，适合做论文图、报告图、多面板科研图。 |
| `speech` | 文本转语音 skill，可做朗读、配音、旁白音频生成。 |
| `top-tier-figure-router` | 顶刊顶会风格作图路由 skill，会把请求转到更合适的高水平作图流程。 |
| `transcribe` | 语音转文本 skill，适合音频/视频转录、说话人区分和访谈整理。 |

## 当前重点增强的 Skill

当前仓库里，本次重点增强过的是：

### `academic-search-workflow`

它已经补入以下能力：

- `OpenAlex + Crossref` 国际文献检索
- 中文艺术与设计期刊的 `CNKI fallback`
- `期刊别名归一化`
- `近5年本地年份过滤`
- 修复后的本地 `CNKI MCP` 调用链

典型适用场景：

- 国际期刊与中文期刊混合检索
- AI、无人机、媒体视听语言、设计、美术、视觉传播等主题综述
- 文献短名单、综述提纲、题录核查

## 部署方法

### 1. 克隆仓库

```powershell
git clone https://github.com/chenjiafu-George/George-skills.git
```

### 2. 运行安装脚本

```powershell
.\install.ps1
```

### 3. 修改本机配置

重点检查：

- `mcp-config/codex/config.portable.template.toml`

需要按新机器改掉的通常有：

- Python 路径
- Chrome 路径
- ChromeDriver 路径
- 本地工作区路径

### 4. 合并到目标机器 Codex 配置

把调整好的 MCP 配置合并到：

```text
C:\Users\<你的用户名>\.codex\config.toml
```

## CNKI MCP 说明

仓库中的 `tools/cnki_mcp_local.py` 是本地修复版包装脚本，不是官方 CNKI 服务。

它的作用是：

- 显式指定本机 Chrome
- 显式指定匹配的 ChromeDriver
- 避开原社区版 MCP 的默认驱动拉取问题
- 支持中文艺术类期刊的检索 fallback

在新机器上部署时，需要重新确认：

- 是否安装了 Chrome
- Chrome 版本与 driver 是否匹配
- Python 路径是否正确

## 相关清单文件

- `docs/skills-manifest.json`
  - skills 名单
- `docs/mcp-manifest.json`
  - MCP 配置名单
- `docs/deploy.md`
  - 部署说明

## 联系方式

- 名称：`George`
- 方向：`具身智能研究员 / 计算机视觉专家`
- Email：`1049138754@qq.com`
- WeChat：`Mr_George_0118`
- 地区：`辽宁 沈阳`

## 海报

海报文件建议放在：

```text
docs/assets/contact/george-poster.jpg
```

![George Poster](docs/assets/contact/george-poster.jpg)

## 微信二维码

二维码文件建议放在：

```text
docs/assets/contact/wechat-qr.jpg
```

![WeChat QR](docs/assets/contact/wechat-qr.jpg)
