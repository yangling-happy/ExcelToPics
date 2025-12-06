# 配置文件 - 请根据实际情况修改

# Excel文件路径
EXCEL_FILE = "data.xlsx"

# 保存目录
SAVE_DIR = "downloaded_images"

# 列名配置（如果自动检测失败，请手动指定）
COLUMN_CONFIG = {
    'name_column': '姓名',     # 姓名所在的列名
    'url_column': '图片链接'    # 图片URL所在的列名
}

# 下载设置
DOWNLOAD_CONFIG = {
    'timeout': 30,            # 下载超时时间（秒）
    'max_retries': 3,         # 最大重试次数
    'delay_between_requests': 0.5  # 请求间隔（秒），避免被封
