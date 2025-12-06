# 批量图片下载器
一个用于从Excel文件中批量下载图片的Python脚本。

## 功能特性
- 从Excel文件中读取图片URL
- 批量下载图片/视频文件
- 自动检测姓名和URL列
- 安全的文件名处理
- 下载统计报告
- 超时和重试机制

## 安装依赖
```bash
pip install -r requirements.txt
```

## 使用方法
### 基本使用
准备Excel文件（例如 data.xlsx），包含至少两列：
- 一列包含姓名/标识
- 一列包含图片URL

修改 download_images.py 中的配置：
```python
EXCEL_FILE = "your_data.xlsx"  # 你的Excel文件
SAVE_DIR = "downloaded_images"  # 保存目录
```

运行脚本：
```bash
python download_images.py
```

### 高级配置
如果需要手动指定列名，可以修改代码：
```python
# 方法1：在main()函数中修改
downloader.download_images(name_col='用户姓名', url_col='图片链接')

# 方法2：使用配置文件（config.py）
```

## Excel文件格式要求
建议的Excel格式：

| 序号 | 姓名 | 学号 | 图片链接 |
|------|------|------|----------|
| 1    | 张三 | 001 | https://example.com/image1.jpg |
| 2    | 李四 | 002 | https://example.com/image2.jpg |

注意：URL必须以 http:// 或 https:// 开头。

## 支持的文件格式
- 图片：JPG/JPEG、PNG、GIF、WebP
- 视频：MP4

## 输出文件命名
下载的文件将按以下格式命名：
```
001_张三.jpg
002_李四.png
003_王五.mp4
```

## 常见问题
1. 列名检测失败
   如果自动检测失败，请手动指定列名：
   ```python
   downloader.download_images(name_col='你的姓名列', url_col='你的URL列')
   ```

2. 下载速度慢
   可以调整 DOWNLOAD_CONFIG 中的 delay_between_requests 参数。

3. 网络错误
   检查网络连接，或调整超时时间。

## 隐私说明
- 本工具仅处理公开可访问的URL
- 不会收集或上传任何个人信息
- 请确保您有权下载和使用这些图片

## 许可证
MIT License

## 贡献
欢迎提交Issue和Pull Request！

---

## .gitignore 文件
```gitignore
# 数据文件（不上传实际数据）
data.xlsx
*.xlsx
*.csv

# 下载的图片
downloaded_images/
images/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 系统文件
.DS_Store
Thumbs.db

# 日志
*.log
```

## 使用示例
```python
# example_usage.py
"""
使用示例
"""

from download_images import ImageDownloader

# 简单示例
downloader = ImageDownloader("示例数据.xlsx", "下载的图片")
downloader.download_images()

# 指定列名示例
# downloader.download_images(name_col='用户姓名', url_col='照片链接')
```

### 快速上手步骤
1. 创建项目文件夹
2. 将上述文件放入文件夹
3. 将你的Excel文件重命名为 data.xlsx 或修改配置
4. 运行 python download_images.py
