"""
Reads Distribution 折线图绘制脚本
===================================
读取 data/*.read_distribution.report.txt 文件，提取各 Group 的 Tags/Kb 数据；
读取 all.summary.tsv 文件，提取各样品的 total bases(G) 数据；
按样品绘制多组折线图并保存为 PNG 图片。

输入：
    - data/ 目录下的 .read_distribution.report.txt 文件
    - all.summary.tsv（可选，用于绘制 total bases 虚线）
输出：reads_distribution.png

用法：
    python plot_reads_distribution.py                          # 按样品名数值排序
    python plot_reads_distribution.py sample_order.txt         # 按指定顺序文件排序

顺序文件格式：每行一个样品名，空行和 # 开头的注释行会被忽略。
示例：
    # 样品顺序
    9
    5
    7

依赖：matplotlib
"""

import csv
import glob
import sys
from pathlib import Path

import matplotlib.pyplot as plt


def parse_sample_name(filepath: str) -> str:
    """
    从文件路径中提取样品名。

    文件名格式：{样品名}.read_distribution.report.txt
    以 "." 分割文件名，取第一个元素作为样品名。

    示例：
        "data/5.read_distribution.report.txt" → "5"
        "data/Sample_A.read_distribution.report.txt" → "Sample_A"
    """
    return Path(filepath).name.split(".")[0]


def parse_report(filepath: str) -> dict[str, float]:
    """
    
    # RSeQC
    sample=$(echo $(basename $PWD))
    /data/software/miniconda3/bin/read_distribution.py \
    -i ${sample}.sorted.markdup.BQSR.bam \
    -r /data/ref/hg38.ensembl.bed >read_distribution.report.txt

    解析单个报告文件，提取 Group 与 Tags/Kb 列的数据。

    文件内容结构（示意）：
        Total Reads                   52344019
        Total Tags                    61472809
        =====================================================================
        Group               Total_bases         Tag_count           Tags/Kb
        CDS_Exons           38513803            14445252            375.07
        ...
        =====================================================================

    解析策略：
        1. 定位第一个 "=====" 行，进入数据表格区域
        2. 跳过表头行（以 "Group" 开头）
        3. 逐行按空白字符分割，取第 0 列（Group）和第 3 列（Tags/Kb）
        4. 遇到第二个 "=====" 行时结束解析

    返回：{Group名称: Tags/Kb数值} 字典
    """
    data: dict[str, float] = {}
    in_table = False  # 标记是否进入数据表格区域
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            # 遇到分隔线：第一次进入表格，第二次退出
            if line.startswith("====="):
                if in_table:
                    break  # 第二个分隔线，结束解析
                in_table = True
                continue
            # 跳过非表格内容：空行、尚未进入表格、表头行
            if not in_table or not line or line.startswith("Group"):
                continue
            # 按空白字符分割每行，列顺序固定：Group | Total_bases | Tag_count | Tags/Kb
            parts = line.split()
            group = parts[0]              # 第 0 列：Group 名称
            tags_per_kb = float(parts[3])  # 第 3 列：Tags/Kb 数值
            data[group] = tags_per_kb
    return data


def load_sample_order(order_file: str) -> list[str]:
    """
    从顺序文件中读取样品名列表，每行一个样品名。

    文件格式：
        - 每行写一个样品名（与文件名中提取的样品名一致）
        - 空行和以 "#" 开头的注释行自动忽略
        - 行首行尾空白自动去除

    示例文件内容：
        # 按实验条件排序
        9
        5
        7

    返回：按文件中出现顺序排列的样品名列表
    """
    sample_order: list[str] = []
    with open(order_file, encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            # 跳过空行和注释行
            if not stripped or stripped.startswith("#"):
                continue
            sample_order.append(stripped)
    return sample_order


def parse_summary(filepath: str = "all.summary.tsv") -> dict[str, float]:
    """
    解析 all.summary.tsv 文件，提取各样品的 total bases(G) 数据。

    文件格式（TSV，制表符分隔）：
        Sample	total reads(M)	total bases(G)	...
        5	54.84	8.23	...
        7	131.29	19.69	...
        ...

    返回：{样品名: total_bases(G)值} 字典。
          若文件不存在或解析失败，返回空字典。
    """
    summary: dict[str, float] = {}
    try:
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                sample = row["Sample"].strip()
                total_bases = float(row["total bases(G)"])
                summary[sample] = total_bases
    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"警告：读取 {filepath} 失败 — {e}，total bases 虚线将不会绘制。")
    return summary


