# 店铺营业状态核实铁律（MUST VERIFY BEFORE LISTING）

> 任何具体店铺（餐厅 / 甜点店 / 马卡龙店 / 酒店 / 网红打卡店 / 特色小吃店）在写入攻略前，**必须先核实当前是否仍在营业**。硬性约束，不允许跳过。

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

## 通用核实清单（每份攻略生成前自检）
- [ ] 第 4 节每家「餐厅 / 甜点店」已 WebSearch 验证 2026 仍在营业
- [ ] 淘汰店铺已用同区域、同类型、已验证替代店替换
- [ ] 第 5 节每家「酒店」已在 Booking / Tripadvisor 确认可订、价位与描述一致
- [ ] 第 7 节每个景点门票「官网链接」已 WebSearch 核实真实可访问
- [ ] 攻略发布前再扫一遍，无 "permanently closed / 已停业 / 关门" 字样的店

## 辅助工具
- `scripts/verify_shops.py`：输入店铺名列表，自动生成 WebSearch 查询模板 + 结果记录表骨架。
  ```bash
  python scripts/verify_shops.py --city "Paris" "Ladurée Champs-Élysées" "Pierre Hermé 86 Champs"
  ```
