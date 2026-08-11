# organize-local-files

一个用于整理本地目录中文件的脚本工具，按文件类别和修改月份归档，支持预览模式、安全冲突处理及用户扩展分类规则。

## 特性

- 仅整理指定来源目录下的直接文件，不递归处理子目录。
- 默认预览模式，不会移动、覆盖或删除任何文件。
- 按文件类型和 `YYYY-MM` 修改时间分组到目标目录。默认目标目录为 `SOURCE/已整理`。
- 支持未知扩展名学习分类，并将规则保存在目标目录下的 `.organize-local-files-rules.json`。
- 支持三种冲突处理策略：`safe`、`skip`、`newer-wins`。

## 使用方法

```powershell
# 预览整理计划（默认）
python scripts/organize_files.py "$env:USERPROFILE\Downloads"

# 给未知扩展名指定类别并保存规则
python scripts/organize_files.py "$env:USERPROFILE\Downloads" --learn ".sketch=设计源文件"

# 在确认预览后实际移动文件
python scripts/organize_files.py "$env:USERPROFILE\Downloads" --apply
```

## 参数说明

- `source`：要整理的文件夹路径。
- `--destination`：目标归档根目录，默认是 `SOURCE/已整理`。
- `--apply`：实际移动文件；不加此参数仅生成预览报告。
- `--collision-policy`：冲突处理策略，可选值：`safe`（默认）、`skip`、`newer-wins`。
- `--learn .EXT=CATEGORY`：为扩展名指定类别并持久化规则。
- `--report PATH`：将 JSON 格式结果写入指定路径。

## 冲突规则

- 文件大小相同且修改时间相差不超过 2 秒：视为同一文件，跳过来源文件。
- `safe`：保留两者，并将来源文件另存为 `名称 (1).扩展名`。
- `skip`：保留目标文件并跳过来源文件。
- `newer-wins`：仅在来源文件更新时覆盖目标文件。

## 默认分类规则

默认使用扩展名分类，未列出的扩展名归入 `其他`，并在预览报告中列出。

具体默认类别可参考：
- `文档`
- `表格`
- `演示文稿`
- `图片`
- `音频`
- `视频`
- `压缩包`
- `代码`
- `安装包`

## 参考规则文件

请查看 `references/category-rules.md` 了解默认分类规则和扩展名对应关系。

## 注意事项

- 脚本只处理直接文件，不处理子目录、符号链接或目录本身。
- `--apply` 前应始终先运行预览，确认整理计划。
- `newer-wins` 是不可逆覆盖行为，只有在明确要求时才使用。