def load_all_data(
    pattern: str = "data/*.read_distribution.report.txt",
    order_file: str | None = None,
    summary_file: str = "all.summary.tsv",
) -> tuple[dict[str, dict[str, float]], list[str], dict[str, float]]:
    """
    遍历所有匹配的报告文件，组装完整的多样品数据，
    同时加载 all.summary.tsv 中的 total bases 数据。

    处理流程：
        1. glob 匹配所有符合条件的报告文件
        2. 确定样品排序方式（顺序文件 > 字符串排序）
        3. 逐个文件解析 Reads Distribution 数据
        4. 加载 total bases(G) 数据

    排序规则：
        - 若提供了 order_file，按文件中列出的顺序排列样品，
          仅包含顺序文件中列出的样品，未在顺序文件中的报告文件会被跳过。
        - 若未提供 order_file，按样品名字符串升序排列。

    参数：
        pattern:      文件匹配模式，默认 "data/*.read_distribution.report.txt"
        order_file:   可选，样品顺序文件路径，每行一个样品名
        summary_file: all.summary.tsv 文件路径

    返回：
        - all_data:      {Group名称: {样品名: Tags/Kb值}} 的嵌套字典
        - sample_names:  按指定顺序排列的样品名列表，用于 x 轴刻度
        - total_bases:   {样品名: total_bases(G)值} 字典
    """
    # 用字典映射 {样品名: 文件路径}，便于按指定顺序查找
    file_map: dict[str, str] = {}
    for filepath in glob.glob(pattern):
        sample = parse_sample_name(filepath)
        file_map[sample] = filepath

    # 确定样品排序顺序
    if order_file is not None:
        # 按顺序文件指定的顺序排列，只包含顺序文件中列出的样品
        ordered_samples = load_sample_order(order_file)
        sample_names = [s for s in ordered_samples if s in file_map]
        # 若顺序文件中有找不到报告的样品，给出提示
        missing = [s for s in ordered_samples if s not in file_map]
        if missing:
            print(f"警告：以下样品在 data 目录中未找到对应报告文件，已跳过：{missing}")
    else:
        # 默认：按样品名字符串升序排列
        sample_names = sorted(file_map.keys())

    # 按确定的顺序依次解析每个报告文件
    all_data: dict[str, dict[str, float]] = {}
    for sample in sample_names:
        report = parse_report(file_map[sample])
        for group, value in report.items():
            # setdefault：首次遇到该 Group 时创建空字典，然后填入 {样品名: 值}
            all_data.setdefault(group, {})[sample] = value

    # 加载 total bases 数据
    total_bases = parse_summary(summary_file)

    return all_data, sample_names, total_bases


def plot_line_chart(
    data: dict[str, dict[str, float]],
    sample_names: list[str],
    total_bases: dict[str, float] | None = None,
    output_path: str = "reads_distribution.png",
) -> None:
    """
    绘制多组折线图并保存为 PNG 文件。

    图表结构：
        - x 轴：样品名（按 order_file 或字符串排序的样品列表）
        - 左 y 轴（Tags/Kb）：每条折线代表一个 Group，不同颜色区分
        - 右 y 轴（Total Bases (G)）：黑色虚线，表示各样品的 total bases
        - 数据点用圆点标记；total bases 用三角标记
        - 图例放置在图表右侧外部，避免遮挡数据

    参数：
        data:          {Group名称: {样品名: Tags/Kb值}} 嵌套字典
        sample_names:  x 轴样品名列表（已按指定顺序排列）
        total_bases:   {样品名: total_bases(G)值} 字典，None 则跳过虚线
        output_path:   输出图片路径，默认 "reads_distribution.png"
    """
    # 创建画布与主坐标轴，尺寸 12×7 英寸，确保 10 条折线图例不拥挤
    fig, ax1 = plt.subplots(figsize=(12, 7))

    # ---- 左 y 轴：Tags/Kb 折线 ----
    for group, values in data.items():
        # 从嵌套字典中取出该 Group 在各样品中的 Tags/Kb 值
        # 若某样品缺少该 Group 数据，用 NaN 填充（matplotlib 会自动断开线条）
        y = [values.get(s, float("nan")) for s in sample_names]
        # marker='o'：在每个数据点绘制圆点标记
        ax1.plot(sample_names, y, marker="o", label=group)

    ax1.set_xlabel("Sample")
    ax1.set_ylabel("Tags/Kb")
    ax1.grid(True, alpha=0.3)

    # ---- 右 y 轴：Total Bases (G) 虚线 ----
    if total_bases:
        # 从 total_bases 字典中取出各样品对应的值，缺少则用 NaN
        tb_y = [total_bases.get(s, float("nan")) for s in sample_names]
        # 仅当至少有一个有效数值时才绘制
        if any(v == v for v in tb_y):  # NaN != NaN，利用此特性判断
            ax2 = ax1.twinx()  # 创建共享 x 轴的第二 y 轴
            ax2.plot(
                sample_names, tb_y,
                color="black", linestyle="--", marker="^", linewidth=1.5,
                label="Total Bases (G)",
            )
            ax2.set_ylabel("Total Bases (G)")

    # ---- 标题与图例 ----
    plt.title("Reads Distribution by Group")

    # 合并左右轴的图例，统一放置在图表右侧外部
    lines1, labels1 = ax1.get_legend_handles_labels()
    if total_bases and any(v == v for v in tb_y):
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, bbox_to_anchor=(1.02, 1), loc="upper left")
    else:
        ax1.legend(bbox_to_anchor=(1.02, 1), loc="upper left")

    # 自动调整布局，确保图例不被裁剪
    fig.tight_layout()

    # 保存图片，dpi=150 保证清晰度
    fig.savefig(output_path, dpi=150)
    plt.close(fig)  # 释放内存
    print(f"Saved: {output_path}")


def main() -> None:
    """
    主入口：解析命令行参数 → 加载数据 → 绘图 → 保存。

    命令行用法：
        python plot_reads_distribution.py                          # 默认数值排序
        python plot_reads_distribution.py sample_order.txt         # 按顺序文件排序
    """
    order_file: str | None = None
    if len(sys.argv) > 1:
        order_file = sys.argv[1]

    data, sample_names, total_bases = load_all_data(order_file=order_file)
    plot_line_chart(data, sample_names, total_bases=total_bases)


if __name__ == "__main__":
    main()
