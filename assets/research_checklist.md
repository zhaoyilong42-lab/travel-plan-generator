# 营业 / 开放状态核实铁律（MUST VERIFY BEFORE LISTING）

> 任何具体**店铺**（餐厅 / 甜点店 / 马卡龙店 / 酒店 / 网红打卡店 / 特色小吃店）或**景点 / 游乐项目**（景点 / 博物馆 / 观景台 / 游乐设施 / 演出 / 巡游 / 烟花 / 缆车）在写入攻略前，**必须先核实当前是否仍在营业 / 开放运营**。硬性约束，不允许跳过。本文件分两部分：① 店铺核实（见下）② 景点 / 游乐项目核实（见末尾新加小节）。

## 核实步骤（强制 3 步）
1. **WebSearch 搜索**：「店名 + 城市 + permanently closed / still open 2026」或「店名 + closed」。
   - 优先信源：**店官网** > **Google Maps**（看是否标 "Permanently closed / 永久停业"）> **Tripadvisor / Yelp 评论区**提到关门 > **Sortiraparis / Time Out 等本地资讯站**停业通告。
   - 出现 "permanently closed / 永久停业 / fermé définitivement / 已关闭" → 直接淘汰，找替代。
2. **替代方案**：淘汰店必须用**同类型、同区域、已确认营业**的店替换（替换店再次走步骤 1 验证）；不要因找不到替代就留着关门的店。
3. **写进攻略时**：在第 4 节 / 网红甜点表里，每家店标注「✅ 已验证 2026 仍在营业」；用户对某店有疑问时，让他看 Google Maps / 店官网自查。

## 反例（禁止）
- 用户说"你推荐的店都永久停业"时，还在回复里继续推同一批店。
- 只看 1 篇过时博客（2022/2023）就信以为真写进攻略。
- 写"营业时间见官网"就想跳过验证 —— 不行，必须主动确认"是否仍在营业"，这是两个问题。

## 正例
- 推 Ladurée：搜「Ladurée Champs-Élysées still open 2025」→ 见 "reopened its doors, totally transformed" → 确认营业 → 写入。
- 推 Pierre Hermé：搜「Pierre Hermé 86 Champs permanently closed」→ sortiraparis.com 标 "permanently closed" → 淘汰 → 改推 Ladurée / Jean-Paul Hévin / Carette。

## 景点 / 游乐项目运营状态核实（MUST VERIFY BEFORE LISTING）

> 任何**景点、博物馆、观景台、游乐设施、演出、巡游、烟花、缆车、电梯观光**等写入攻略前，**必须先核实当前是否开放运营**。硬性约束，不允许跳过。**主题公园**（迪士尼 / Universal 等）的设施与演出**季节性检修、临时关闭**极常见，必须查当日状态，而非仅信旧博客。

### 核实步骤（强制）
1. **官方网站 / 官方 APP 查当日运营**：景点官网的「开放时间 / 临时关闭 / 维护 / Closure」页 > 官方 APP（如 Disneyland Paris APP 查设施实时开放）> WebSearch「景点名 + temporarily closed / under refurbishment / 2026 开放 / season closure」> Google Maps（看是否标 "Permanently closed / 已关闭"）。
   - 出现「temporarily closed / 暂时关闭 / under refurbishment / 翻新中 / 已关闭 / closed for maintenance」→ 不得写入必玩，替换或剔除。
2. **替代 / 剔除**：已关闭 / 停运的项目**不得写入攻略**；能用同区域可替代项目替换就替换（替换项再次走步骤 1），否则直接从行程剔除，并在备注说明「已核实 X 月 X 日关闭」。
3. **写进攻略时**：在行程 / 第 8 节注明「✅ 已核实 2026 开放（核实日期）」或明确标注关闭；用户对某项目有疑问时，让他查官网 / APP 自查。核实方法与店铺完全一致，可复用 `scripts/verify_shops.py`（传入景点 / 设施名列表即可批量生成查询）。

### 反例（禁止）
- 用户说「XX 项目停运了」，还在攻略里写「登顶 XX / 看 XX 演出」。
- 只看过时博客（2022/2023）就写「XX 演出每天都有」，实际已停演或改期。
- 把主题公园设施当「永久开放」写，不查当日检修；用户到了发现设施关闭。
- 推「登顶某观景台」前不核实，结果该观景台已关闭或暂停开放。

### 正例
- 写迪士尼行程：先查 Disneyland Paris APP 当日设施开放 → 某设施标 "Temporarily closed for refurbishment" → 不写进必玩，改推开放设施。
- 写凯旋门：查官网 paris-arc-de-triomphe.fr → 顶层平台 2026 开放（€16/€22，含 284 级台阶）→ 写入并标注核实日期；若官网标关闭则改外观拍照打卡。
- 写埃菲尔铁塔顶层：查官网 → 当日是否开放 / 当日票务 → 写入或改顶层以外方案。

## 通用核实清单（每份攻略生成前自检）
- [ ] 第 4 节每家「餐厅 / 甜点店」已 WebSearch 验证 2026 仍在营业
- [ ] 淘汰店铺已用同区域、同类型、已验证替代店替换
- [ ] 第 5 节每家「酒店」已在 Booking / Tripadvisor 确认可订、价位与描述一致
- [ ] 第 7 节每个景点门票「官网链接」已 WebSearch 核实真实可访问
- [ ] 第 2 节每个「景点 / 游乐设施 / 演出 / 巡游 / 烟花」已 WebSearch + 官网 / 官方 APP 核实**当前开放运营**（主题公园须查当日）
- [ ] 已关闭 / 停运的景点 / 设施已**剔除**或用同区域替代，并在行程注明核实日期
- [ ] 攻略发布前再扫一遍，无 "permanently closed / temporarily closed / 已停业 / 已关闭 / 停运 / 关门" 字样的店或景点

## 辅助工具
- `scripts/verify_shops.py`：输入店铺名列表，自动生成 WebSearch 查询模板 + 结果记录表骨架。
  ```bash
  python scripts/verify_shops.py --city "Paris" "Ladurée Champs-Élysées" "Pierre Hermé 86 Champs"
  ```
