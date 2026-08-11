#!/usr/bin/env python3
"""Preview or safely organize direct files from a local folder."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

DEFAULT_RULES = {
    "文档": ".pdf .doc .docx .odt .rtf .txt .md .csv .epub",
    "表格": ".xls .xlsx .xlsm .ods",
    "演示文稿": ".ppt .pptx .odp .key",
    "图片": ".jpg .jpeg .png .gif .webp .bmp .tif .tiff .svg .heic",
    "音频": ".mp3 .wav .flac .m4a .aac .ogg",
    "视频": ".mp4 .mov .mkv .avi .wmv .webm",
    "压缩包": ".zip .rar .7z .tar .gz .bz2 .xz",
    "代码": ".py .js .ts .jsx .tsx .java .c .cpp .cs .go .rs .html .css .json .yaml .yml .xml .sql .ipynb",
    "安装包": ".exe .msi .dmg .pkg .apk .deb .rpm",
}
EXTENSION_MAP = {ext: category for category, exts in DEFAULT_RULES.items() for ext in exts.split()}
RULES_FILENAME = ".organize-local-files-rules.json"
INVALID_CATEGORY_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Folder whose direct files will be organized")
    parser.add_argument("--destination", type=Path, help="Archive root; default: SOURCE/已整理")
    parser.add_argument("--apply", action="store_true", help="Move files. Without this flag, only preview.")
    parser.add_argument("--collision-policy", choices=("safe", "skip", "newer-wins"), default="safe")
    parser.add_argument("--learn", action="append", default=[], metavar=".EXT=CATEGORY", help="Persist a category for an extension")
    parser.add_argument("--report", type=Path, help="Write the result JSON to this path")
    return parser.parse_args()


def load_rules(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return {str(k).lower(): str(v) for k, v in data.items() if str(k).startswith(".") and str(v)}
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Cannot read rules file {path}: {error}") from error


def add_learned_rules(items: list[str], rules: dict[str, str]) -> None:
    for item in items:
        if "=" not in item:
            raise ValueError(f"Invalid --learn value {item!r}; use .ext=category")
        extension, category = (part.strip() for part in item.split("=", 1))
        if not extension.startswith(".") or len(extension) == 1 or not category:
            raise ValueError(f"Invalid --learn value {item!r}; use .ext=category")
        if INVALID_CATEGORY_CHARS.search(category) or category in {".", ".."}:
            raise ValueError(f"Unsafe category name: {category!r}")
        rules[extension.lower()] = category


def alternate_path(path: Path) -> Path:
    for index in range(1, 10000):
        candidate = path.with_name(f"{path.stem} ({index}){path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Too many name collisions for {path.name}")


def decide(source: Path, target: Path, policy: str) -> tuple[str, Path]:
    if not target.exists():
        return "move", target
    source_stat, target_stat = source.stat(), target.stat()
    same_time = abs(source_stat.st_mtime - target_stat.st_mtime) <= 2
    if source_stat.st_size == target_stat.st_size and same_time:
        return "skip-duplicate", target
    if policy == "skip":
        return "skip-conflict", target
    if policy == "newer-wins" and source_stat.st_mtime > target_stat.st_mtime:
        return "overwrite", target
    return "rename", alternate_path(target)


def main() -> int:
    args = parse_args()
    source = args.source.expanduser().resolve()
    if not source.is_dir():
        raise ValueError(f"Source is not a directory: {source}")
    destination = (args.destination.expanduser() if args.destination else source / "已整理").resolve()
    if destination == source:
        raise ValueError("Destination must not be the source directory")
    rules_file = destination / RULES_FILENAME
    learned = load_rules(rules_file)
    add_learned_rules(args.learn, learned)
    categories = EXTENSION_MAP | learned
    plans, unknown = [], set()
    for item in source.iterdir():
        if not item.is_file() or item.is_symlink() or item.name.startswith("."):
            continue
        extension = item.suffix.lower()
        category = categories.get(extension, "其他")
        if category == "其他":
            unknown.add(extension or "[无扩展名]")
        month = datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m")
        target = destination / category / month / item.name
        action, final_target = decide(item, target, args.collision_policy)
        plans.append({"source": str(item), "destination": str(final_target), "action": action, "category": category})
    if args.apply:
        destination.mkdir(parents=True, exist_ok=True)
        if args.learn:
            rules_file.write_text(json.dumps(learned, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for plan in plans:
            if plan["action"].startswith("skip"):
                continue
            target = Path(plan["destination"])
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(plan["source"], target)
    report = {"mode": "apply" if args.apply else "preview", "source": str(source), "destination": str(destination), "collision_policy": args.collision_policy, "summary": dict(Counter(p["action"] for p in plans)), "unknown_extensions": sorted(unknown), "plans": plans}
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.expanduser().write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(2)
