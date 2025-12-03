"""
图片下载器 - 从 Unsplash 等免费图库下载图片
"""
import os
import requests
from typing import List, Optional
import random


class ImageDownloader:
    """图片下载器"""
    
    def __init__(self, save_folder: str):
        """
        初始化下载器
        
        Args:
            save_folder: 图片保存文件夹（本地路径）
        """
        self.save_folder = save_folder
        
        # 创建保存文件夹
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
    
    def download_from_unsplash(
        self, 
        keywords: List[str], 
        count: int = 3,
        orientation: str = "portrait"
    ) -> List[str]:
        """
        从 Unsplash 下载图片
        
        Args:
            keywords: 搜索关键词列表
            count: 下载数量
            orientation: 图片方向 (portrait/landscape/squarish)
        
        Returns:
            下载的图片文件名列表
        """
        downloaded_files = []
        
        print(f"\n📥 从 Unsplash 下载图片...")
        print(f"   关键词: {', '.join(keywords)}")
        print(f"   数量: {count} 张")
        
        for i, keyword in enumerate(keywords[:count]):
            try:
                # Unsplash Source API (无需 API Key)
                # 随机获取相关图片
                url = f"https://source.unsplash.com/800x600/?{keyword}"
                
                print(f"   [{i+1}/{count}] 下载: {keyword}...", end=" ")
                
                # 下载图片
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                # 保存图片
                filename = f"auto_{keyword}_{random.randint(1000, 9999)}.jpg"
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
            keywords: 搜索关键词（如果为 None 则下载随机图片）
            count: 下载数量
        
        Returns:
            下载的图片文件名列表
        """
        if keywords and len(keywords) > 0:
            # 使用关键词从 Unsplash 下载
            files = self.download_from_unsplash(keywords, count)
            
            # 如果下载失败，使用随机图片
            if not files:
                print("\n⚠️ Unsplash 下载失败，尝试使用随机图片...")
                files = self.download_from_picsum(count)
        else:
            # 直接下载随机图片
            files = self.download_from_picsum(count)
        
        return files


if __name__ == "__main__":
    # 测试
    downloader = ImageDownloader(r"E:\docker-xiaohongshu\images")
    
    # 测试 1: 使用关键词下载
    print("="*60)
    print("测试 1: 使用关键词下载")
    print("="*60)
    files = downloader.download_from_unsplash(["coffee", "food", "dessert"], count=3)
    print(f"\n下载的文件: {files}")
    
    # 测试 2: 下载随机图片
    print("\n" + "="*60)
    print("测试 2: 下载随机图片")
    print("="*60)
    files = downloader.download_from_picsum(count=2)
    print(f"\n下载的文件: {files}")
