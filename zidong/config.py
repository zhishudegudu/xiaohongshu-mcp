"""
配置管理模块
"""
import os
import platform
from dataclasses import dataclass
from typing import Optional


# ================= 🔴 代理配置 =================
# 如果需要使用代理访问 Gemini API，取消下面两行的注释并修改端口
os.environ["http_proxy"] = "http://127.0.0.1:1080"
os.environ["https_proxy"] = "http://127.0.0.1:1080"
# 重要：本地地址不走代理，避免影响 MCP 服务器连接
# no_proxy 必须在设置代理之前或同时设置
os.environ["no_proxy"] = "localhost,127.0.0.1,::1,0.0.0.0"
os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1,0.0.0.0"  # 有些库用大写
# ===============================================


def is_docker_mode() -> bool:
    """
    智能检测是否为 Docker 模式
    
    检测逻辑：
    1. 如果设置了环境变量 USE_DOCKER，使用该值
    2. 否则，通过检测 MCP 服务器响应头判断
    3. 默认为 Docker 模式
    """
    # 1. 优先使用环境变量
    use_docker_env = os.getenv("USE_DOCKER", "").lower()
    if use_docker_env == "true":
        return True
    elif use_docker_env == "false":
        return False
    
    # 2. 自动检测：尝试连接 MCP 服务器并检查是否在容器中运行
    try:
        import requests
        response = requests.get(
            "http://127.0.0.1:18060/api/v1/health",
            timeout=2,
            proxies={"http": None, "https": None}
        )
        # 检查响应头中是否有 Docker 相关信息
        # 或者检查服务器返回的信息
        if response.status_code == 200:
            # 如果能连接到 18060 端口，很可能是 Docker 模式
            # 因为本地直接运行通常不会占用这个端口
            return True
    except:
        pass
    
    # 3. 默认为 Docker 模式（因为大多数情况下使用 Docker）
    return True


def get_default_image_folder() -> str:
    """
    返回图片文件夹路径（MCP 服务器可访问的路径）
    
    重要：这个路径是给 MCP 服务器使用的，不是 Python 本地路径！
    
    自动检测模式：
    - Docker 模式：使用容器内路径 /app/images
    - 本地模式：使用本地路径
    
    手动指定：设置环境变量 USE_DOCKER=true/false
    """
    if is_docker_mode():
        # Docker 模式：MCP 服务器在容器中
        return "/app/images"
    else:
        # 本地模式：MCP 服务器直接运行
        if platform.system() == "Windows":
            return r"E:\新建文件夹"
        else:
            return "/home/wu/images"


@dataclass
class Config:
    """全局配置"""
    
    # Gemini API配置
    # ⚠️ 重要：不要在代码中硬编码 API Key！请使用环境变量
    # 设置方法：$env:GEMINI_API_KEY="你的新API Key"
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "AIzaSyA53mDfUtrYYAD-FNhn2bGWGmgDFN_Tjts")
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    # 可用模型: gemini-2.5-flash (快速), gemini-2.5-pro (高质量), gemini-flash-latest
    gemini_model: str = "gemini-2.5-flash"
    
    # Gemini 代理配置（如果你的地区不支持 Gemini API）
    # 设置方法：$env:GEMINI_PROXY="http://127.0.0.1:7890"
    # 或者：$env:GEMINI_PROXY="socks5://127.0.0.1:7890"
    gemini_proxy: str = os.getenv("GEMINI_PROXY", "")
    
    # Pixabay API 配置（用于自动下载图片）
    # 注册地址：https://pixabay.com/api/docs/
    # 设置方法：$env:PIXABAY_API_KEY="你的API_Key"
    pixabay_api_key: str = os.getenv("PIXABAY_API_KEY", "53626706-ebfb74caeb7c442e4d6d40d9d")
    
    # MCP服务器配置
    # 如果在同一台机器上运行Python和MCP服务器，使用 localhost
    # 如果MCP服务器在其他机器上，使用该机器的IP地址
    # 默认使用 localhost，如果需要远程访问请修改为实际IP
    mcp_server_url: str = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:18060/mcp")
    
    # 图片配置
    image_folder: str = os.getenv("IMAGE_FOLDER", get_default_image_folder())
    # 本地图片文件夹（用于选择图片）
    # Docker 模式：宿主机上的图片目录
    # 本地模式：与 image_folder 相同
    local_image_folder: str = os.getenv("LOCAL_IMAGE_FOLDER", r"E:\docker-xiaohongshu\images")
    
    # 爬取配置
    crawl_keyword: str = "美食推荐"  # 默认搜索关键词
    crawl_limit: int = 10  # 爬取数量限制
    
    # 发布配置
    auto_publish: bool = False  # 是否自动发布（不需要确认）
    auto_download_images: bool = True  # 是否自动下载配图
    
    @classmethod
    def from_env(cls) -> "Config":
        """从环境变量加载配置"""
        return cls(
            gemini_api_key=os.getenv("GEMINI_API_KEY", cls.gemini_api_key),
            mcp_server_url=os.getenv("MCP_SERVER_URL", cls.mcp_server_url),
            image_folder=os.getenv("IMAGE_FOLDER", cls.image_folder),
        )


# 全局配置实例
config = Config.from_env()
