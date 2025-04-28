#!/usr/venv/django/bin/python

"""
webp_converter.py - 图片转 WebP 工具

用法:
  python webp_converter.py [图片路径1] [图片路径2] ...

示例:
  python webp_converter.py ./1.png ~/images/photo.jpg
"""

import argparse
from pathlib import Path
from PIL import Image
import sys


def convert_image(
    input_path: Path,
    output_dir: Path = None,
    max_size: int = 200,
    quality: int = 75,
    replace_original: bool = False,
) -> bool:
    """转换单张图片为 WebP 格式"""
    try:
        with Image.open(input_path) as img:
            # 保留透明度
            if img.mode in ("RGBA", "LA", 'P'):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")

            # 保持比例缩放
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

            # 生成输出路径
            if replace_original:
                output_path = input_path.with_suffix(".webp")
            else:
                output_dir = output_dir or input_path.parent
                output_path = output_dir / f"{input_path.stem}.webp"

            # 保存为 WebP
            img.save(
                output_path,
                "WEBP",
                quality=quality,
                method=6,
                lossless=False,
                optimize=True,
            )

            return True
    except Exception as e:
        print(f"错误处理 {input_path.name}: {str(e)}", file=sys.stderr)
        return False


def main():
    # 配置命令行参数
    parser = argparse.ArgumentParser(
        description="将图片转换为 WebP 格式",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="要转换的图片路径（支持通配符）\n示例: python webp_converter.py *.png",
    )
    parser.add_argument("-o", "--output", help="输出目录（默认同输入文件目录）")
    parser.add_argument(
        "-r", "--replace", action="store_true", help="替换原始文件（默认保留原文件）"
    )
    parser.add_argument(
        "-q", "--quality", type=int, default=75, help="压缩质量 (1-100，默认 75)"
    )
    parser.add_argument(
        "-s", "--size", type=int, default=200, help="最大边长像素（默认 200）"
    )

    args = parser.parse_args()

    # 验证质量参数
    if not 1 <= args.quality <= 100:
        print("错误：质量参数必须介于 1-100 之间", file=sys.stderr)
        sys.exit(1)

    # 处理输出目录
    output_dir = Path(args.output).resolve() if args.output else None
    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    # 转换统计
    total = 0
    success = 0

    # 处理所有输入文件
    for file_pattern in args.files:
        for input_path in Path().glob(file_pattern):
            if not input_path.is_file():
                continue

            total += 1
            if convert_image(
                input_path=input_path,
                output_dir=output_dir,
                max_size=args.size,
                quality=args.quality,
                replace_original=args.replace,
            ):
                success += 1
                print(f"转换成功: {input_path} → {input_path.with_suffix('.webp')}")
            else:
                print(f"转换失败: {input_path}")

    # 输出统计信息
    print(f"\n转换完成: 共处理 {total} 个文件")
    print(f"成功: {success} 个")
    print(f"失败: {total - success} 个")


if __name__ == "__main__":
    main()
