# 默认分类规则

脚本以扩展名（不区分大小写）分类。用户学习的规则优先于此表，并保存在目标目录的 `.organize-local-files-rules.json`。

| 类别 | 扩展名 |
| --- | --- |
| 文档 | `.pdf`, `.doc`, `.docx`, `.odt`, `.rtf`, `.txt`, `.md`, `.csv`, `.epub` |
| 表格 | `.xls`, `.xlsx`, `.xlsm`, `.ods` |
| 演示文稿 | `.ppt`, `.pptx`, `.odp`, `.key` |
| 图片 | `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.bmp`, `.tif`, `.tiff`, `.svg`, `.heic` |
| 音频 | `.mp3`, `.wav`, `.flac`, `.m4a`, `.aac`, `.ogg` |
| 视频 | `.mp4`, `.mov`, `.mkv`, `.avi`, `.wmv`, `.webm` |
| 压缩包 | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2`, `.xz` |
| 代码 | `.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.java`, `.c`, `.cpp`, `.cs`, `.go`, `.rs`, `.html`, `.css`, `.json`, `.yaml`, `.yml`, `.xml`, `.sql`, `.ipynb` |
| 安装包 | `.exe`, `.msi`, `.dmg`, `.pkg`, `.apk`, `.deb`, `.rpm` |

无扩展名或未列出的扩展名归入 `其他`，并在预览报告中列出。将用户指定的类别原样保存；不要擅自把可执行文件或隐私文件归为其他类别后自动删除。
