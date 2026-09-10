#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_shops.py — 店铺营业状态核实助手

功能：
  给定一组店铺名（可选城市），生成 WebSearch 查询模板 + Markdown 结果记录表骨架，
  让 AI 逐项核实「是否仍在营业」后回填状态与替代店。

用法：
  python verify_shops.py --city "Paris" "Ladurée Champs-Élysées" "Pierre Hermé 86 Champs" "Bouillon Chartier"
  python verify_shops.py "店A" "店B"            # 不带城市

依赖：仅标准库
"""
import argparse
import sys


def build_queries(shop: str, city: str):
    c = f" {city}" if city else ""
    q_closed = f"{shop}{c} permanently closed 2026".strip()
    q_open = f"{shop}{c} still open 2026".strip()
    return q_closed, q_open


def main():
    p = argparse.ArgumentParser(description="生成店铺营业状态核实用的搜索查询 + 记录表")
    p.add_argument("shops", nargs="+", help="店铺名列表")
    p.add_argument("--city", default="", help="城市名，用于拼接搜索词")
    args = p.parse_args()

    shops = args.shops
    city = args.city

    print("# 店铺营业状态核实表\n")
    print("> 优先信源：店官网 > Google Maps(看是否标 Permanently closed) > "
          "Tripadvisor/Yelp 评论 > Sortiraparis/Time Out 本地资讯")
    print("> 出现 permanently closed / 永久停业 / fermé définitivement → 淘汰，用同区域同类型替代\n")

    print("| # | 店铺 | 搜索查询(closed) | 搜索查询(open) | 状态(营业/停业) | 替代店 |")
    print("| --- | --- | --- | --- | --- | --- |")
    for i, s in enumerate(shops, 1):
        qc, qo = build_queries(s, city)
        print(f"| {i} | {s} | `{qc}` | `{qo}` | ? | ? |")

    print("\n## 逐店搜索建议")
    for i, s in enumerate(shops, 1):
        qc, qo = build_queries(s, city)
        print(f"{i}. **{s}**")
        print(f"   - 查停业: `{qc}`")
        print(f"   - 查在营: `{qo}`")

    return 0


if __name__ == "__main__":
    sys.exit(main())
