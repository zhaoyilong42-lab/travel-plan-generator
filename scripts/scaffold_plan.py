#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scaffold_plan.py — 9 节旅行攻略骨架生成器

功能：
  读取用户输入的 JSON（目的地/天数/人数/预算等），输出一份带占位符的 9 节 Markdown 骨架，
  让 AI 在 WebSearch 研究后直接填充具体内容，保证结构一致。

用法：
  python scaffold_plan.py --input user_input.json --out plan_skeleton.md
  python scaffold_plan.py --destination "Paris" --days "3天2晚" --arrival "CDG 12:00" \
      --party "2成人" --pace "中等" --budget "€1000" --style "出片打卡" \
      --must "铁塔,卢浮宫,凯旋门,迪士尼" --avoid "网红店" --out plan_skeleton.md

输入字段（JSON）：
  destination, days, arrival, party, pace, budget_tier, budget_total,
  accommodation, food, style, must_visit, avoid, other

依赖：仅标准库
"""
import argparse
import json
import sys
from datetime import date


def load_input(args):
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "destination": args.destination or "（待填）",
        "days": args.days or "（待填）",
        "arrival": args.arrival or "（待填）",
        "party": args.party or "（待填）",
        "pace": args.pace or "中等",
        "budget_tier": args.budget_tier or "（待填）",
        "budget_total": args.budget_total or "（待填）",
        "accommodation": args.accommodation or "（待填）",
        "food": args.food or "（参考 assets/user_preferences.md）",
        "style": args.style or "出片打卡",
        "must_visit": args.must or "（待填）",
        "avoid": args.avoid or "（待填）",
        "other": args.other or "（待填）",
    }


def render(d):
    lines = []
    lines.append(f"# {d['destination']} 旅行攻略\n")
    lines.append(f"_生成日期 {date.today().isoformat()}_\n")
    lines.append("> ⚠️ 免责声明：本攻略由 AI 辅助生成，价格/营业状态会变动，出行前请自行核实。\n")

    # 1
    lines.append("## 一、基本信息\n")
    lines.append("| 项目 | 内容 |")
    lines.append("| --- | --- |")
    rows = [
        ("旅行目的地", d["destination"]),
        ("旅游天数", d["days"]),
        ("到达机场/车站与时间", d["arrival"]),
        ("旅游人数", d["party"]),
        ("旅游节奏", d["pace"]),
        ("预算档位 / 总价", f'{d["budget_tier"]} / {d["budget_total"]}'),
        ("住宿要求", d["accommodation"]),
        ("美食要求", d["food"]),
        ("旅行风格", d["style"]),
        ("必打卡", d["must_visit"]),
        ("避坑", d["avoid"]),
        ("其他要求", d["other"]),
    ]
    for k, v in rows:
        lines.append(f"| {k} | {v} |")
    lines.append("")

    # 2
    lines.append("## 二、日程安排（逐小时时间线）\n")
    lines.append("> 🗺️ 每日 Google 地图总路线（点击打开）：[Day1 路线](https://www.google.com/maps/dir/?travelmode=transit)\n")
    lines.append("### Day 1（待填日期）")
    lines.append("| 时间 | 行程节点 | 详细活动与安排说明 |")
    lines.append("| --- | --- | --- |")
    lines.append("| （待填） | （从哪到哪+交通） | （打卡点/时长/餐饮交叉引用） |")
    lines.append("")

    # 3-9 标题占位
    structure = [
        ("三、交通方式与费用", "路段 | 方式 | 时长 / 费用"),
        ("四、餐饮推荐", "先列城市特色美食 → 网红甜点名店 → 按天分表（餐次|餐厅|招牌|人均|位置）"),
        ("五、住宿推荐", "按城市分块各推 3 家（名称|类型|位置/地铁|参考价|备注）"),
        ("六、总预算分配", "项目 | 明细 | 金额（含合计）"),
        ("七、提前预约 / 提前购票", "逐条 + 可点击官网链接"),
        ("八、实用贴士", "8–10 条，贴合目的地"),
        ("九、结束语", "「小泷希望你的旅途愉快 开心的度过每一天」"),
    ]
    for title, cols in structure:
        lines.append(f"## {title}\n")
        lines.append(f"> 格式：{cols}\n")
        lines.append("（待 WebSearch 研究后填充）\n")

    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="生成 9 节旅行攻略骨架")
    p.add_argument("--input", help="用户输入 JSON 文件路径")
    p.add_argument("--out", default="plan_skeleton.md", help="输出骨架文件路径")
    p.add_argument("--destination")
    p.add_argument("--days")
    p.add_argument("--arrival")
    p.add_argument("--party")
    p.add_argument("--pace")
    p.add_argument("--budget_tier")
    p.add_argument("--budget_total")
    p.add_argument("--accommodation")
    p.add_argument("--food")
    p.add_argument("--style")
    p.add_argument("--must")
    p.add_argument("--avoid")
    p.add_argument("--other")
    args = p.parse_args()

    d = load_input(args)
    md = render(d)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 骨架已写入: {args.out}")
    print(f"   目的地={d['destination']} 天数={d['days']} 人数={d['party']} 预算={d['budget_total']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
