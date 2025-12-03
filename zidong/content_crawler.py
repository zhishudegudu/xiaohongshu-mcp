"""
内容爬取和清洗模块
"""
from typing import List, Dict, Any
from mcp_client import MCPClient, FeedItem


class ContentCrawler:
    """内容爬取器"""
    
    def __init__(self, mcp_client: MCPClient):
        self.mcp_client = mcp_client
    
    def crawl_reference_content(self, keyword: str, limit: int = 10) -> List[FeedItem]:
        """
        爬取参考内容
        
        Args:
            keyword: 搜索关键词
            limit: 爬取数量限制
        
        Returns:
            Feed列表
        """
        feeds = self.mcp_client.search_feeds(keyword, limit)
        return feeds
    
    def clean_and_extract(self, feeds: List[FeedItem]) -> Dict[str, Any]:
        """
        清洗和提取数据
        
        Args:
            feeds: Feed列表
        
        Returns:
            清洗后的数据字典
        """
        print(f"🧹 清洗 {len(feeds)} 条数据...")
        
        cleaned_data = {
            "titles": [],
            "contents": [],
            "tags": set(),
            "total_likes": 0,
            "top_content": None
        }
        
        max_likes = 0
        
        for feed in feeds:
            # 提取标题
            if feed.title:
                cleaned_data["titles"].append(feed.title)
            
            # 提取内容
            if feed.content:
                cleaned_data["contents"].append(feed.content)
            
            # 提取标签
            if feed.tags:
                for tag in feed.tags:
                    if isinstance(tag, dict):
                        cleaned_data["tags"].add(tag.get("name", ""))
                    else:
                        cleaned_data["tags"].add(str(tag))
            
            # 统计点赞
            cleaned_data["total_likes"] += feed.likes
            
            # 找出最受欢迎的内容
            if feed.likes > max_likes:
                max_likes = feed.likes
                cleaned_data["top_content"] = {
                    "title": feed.title,
                    "content": feed.content,
                    "likes": feed.likes
                }
        
        # 转换tags为列表
        cleaned_data["tags"] = list(cleaned_data["tags"])[:10]  # 最多保留10个标签
        
        print(f"✅ 清洗完成: {len(cleaned_data['titles'])} 个标题, {len(cleaned_data['tags'])} 个标签")
        
        return cleaned_data
    
    def get_reference_materials(self, keyword: str, limit: int = 10) -> Dict[str, Any]:
        """
        一站式获取参考资料（爬取+清洗）
        
        Args:
            keyword: 搜索关键词
            limit: 爬取数量
        
        Returns:
            清洗后的参考资料
        """
        feeds = self.crawl_reference_content(keyword, limit)
        return self.clean_and_extract(feeds)
