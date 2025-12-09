"""
图片下载器 - 从免费图库下载图片

注意：由于免费图片 API 限制，建议手动准备图片。
或者注册自己的 API Key：
- Pixabay: https://pixabay.com/api/docs/
- Pexels: https://www.pexels.com/api/
"""
import os
import requests
from typing import List, Optional
import random
import time


class ImageDownloader:
    """图片下载器"""
    
    def __init__(self, save_folder: str, pixabay_api_key: str = None):
        """
        初始化下载器
        
        Args:
            save_folder: 图片保存文件夹（本地路径）
            pixabay_api_key: Pixabay API Key（可选）
        """
        self.save_folder = save_folder
        self.pixabay_api_key = pixabay_api_key
        
        # 创建保存文件夹
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
    
    def download_from_pixabay(
        self, 
        keywords: List[str], 
        count: int = 3
    ) -> List[str]:
        """
        从 Pixabay 下载图片（完全免费）
        
        Args:
            keywords: 搜索关键词列表
            count: 下载数量
        
        Returns:
            下载的图片文件名列表
        """
        downloaded_files = []
        
        print(f"\n📥 从 Pixabay 下载图片...")
        print(f"   关键词: {', '.join(keywords)}")
        print(f"   数量: {count} 张")
        
        # Pixabay API Key
        # 从配置读取，如果没有则使用默认的（可能失效）
        api_key = self.pixabay_api_key or "45599090-5e6a4c5e8b8e4c5e8b8e4c5e"
        
        if not self.pixabay_api_key:
            print("   ⚠️ 未配置 Pixabay API Key，使用默认 Key（可能失效）")
            print("   💡 建议：在 https://pixabay.com/api/docs/ 注册获取自己的 API Key")
        
        for i, keyword in enumerate(keywords[:count]):
            try:
                # Pixabay API 搜索
                search_url = "https://pixabay.com/api/"
                params = {
                    "key": api_key,
                    "q": keyword,
                    "image_type": "photo",
                    "per_page": 3,
                    "page": random.randint(1, 5)
                }
                
                print(f"   [{i+1}/{count}] 搜索: {keyword}...", end=" ")
                
                # 搜索图片
                response = requests.get(search_url, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                hits = data.get("hits", [])
                
                if not hits:
                    print(f"❌ 未找到相关图片")
                    continue
                
                # 随机选择一张图片
                hit = random.choice(hits)
                image_url = hit["largeImageURL"]  # 或 "webformatURL"
                
                print(f"下载中...", end=" ")
                
                # 下载图片
                img_response = requests.get(image_url, timeout=30)
                img_response.raise_for_status()
                
                # 保存图片
                # 清理关键词作为文件名（移除空格和特殊字符）
                clean_keyword = keyword.replace(" ", "_").replace("/", "_")[:20]
                filename = f"auto_{clean_keyword}_{random.randint(1000, 9999)}.jpg"
                filepath = os.path.join(self.save_folder, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(img_response.content)
                
                downloaded_files.append(filename)
                print("✅")
                
                # 避免请求过快
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ {str(e)[:50]}")
                continue
        
        if downloaded_files:
            print(f"\n✅ 成功下载 {len(downloaded_files)} 张图片")
        else:
            print(f"\n⚠️ 未能下载任何图片")
        
        return downloaded_files
    
    def download_from_picsum(self, count: int = 3) -> List[str]:
        """
        从 Lorem Picsum 下载随机图片（备用方案）
        
        Args:
            count: 下载数量
        
        Returns:
            下载的图片文件名列表
        """
        downloaded_files = []
        
        print(f"\n📥 从 Lorem Picsum 下载随机图片...")
        print(f"   数量: {count} 张")
        
        for i in range(count):
            try:
                # Lorem Picsum API (无需 API Key)
                url = f"https://picsum.photos/800/600?random={random.randint(1, 10000)}"
                
                print(f"   [{i+1}/{count}] 下载随机图片...", end=" ")
                
                # 下载图片
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                # 保存图片
                filename = f"auto_random_{random.randint(1000, 9999)}.jpg"
                filepath = os.path.join(self.save_folder, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                downloaded_files.append(filename)
                print("✅")
                
            except Exception as e:
                print(f"❌ {e}")
                continue
        
        if downloaded_files:
            print(f"\n✅ 成功下载 {len(downloaded_files)} 张图片")
        else:
            print(f"\n⚠️ 未能下载任何图片")
        
        return downloaded_files
    
    def download_images(
        self, 
        keywords: Optional[List[str]] = None, 
        count: int = 3
    ) -> List[str]:
        """
        智能下载图片
        
        Args:
            keywords: 搜索关键词（如果为 None 则返回空列表）
            count: 下载数量
        
        Returns:
            下载的图片文件名列表
        """
        if keywords and len(keywords) > 0:
            # 使用关键词从 Pixabay 下载
            files = self.download_from_pixabay(keywords, count)
            
            # 如果下载失败，不使用随机图片，而是返回空列表
            # 让调用者决定是否使用本地图片
            if not files:
                print("\n⚠️ 图片下载失败")
                print("💡 建议：使用本地图片或稍后重试")
        else:
            # 没有关键词，返回空列表
            print("\n⚠️ 未提供搜索关键词")
            files = []
        
        return files


if __name__ == "__main__":
    # 测试
    downloader = ImageDownloader(r"E:\docker-xiaohongshu\images")
    
    # 测试: 使用关键词下载
    print("="*60)
    print("测试: 从 Pixabay 下载图片")
    print("="*60)
    files = downloader.download_from_pixabay(["coffee", "cafe", "latte"], count=3)
    print(f"\n下载的文件: {files}")
