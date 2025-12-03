"""
MCP客户端封装 - 与小红书MCP服务器交互
"""
import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class FeedItem:
    """Feed数据结构"""
    feed_id: str
    title: str
    content: str
    tags: List[str]
    author: str
    likes: int
    xsec_token: str


class MCPClient:
    """小红书MCP客户端 - 使用 REST API"""
    
    def __init__(self, server_url: str):
        # 将 /mcp 端点转换为 /api/v1 端点
        if server_url.endswith("/mcp"):
            self.base_url = server_url.replace("/mcp", "/api/v1")
        else:
            self.base_url = server_url.rstrip("/") + "/api/v1"
        
        print(f"🔗 使用 REST API: {self.base_url}")
    
    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """GET 请求"""
        url = f"{self.base_url}{endpoint}"
        try:
            # 禁用代理（MCP 服务器在本地）
            proxies = {"http": None, "https": None}
            response = requests.get(url, params=params, timeout=30, proxies=proxies)
            response.raise_for_status()
            result = response.json()
            # API 返回格式: {"success": true, "data": {...}}
            # 自动解包 data 字段
            if isinstance(result, dict) and "data" in result:
                return result["data"]
            return result
        except requests.exceptions.RequestException as e:
            raise Exception(f"API 请求失败: {e}")
    
    def _post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """POST 请求"""
        url = f"{self.base_url}{endpoint}"
        try:
            # 发布请求可能需要更长时间（上传图片等），设置更长的超时
            timeout = 180 if endpoint == "/publish" else 60
            # 禁用代理（MCP 服务器在本地）
            proxies = {"http": None, "https": None}
            response = requests.post(url, json=data, timeout=timeout, proxies=proxies)
            response.raise_for_status()
            result = response.json()
            # API 返回格式: {"success": true, "data": {...}}
            # 自动解包 data 字段
            if isinstance(result, dict) and "data" in result:
                return result["data"]
            return result
        except requests.exceptions.RequestException as e:
            raise Exception(f"API 请求失败: {e}")
    
    def check_login_status(self) -> bool:
        """检查登录状态"""
        result = self._get("/login/status")
        # REST API 返回格式: {"is_logged_in": true, "username": "xxx"}
        return result.get("is_logged_in", False)
    
    def search_feeds(self, keyword: str, limit: int = 10) -> List[FeedItem]:
        """搜索Feed内容"""
        print(f"🔍 搜索关键词: {keyword}")
        
        data = self._post("/feeds/search", {
            "keyword": keyword,
            "filters": {
                "sort_by": "综合",
                "note_type": "不限"
            }
        })
        
        feeds = []
        items = data.get("items", [])[:limit]
        
        for item in items:
            note_card = item.get("note_card", {})
            interact_info = note_card.get("interact_info", {})
            
            feed = FeedItem(
                feed_id=note_card.get("note_id", ""),
                title=note_card.get("display_title", ""),
                content=note_card.get("desc", ""),
                tags=note_card.get("tag_list", []),
                author=note_card.get("user", {}).get("nickname", ""),
                likes=int(interact_info.get("liked_count", "0")),
                xsec_token=item.get("xsec_token", "")
            )
            feeds.append(feed)
        
        print(f"✅ 找到 {len(feeds)} 条内容")
        return feeds
    
    def get_feed_detail(self, feed_id: str, xsec_token: str) -> Dict[str, Any]:
        """获取Feed详情"""
        return self._post("/feeds/detail", {
            "feed_id": feed_id,
            "xsec_token": xsec_token
        })
    
    def publish_content(self, title: str, content: str, images: List[str], tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """发布内容"""
        print(f"🚀 发布内容: {title}")
        print(f"📤 正在上传 {len(images)} 张图片，请稍候...")
        print(f"⏳ 这可能需要 1-3 分钟，请耐心等待...")
        
        data = {
            "title": title,
            "content": content,
            "images": images
        }
        
        if tags:
            data["tags"] = tags
        
        result = self._post("/publish", data)
        
        # REST API 返回格式可能不同，检查多种可能的成功标志
        if result.get("success") or "成功" in str(result):
            print("✅ 发布成功!")
        else:
            print(f"⚠️ 发布结果: {result}")
        
        return result
