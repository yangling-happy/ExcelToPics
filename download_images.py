import pandas as pd
import requests
import os
import re
from typing import Optional, Dict, Tuple

class ImageDownloader:
    def __init__(self, excel_path: str, save_dir: str):
        """
        初始化图片下载器
        
        Args:
            excel_path: Excel文件路径
            save_dir: 保存图片的目录
        """
        self.excel_path = excel_path
        self.save_dir = save_dir
        self.df = None
        
        # 创建保存目录
        os.makedirs(self.save_dir, exist_ok=True)
        
    def load_excel(self):
        """加载Excel文件"""
        try:
            self.df = pd.read_excel(self.excel_path)
            print(f"成功加载Excel文件，共 {len(self.df)} 条记录")
            return True
        except Exception as e:
            print(f"加载Excel文件失败: {e}")
            return False
    
    def find_columns(self) -> Tuple[Optional[str], Optional[str]]:
        """自动识别姓名列和URL列"""
        name_col = None
        url_col = None
        
        # 常见的姓名列名模式
        name_patterns = ['姓名', 'name', 'Name', '用户', '用户姓名']
        # 常见的URL列名模式
        url_patterns = ['图片', '照片', 'image', 'Image', 'url', 'URL', '链接']
        
        for col in self.df.columns:
            col_str = str(col)
            # 查找姓名列
            if not name_col:
                for pattern in name_patterns:
                    if pattern in col_str:
                        name_col = col
                        break
            
            # 查找URL列
            if not url_col:
                for pattern in url_patterns:
                    if pattern in col_str:
                        url_col = col
                        break
        
        # 如果没找到，使用前两列尝试
        if not name_col and len(self.df.columns) > 0:
            name_col = self.df.columns[0]
        
        if not url_col and len(self.df.columns) > 1:
            url_col = self.df.columns[1]
        
        return name_col, url_col
    
    def sanitize_filename(self, filename: str) -> str:
        """清理文件名，移除非法字符"""
        # 移除Windows文件名中不允许的字符
        illegal_chars = r'[<>:"/\\|?*\x00-\x1f]'
        filename = re.sub(illegal_chars, '_', filename)
        
        # 限制文件名长度
        if len(filename) > 200:
            name_part = filename[:100]
            ext_part = os.path.splitext(filename)[1]
            filename = name_part + ext_part
        
        return filename.strip()
    
    def get_file_extension(self, url: str) -> str:
        """从URL获取文件扩展名"""
        # 常见图片/视频扩展名
        extensions = {
            '.jpg': ['.jpg', '.jpeg', '.JPG', '.JPEG'],
            '.png': ['.png', '.PNG'],
            '.gif': ['.gif', '.GIF'],
            '.mp4': ['.mp4', '.MP4'],
            '.webp': ['.webp', '.WEBP']
        }
        
        # 检查URL中是否包含特定扩展名
        url_lower = url.lower()
        for ext, patterns in extensions.items():
            for pattern in patterns:
                if pattern in url_lower:
                    return ext
        
        # 从URL路径中提取扩展名
        try:
            parsed_url = requests.utils.urlparse(url)
            path = parsed_url.path
            ext = os.path.splitext(path)[1]
            if ext and len(ext) <= 10:  # 合理的扩展名长度
                return ext.lower()
        except:
            pass
        
        # 默认返回.jpg
        return '.jpg'
    
    def download_images(self, name_col: str = None, url_col: str = None):
        """
        下载所有图片
        
        Args:
            name_col: 姓名列名（可选，自动检测）
            url_col: URL列名（可选，自动检测）
        """
        if self.df is None:
            if not self.load_excel():
                return
        
        # 自动检测列名
        if not name_col or not url_col:
            detected_name_col, detected_url_col = self.find_columns()
            name_col = name_col or detected_name_col
            url_col = url_col or detected_url_col
        
        if not name_col or not url_col:
            print("无法确定姓名列和URL列，请手动指定")
            print(f"可用列名: {list(self.df.columns)}")
            return
        
        print(f"使用姓名列: {name_col}")
        print(f"使用URL列: {url_col}")
        
        success_count = 0
        fail_count = 0
        skipped_count = 0
        
        for idx, row in self.df.iterrows():
            try:
                # 获取姓名
                name_value = row[name_col]
                if pd.isna(name_value):
                    name = f"未命名_{idx+1}"
                else:
                    name = str(name_value).strip()
                
                # 获取URL
                url = row[url_col]
                if pd.isna(url) or not isinstance(url, str) or not url.startswith('http'):
                    skipped_count += 1
                    continue
                
                print(f"[{idx+1}/{len(self.df)}] 处理: {name}")
                
                # 下载文件
                response = requests.get(url, timeout=30, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                
                if response.status_code == 200:
                    # 获取文件扩展名
                    ext = self.get_file_extension(url)
                    
                    # 生成安全的文件名
                    safe_name = self.sanitize_filename(name)
                    filename = f"{idx+1:03d}_{safe_name}{ext}"
                    filepath = os.path.join(self.save_dir, filename)
                    
                    # 保存文件
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    success_count += 1
                    print(f"  ✓ 保存为: {filename}")
                else:
                    print(f"  ✗ HTTP错误: {response.status_code}")
                    fail_count += 1
                    
            except requests.exceptions.Timeout:
                print(f"  ✗ 下载超时")
                fail_count += 1
            except Exception as e:
                print(f"  ✗ 错误: {str(e)[:100]}")
                fail_count += 1
        
        # 生成统计报告
        self._generate_report(success_count, fail_count, skipped_count)
    
    def _generate_report(self, success: int, fail: int, skipped: int):
        """生成下载报告"""
        print("\n" + "="*50)
        print("下载完成！")
        print("="*50)
        print(f"总记录数: {len(self.df)}")
        print(f"成功下载: {success}")
        print(f"下载失败: {fail}")
        print(f"跳过记录: {skipped}")
        print(f"文件保存到: {os.path.abspath(self.save_dir)}")
        print("="*50)


def main():
    """主函数"""
    # 配置文件路径
    EXCEL_FILE = "data.xlsx"  # 替换为你的Excel文件名
    SAVE_DIR = "downloaded_images"
    
    # 创建下载器实例
    downloader = ImageDownloader(EXCEL_FILE, SAVE_DIR)
    
    # 下载图片
    downloader.download_images()
    
    # 如果需要手动指定列名，可以使用：
    # downloader.download_images(name_col='姓名', url_col='图片链接')


if __name__ == "__main__":
    main()
