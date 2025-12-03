"""
配置模板 - 复制此文件为 config_custom.py 并修改
"""
import os
import platform
from dataclasses import dataclass


def get_default_image_folder() -> str:
    """
    返回图片文件夹路径（MCP 服务器可访问的路径）
    
    Docker 模式（默认）：
    - 使用容器内路径：/app/images
    - 对应宿主机目录：E:/docker-xiaohongshu/images/
    
    本地模式：
    - 设置环境变量：USE_DOCKER=false
    - 使用本地路径
    """
    use_docker = os.getenv("USE_DOCKER", "true").lower() == "true"
    
    if use_docker:
        # Docker 模式（默认）
        return "/app/images"
    else:
        # 本地模式
        if platform.system() == "Windows":
            return r"C:\Users\wu\Pictures\xiaohongshu"
        else:
            return "/home/wu/images"


@dataclass
class Config:
    """全局配置"""
    
    # ==================== 必须修改的配置 ====================
    
    # 1. Gemini API Key
    # 从这里获取: https://aistudio.google.com/app/apikey
    gemini_api_key: str = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXX"  # ← 改成你的真实 API Key
    
    # 2. MCP 服务器地址
    # 如果 Python 和 MCP 在同一台 Windows 机器上运行:
    mcp_server_url: str = "http://127.0.0.1:18060/mcp"
    
    # 如果 MCP 在其他机器或 WSL 中运行，取消下面的注释并修改:
    # mcp_server_url: str = "http://192.168.21.59:18060/mcp"
    
    # 3. 图片文件夹路径
    # Docker 模式（默认）：
    image_folder: str = get_default_image_folder()  # 容器内路径：/app/images
    local_image_folder: str = r"E:\docker-xiaohongshu\images"  # 宿主机路径（用于选择图片）
    
    # 本地模式（设置 USE_DOCKER=false）：
    # image_folder: str = r"C:\Users\wu\Pictures\xiaohongshu"
    # local_image_folder: str = r"C:\Users\wu\Pictures\xiaohongshu"
    
    # ==================== 可选配置 ====================
    
    # Gemini 配置
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    gemini_model: str = "gemini-1.5-pro"  # 或 "gemini-1.5-flash" (更快但质量稍低)
    
    # 爬取配置
    crawl_keyword: str = "美食推荐"  # 默认搜索关键词
    crawl_limit: int = 10  # 每次爬取的参考内容数量
    
    # 发布配置
    auto_publish: bool = False  # 是否自动发布（不需要确认）
    # 建议先设为 False，测试稳定后再改为 True
    
    @classmethod
    def from_env(cls) -> "Config":
        """从环境变量加载配置（优先级更高）"""
        return cls(
            gemini_api_key=os.getenv("GEMINI_API_KEY", cls.gemini_api_key),
            mcp_server_url=os.getenv("MCP_SERVER_URL", cls.mcp_server_url),
            image_folder=os.getenv("IMAGE_FOLDER", cls.image_folder),
        )


# 全局配置实例
config = Config.from_env()


# ==================== 配置检查 ====================
def check_config():
    """检查配置是否正确"""
    issues = []
    
    # 检查 API Key
    if config.gemini_api_key == "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXX":
        issues.append("❌ Gemini API Key 未配置")
    
    # 检查本地图片文件夹
    if not os.path.exists(config.local_image_folder):
        issues.append(f"❌ 本地图片文件夹不存在: {config.local_image_folder}")
    
    # 检查图片
    if os.path.exists(config.local_image_folder):
        files = [f for f in os.listdir(config.local_image_folder) 
                if f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))]
        if not files:
            issues.append(f"❌ 图片文件夹中没有图片: {config.local_image_folder}")
    
    if issues:
        print("⚠️ 配置检查发现问题:")
        for issue in issues:
            print(f"   {issue}")
        return False
    else:
        print("✅ 配置检查通过")
        return True


if __name__ == "__main__":
    print("="*60)
    print("配置信息:")
    print("="*60)
    print(f"Gemini API Key: {'已配置' if config.gemini_api_key != 'AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXX' else '❌ 未配置'}")
    print(f"MCP 服务器: {config.mcp_server_url}")
    print(f"MCP 服务器路径: {config.image_folder}")
    print(f"本地图片文件夹: {config.local_image_folder}")
    print(f"爬取数量: {config.crawl_limit}")
    print(f"自动发布: {config.auto_publish}")
    print("="*60)
    check_config()
