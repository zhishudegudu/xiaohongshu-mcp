"""
内容发布模块
"""
import os
import random
from typing import List, Optional
from mcp_client import MCPClient
from image_downloader import ImageDownloader


class Publisher:
    """内容发布器"""
    
    def __init__(self, mcp_client: MCPClient, image_folder: str, local_image_folder: str = None):
        """
        初始化发布器
        
        Args:
            mcp_client: MCP 客户端
            image_folder: MCP 服务器可访问的图片路径（如 Docker 容器内路径 /app/images）
            local_image_folder: 本地图片文件夹路径（用于选择图片），如果为 None 则使用 image_folder
        """
        self.mcp_client = mcp_client
        self.image_folder = image_folder  # 发送给 MCP 服务器的路径
        self.local_image_folder = local_image_folder or image_folder  # 本地选择图片的路径
        self.image_downloader = ImageDownloader(local_image_folder)  # 图片下载器
    
    def get_random_images(self, count: int = 1) -> List[str]:
        """
        随机选择图片
        
        Args:
            count: 需要的图片数量
        
        Returns:
            图片路径列表（MCP 服务器可访问的路径）
        """
        # 从本地文件夹选择图片
        if not os.path.exists(self.local_image_folder):
            raise Exception(f"错误：找不到本地图片文件夹 {self.local_image_folder}")
        
        files = [
            f for f in os.listdir(self.local_image_folder)
            if f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))
        ]
        
        if not files:
            raise Exception(f"错误：文件夹 {self.local_image_folder} 里没有图片！")
        
        # 随机选择指定数量的图片
        selected_count = min(count, len(files))
        selected_files = random.sample(files, selected_count)
        
        # 构建 MCP 服务器可访问的路径
        full_paths = [os.path.join(self.image_folder, f).replace("\\", "/") for f in selected_files]
        
        print(f"🖼️ 选中 {len(full_paths)} 张图片:")
        for path in full_paths:
            print(f"   - {path}")
        
        return full_paths
    
    def download_images_by_keywords(self, keywords: List[str], count: int = 3) -> List[str]:
        """
        根据关键词下载图片
        
        Args:
            keywords: 搜索关键词列表
            count: 下载数量
        
        Returns:
            图片路径列表（MCP 服务器可访问的路径）
        """
        # 下载图片到本地
        filenames = self.image_downloader.download_images(keywords, count)
        
        # 构建 MCP 服务器可访问的路径
        full_paths = [os.path.join(self.image_folder, f).replace("\\", "/") for f in filenames]
        
        return full_paths
    
    def publish(
        self,
        title: str,
        content: str,
        tags: Optional[List[str]] = None,
        images: Optional[List[str]] = None,
        image_count: int = 1,
        auto_confirm: bool = False
    ) -> bool:
        """
        发布内容
        
        Args:
            title: 标题
            content: 内容
            tags: 标签列表
            images: 图片路径列表（如果不提供则随机选择）
            image_count: 需要的图片数量（当images为None时使用）
            auto_confirm: 是否自动确认发布
        
        Returns:
            是否发布成功
        """
        # 如果没有提供图片，则随机选择
        if images is None:
            images = self.get_random_images(image_count)
        
        # 显示预览
        print("\n" + "="*50)
        print("📝 内容预览:")
        print(f"标题: {title}")
        print(f"内容: {content[:100]}...")
        if tags:
            print(f"标签: {', '.join(tags)}")
        print(f"图片数量: {len(images)}")
        print("="*50 + "\n")
        
        # 确认发布
        if not auto_confirm:
            confirm = input("⚠️ 按回车键确认发布，输入 'n' 取消: ")
            if confirm.lower() == 'n':
                print("❌ 已取消发布")
                return False
        
        # 执行发布
        try:
            self.mcp_client.publish_content(
                title=title,
                content=content,
                images=images,
                tags=tags
            )
            print("🎉 发布成功！")
            return True
        
        except Exception as e:
            print(f"❌ 发布失败: {e}")
            return False
