---
name: organize-local-files
description: Safely organize cluttered local folders such as Downloads and Desktop by file type and modification date. Use when Codex needs to preview or move local files into category folders, resolve duplicate filenames by size and timestamp, or learn a user's preferred category for an unknown extension.
---

# 智能本地文件整理

使用 `scripts/organize_files.py` 整理用户明确指定的本地目录。默认只生成预览，绝不移动、覆盖或删除文件。

## 工作流程

1. 确认范围：只处理用户点名的来源目录；排除隐藏文件、文件夹和系统文件，除非用户另有要求。
2. 先运行预览，展示目标根目录、按类别/月份的去向、冲突和未知扩展名。
3. 遇到未知扩展名时，询问用户归类；用 `--learn EXT=类别` 写入规则库，再重新预览。
4. 仅在用户确认预览后，以 `--apply` 执行。保留脚本输出的 JSON 报告。

默认目标结构为 `<destination>/<类别>/<YYYY-MM>/文件名`，因此既按类型又按修改月份归档。默认 destination 是来源目录下的 `已整理`；多个来源请始终传入单独的 `--destination`。

## 运行

```powershell
# 预览（默认）
python scripts/organize_files.py "$env:USERPROFILE\Downloads"

# 先给未知扩展名命名类别；规则写入目标目录
python scripts/organize_files.py "$env:USERPROFILE\Downloads" --learn ".sketch=设计源文件"

# 用户确认后才实际移动
python scripts/organize_files.py "$env:USERPROFILE\Downloads" --apply
```

读取 [references/category-rules.md](references/category-rules.md) 以调整内置类别或向用户解释分类。

## 重名规则

- 文件大小相同且修改时间相差不超过 2 秒：视为同一文件，跳过来源文件。
- 默认 `safe`：保留两者，并将来源文件另存为 `名称 (1).扩展名`。
- `skip`：保留现有目标文件并跳过来源文件。
- `newer-wins`：仅在来源更新时覆盖旧目标文件；这是不可逆的，只有用户明确要求时才可使用，并必须先预览。

不要把“相同大小”单独视为重复；文件内容的哈希校验仅在用户要求更严格去重时额外执行。绝不对目录本身、符号链接或脚本运行目录执行整理。
