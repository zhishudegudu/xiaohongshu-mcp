#!/usr/bin/env python3
"""
简单示例：快速测试发布功能
"""
import os

# 设置代理（如果需要访问 Gemini API）
# 如果你已经在系统环境变量中设置了代理，可以注释掉这两行
os.environ["http_proxy"] = "http://127.0.0.1:1080"
os.environ["https_proxy"] = "http://127.0.0.1:1080"

from config import config
from mcp_client import MCPClient
from ai_generator import AIGenerator
from publisher import Publisher


def simple_publish():
    """简单发布示例（不爬取参考资料）"""
    
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
        pixabay_api_key=config.pixabay_api_key
    )
    
    # 生成内容
    topic = "第一次用Python自动发小红书"
    result = ai_generator.generate_from_scratch(topic)
    
    # 发布
    publisher.publish(
        title=result["title"],
        content=result["content"],
        image_count=1,
        auto_confirm=False  # 需要手动确认
    )


if __name__ == "__main__":
    simple_publish()
