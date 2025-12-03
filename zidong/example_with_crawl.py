#!/usr/bin/env python3
"""
完整示例：爬取参考资料后生成发布
"""
from config import config
from mcp_client import MCPClient
from content_crawler import ContentCrawler
from ai_generator import AIGenerator
from publisher import Publisher


def crawl_and_publish():
    """爬取参考资料并发布"""
    
    # 初始化
    mcp_client = MCPClient(config.mcp_server_url)
    crawler = ContentCrawler(mcp_client)
    ai_generator = AIGenerator(
        api_key=config.gemini_api_key,
        base_url=config.gemini_base_url,
        model=config.gemini_model
    )
    publisher = Publisher(mcp_client, config.image_folder, config.local_image_folder)
    
    # 1. 爬取参考资料
    keyword = "上海美食推荐"
    print(f"🔍 搜索关键词: {keyword}")
    reference_data = crawler.get_reference_materials(keyword, limit=10)
    
    # 2. 生成内容
    topic = "上海必吃美食清单"
    result = ai_generator.generate_from_references(topic, reference_data)
    
    # 3. 发布
    publisher.publish(
        title=result["title"],
        content=result["content"],
        tags=result.get("tags", []),
        image_count=3,
        auto_confirm=False
    )


if __name__ == "__main__":
    crawl_and_publish()
