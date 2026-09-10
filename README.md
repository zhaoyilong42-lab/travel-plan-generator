# travel-plan-generator（小泷 · 旅行攻略生成 Skill）

专业旅行攻略生成 Skill，可接入 **WorkBuddy AI** 使用。输入目的地 / 天数 / 人数 / 预算 / 节奏 / 美食 / 打卡等需求，联网检索真实数据，生成结构严谨、可直接照走的旅行攻略（10 节，含购物和伴手礼）。

## ✨ 功能亮点

- **10 节固定结构**：基本信息 → 日程 → 交通 → 餐饮 → 住宿 → 购物 → 预算 → 预约 → 贴士 → 结束语
- **逐小时时间线** + 每日 Google 地图路线
- 餐厅附 **📍 Google Maps 跳转**、酒店附 **🔗 Booking.com 跳转**
- 严格的「就近用餐」「店铺营业核实（WebSearch + Google Maps）」铁律
- 内置用户偏好约束（不吃奇形怪状食材、不排网红店等，可按当次需求覆盖）
- 每篇攻略以固定签名收尾：「小泷希望你的旅途愉快 开心的度过每一天」

## 📦 安装（给别人用的方式）

把本仓库的 `travel-plan-generator/` 目录**整体**复制到 WorkBuddy 的 skills 目录：

- Windows：`%USERPROFILE%\.workbuddy-ai\skills\travel-plan-generator\`
- macOS / Linux：`~/.workbuddy-ai/skills/travel-plan-generator/`

复制后**重启 WorkBuddy**，在对话里直接说「帮我做一份巴黎 3 天攻略」「生成东京 5 天路线」等需求即可触发。

也可以 `git clone` 后把目录软链 / 复制到上述路径。

## 🌐 跨 Agent / 跨客户端使用（不只 WorkBuddy）

本 skill 的方法论是**纯 Markdown + Python**，与具体客户端无关。除 WorkBuddy 外，Codex、Claude Code、Cursor 等也能直接用：

- **Codex / 兼容 AGENTS.md 的客户端**：仓库根目录已含 `AGENTS.md`（本文件即入口指令），在此目录启动 Agent 即自动加载。
- **Claude Code**：把整个 `travel-plan-generator/` 复制到 `~/.claude/skills/travel-plan-generator/`（`SKILL.md` 格式与 Claude Code 技能兼容，会被识别为技能）；或在项目根保留 `CLAUDE.md`。
- **通用**：任何能读 Markdown 指令的 Agent，把仓库内容纳入上下文即可按规则生成攻略。

`AGENTS.md` / `CLAUDE.md` 内含**精简但完整**的 10 节规则与脚本用法，即使只读一个文件也能产出合规攻略；需要权威细节时再读 `SKILL.md` 与 `assets/`。

## 🗂 目录结构

```
travel-plan-generator/
├── SKILL.md                   # 角色、三条铁律、调用流程（必须）
├── assets/
│   ├── output_structure.md    # 10 节完整格式规范
│   ├── user_preferences.md    # 用户长期偏好（硬约束）
│   ├── research_checklist.md  # 店铺营业核实铁律 + 自查清单
│   └── shop_lists.md          # 已核实店铺白/黑名单（可复用+更新）
├── scripts/
│   ├── scaffold_plan.py       # 由 JSON/参数生成 9 节骨架（仅标准库）
│   ├── verify_shops.py        # 批量生成店铺营业核实查询（仅标准库）
│   └── md2pdf.py              # 跨平台 Markdown → (MD + PDF) 导出（需 reportlab）
└── references/                # 风格对齐用样例攻略（可删）
    ├── 意大利路线一_打卡式.md
    ├── 意大利路线二_休闲式.md
    └── 罗马_3天_含购物甜点样例.md
```

## 🔧 依赖

- `scaffold_plan.py` / `verify_shops.py` 仅用 **Python 标准库**，无需 `pip install`。
- `md2pdf.py`（PDF 导出）需安装 **reportlab**：`pip install reportlab`。
- 攻略正文为 Markdown，WorkBuddy 读取 `SKILL.md` 后自动加载。

## 📄 PDF 导出（一键出 MD + PDF）

本仓库自带跨平台导出脚本 `scripts/md2pdf.py`，读入一份 Markdown 路线，**同时产出 `.md` 文档与 `.pdf` 文档**：

```bash
pip install reportlab
python scripts/md2pdf.py 路线.md                 # 在同目录生成 路线.md + 路线.pdf
python scripts/md2pdf.py 路线.md --out out/      # 指定输出目录
python scripts/md2pdf.py 路线.md --out 路线.pdf   # 直接指定 PDF 路径
python scripts/md2pdf.py 路线.md --font /path/to/font.ttc  # 手动指定字体
```

中文字体**自动探测**，无需写死路径：

- Windows：微软雅黑 `msyh.ttc` / SimSun / SimHei
- macOS：苹方 `PingFang.ttc` / Arial Unicode
- Linux：Noto Sans CJK / 文泉驿 `wqy`

若系统无中文字体，脚本会提示安装（Linux：`apt install fonts-noto-cjk` 或 `fonts-wqy-zenhei`）。

## 🤝 贡献

欢迎补充 `assets/shop_lists.md` 里已核实的店铺，或提交 Issue / PR 改进结构与规范。

## 📜 License

MIT
