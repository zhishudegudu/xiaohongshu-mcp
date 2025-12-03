#!/usr/bin/env python3
"""
验证 Docker 容器路径配置
"""
import os
import config

def verify_config():
    """验证配置是否正确"""
    print("="*60)
    print("🔍 验证图片路径配置")
    print("="*60)
    
    # 检测运行模式
    use_docker_env = os.getenv("USE_DOCKER", "")
    is_docker = config.is_docker_mode()
    
    if use_docker_env:
        mode = f"{'Docker 容器模式' if is_docker else '本地模式'} (环境变量指定)"
    else:
        mode = f"{'Docker 容器模式' if is_docker else '本地模式'} (自动检测)"
    
    print(f"\n🎯 当前运行模式: {mode}")
    print("-" * 60)
    
    print("\n1️⃣ 当前配置:")
    print("-" * 60)
    print(f"USE_DOCKER 环境变量: {use_docker_env if use_docker_env else '未设置 (自动检测)'}")
    print(f"检测结果: {'Docker 模式' if is_docker else '本地模式'}")
    print(f"图片文件夹: {config.config.image_folder}")
    print(f"本地图片文件夹: {config.config.local_image_folder}")
    print(f"MCP 服务器: {config.config.mcp_server_url}")
    print(f"Gemini 模型: {config.config.gemini_model}")
    
    print("\n2️⃣ 路径说明:")
    print("-" * 60)
    if is_docker:
        print("✅ Docker 模式:")
        print("   - 宿主机目录: E:\\docker-xiaohongshu\\images\\")
        print("   - 容器内路径: /app/images/")
        print("   - Python 使用: /app/images/")
        print("\n💡 图片放到宿主机目录，代码自动使用容器路径")
    else:
        print("✅ 本地模式:")
        print("   - 图片目录: E:\\新建文件夹\\")
        print("   - Python 使用: E:\\新建文件夹\\")
        print("\n💡 直接使用本地路径，无需 Docker 映射")
    
    print("\n3️⃣ 使用示例:")
    print("-" * 60)
    print("# 自动使用配置的路径")
    print("publisher = Publisher(mcp_client, config.image_folder)")
    print()
    print("# 或手动指定容器内路径")
    print('images = ["/app/images/1.jpg", "/app/images/2.jpg"]')
    print("publisher.publish(title, content, tags, images=images)")
    
    print("\n4️⃣ 检测说明:")
    print("-" * 60)
    print("自动检测逻辑:")
    print("  1. 检查环境变量 USE_DOCKER")
    print("  2. 尝试连接 MCP 服务器 (http://127.0.0.1:18060)")
    print("  3. 默认为 Docker 模式")
    print()
    print("手动指定模式:")
    if is_docker:
        print("  切换到本地模式: $env:USE_DOCKER=\"false\"")
    else:
        print("  切换到 Docker 模式: $env:USE_DOCKER=\"true\"")
    
    print("\n" + "="*60)
    print(f"✅ 配置验证完成！当前模式: {mode}")
    print("="*60)

if __name__ == "__main__":
    verify_config()
