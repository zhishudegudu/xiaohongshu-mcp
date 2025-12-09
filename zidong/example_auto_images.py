#!/usr/bin/env python3
"""
自动配图示例：AI生成内容 + 自动下载配图 + 发布
"""
import os

# 设置代理（如果需要访问 Gemini API）
os.environ["http_proxy"] = "http://127.0.0.1:1080"
os.environ["https_proxy"] = "http://127.0.0.1:1080"

from config import config
from mcp_client import MCPClient
from ai_generator import AIGenerator
from publisher import Publisher


def auto_image_publish():
    """自动配图发布示例"""
    
    # 初始化
    mcp_client = MCPClient(config.mcp_server_url)
    ai_generator = AIGenerator(
        api_key=config.gemini_api_key,
        base_url=config.gemini_base_url,
        model=config.gemini_model,
        proxy=config.gemini_proxy
    )
    publisher = Publisher(
        mcp_client, 
        config.image_folder, 
        config.local_image_folder,
        pixabay_api_key=config.pixabay_api_key  # 传入 Pixabay API Key
    )
    
    # 1. 生成内容
    topic = "上海网红咖啡店探店"
    print(f"\n📝 主题: {topic}")
    result = ai_generator.generate_from_scratch(topic)
    
    title = result["title"]
    content = result["content"]
    
    # 2. 生成图片关键词
    keywords = ai_generator.generate_image_keywords(title, content, count=3)
    
    # 3. 自动下载配图（如果配置了 Pixabay API Key）
    if config.pixabay_api_key:
        print(f"\n📥 尝试自动下载配图...")
        images = publisher.download_images_by_keywords(keywords, count=3)
        
        if not images:
            print("\n⚠️ 图片下载失败，使用本地图片")
            images = publisher.get_random_images(count=3)
    else:
        # 没有配置 API Key，使用本地图片
        print(f"\n💡 建议的图片关键词: {', '.join(keywords)}")
        print(f"   （未配置 Pixabay API Key，使用本地图片）")
        print(f"\n📁 使用本地图片...")
        images = publisher.get_random_images(count=3)
    
    # 4. 发布
    publisher.publish(
        title=title,
        content=content,
        images=images,
        auto_confirm=False
    )


if __name__ == "__main__":
    auto_image_publish()
