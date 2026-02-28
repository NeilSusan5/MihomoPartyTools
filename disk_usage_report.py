#!/usr/bin/env python3
"""
@description 磁盘使用分析报告生成工具
@responsibility 扫描指定目录的磁盘使用情况，生成可视化报告，识别大文件和空间占用热点
"""

import os
import sys
import argparse
from pathlib import Path
from collections import defaultdict

# 文件大小单位转换阈值
SIZE_UNITS = ["B", "KB", "MB", "GB", "TB"]


def format_size(size_bytes):
    """将字节数转换为人类可读的格式"""
    if size_bytes == 0:
        return "0 B"
    unit_index = 0
    size = float(size_bytes)
    while size >= 1024 and unit_index < len(SIZE_UNITS) - 1:
        size /= 1024
        unit_index += 1
    return f"{size:.1f} {SIZE_UNITS[unit_index]}"


def get_dir_size(path):
    """
    递归计算目录的总大小

    :param path: 目标目录路径
    :return: 目录总大小（字节）
    """
    total = 0
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat(follow_symlinks=False).st_size
                elif entry.is_dir(follow_symlinks=False):
                    total += get_dir_size(entry.path)
            except (PermissionError, OSError):
                # 跳过无权限访问的文件
                pass
    except (PermissionError, OSError):
        pass
    return total


def scan_directory(target_path, top_n=10, large_file_threshold_mb=100):
    """
    扫描目标目录，收集磁盘使用数据

    :param target_path: 扫描的根目录
    :param top_n: 显示前 N 个最大的子目录和文件
    :param large_file_threshold_mb: 大文件判定阈值（MB）
    :return: 扫描结果字典
    """
    target = Path(target_path).resolve()
    if not target.exists():
        print(f"错误: 路径 '{target}' 不存在")
        sys.exit(1)
    if not target.is_dir():
        print(f"错误: '{target}' 不是一个目录")
        sys.exit(1)

    # 大文件判定阈值转换为字节
    threshold_bytes = large_file_threshold_mb * 1024 * 1024

    # 收集子目录大小
    subdirs = []
    # 收集大文件列表
    large_files = []
    # 按扩展名统计文件大小
    ext_stats = defaultdict(lambda: {"count": 0, "size": 0})
    # 总文件数和总大小
    total_files = 0
    total_size = 0

    print(f"正在扫描目录: {target} ...")

    # 扫描一级子目录的大小
    try:
        for entry in os.scandir(target):
            try:
                if entry.is_dir(follow_symlinks=False):
                    dir_size = get_dir_size(entry.path)
                    subdirs.append((entry.name, dir_size))
            except (PermissionError, OSError):
                pass
    except (PermissionError, OSError):
        print("警告: 部分目录无法访问")

    # 递归扫描所有文件
    for root, dirs, files in os.walk(target):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for filename in files:
            if filename.startswith('.'):
                continue
            filepath = os.path.join(root, filename)
            try:
                file_size = os.path.getsize(filepath)
                total_files += 1
                total_size += file_size

                # 按扩展名归类统计
                ext = Path(filename).suffix.lower() or "(无扩展名)"
                ext_stats[ext]["count"] += 1
                ext_stats[ext]["size"] += file_size

                # 记录大文件
                if file_size >= threshold_bytes:
                    rel_path = os.path.relpath(filepath, target)
                    large_files.append((rel_path, file_size))
            except (PermissionError, OSError):
                pass

    return {
        "target": str(target),
        "total_files": total_files,
        "total_size": total_size,
        "subdirs": sorted(subdirs, key=lambda x: x[1], reverse=True)[:top_n],
        "large_files": sorted(large_files, key=lambda x: x[1], reverse=True)[:top_n],
        "ext_stats": dict(
            sorted(ext_stats.items(), key=lambda x: x[1]["size"], reverse=True)[:top_n]
        ),
    }


def print_bar(ratio, width=30):
    """生成文本进度条"""
    filled = int(width * ratio)
    bar = "█" * filled + "░" * (width - filled)
    return bar


def print_report(result, top_n=10):
    """
    打印磁盘使用分析报告

    :param result: scan_directory 返回的扫描结果
    :param top_n: 显示条目数量上限
    """
    print("\n" + "=" * 60)
    print("          磁盘使用分析报告")
    print("=" * 60)
    print(f"  扫描目录: {result['target']}")
    print(f"  文件总数: {result['total_files']:,}")
    print(f"  占用空间: {format_size(result['total_size'])}")
    print("=" * 60)

    # 子目录空间占用排行
    if result["subdirs"]:
        print(f"\n📁 子目录空间占用 TOP {top_n}:")
        print("-" * 55)
        max_size = result["subdirs"][0][1] if result["subdirs"] else 1
        for name, size in result["subdirs"]:
            ratio = size / max_size if max_size > 0 else 0
            bar = print_bar(ratio, 20)
            print(f"  {bar} {format_size(size):>10}  {name}/")

    # 大文件列表
    if result["large_files"]:
        print(f"\n🔍 大文件列表:")
        print("-" * 55)
        for filepath, size in result["large_files"]:
            print(f"  {format_size(size):>10}  {filepath}")
    else:
        print("\n✅ 未发现超出阈值的大文件")

    # 按扩展名统计
    if result["ext_stats"]:
        print(f"\n📊 文件类型统计 TOP {top_n}:")
        print("-" * 55)
        print(f"  {'扩展名':<15} {'文件数':>8} {'总大小':>12}")
        print(f"  {'─' * 15} {'─' * 8} {'─' * 12}")
        for ext, stats in result["ext_stats"].items():
            print(f"  {ext:<15} {stats['count']:>8,} {format_size(stats['size']):>12}")

    print("\n" + "=" * 60)
    print("  报告生成完毕")
    print("=" * 60 + "\n")


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="磁盘使用分析报告工具 - 扫描目录并生成空间占用报告"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="要扫描的目录路径（默认: 当前目录）",
    )
    parser.add_argument(
        "-n", "--top",
        type=int,
        default=10,
        help="显示排行榜的条目数（默认: 10）",
    )
    parser.add_argument(
        "-t", "--threshold",
        type=int,
        default=100,
        help="大文件判定阈值，单位 MB（默认: 100）",
    )
    return parser.parse_args()


def main():
    """主入口函数"""
    args = parse_args()
    result = scan_directory(args.path, top_n=args.top, large_file_threshold_mb=args.threshold)
    print_report(result, top_n=args.top)


if __name__ == "__main__":
    main()
