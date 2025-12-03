#!/usr/bin/env python3
"""
快速启动脚本 - 一键检查配置并运行
"""
import sys
import os


def main():
    print("="*70)
    print("🚀 小红书自动发布工具 - 快速启动")
    print("="*70)
    
    # 1. 检查配置
    print("\n📋 步骤 1/4: 检查配置...")
    try:
        from config import config
        
        # 检查 API Key
        if config.gemini_api_key == "AIzaSy...":
            print("❌ 错误: Gemini API Key 未配置")
            print("💡 请修改 config.py 第 25 行，填入你的 API Key")
            print("   获取地址: https://aistudio.google.com/app/apikey")
            return
        
        # 检查本地图片文件夹
        if not os.path.exists(config.local_image_folder):
            print(f"❌ 错误: 本地图片文件夹不存在: {config.local_image_folder}")
            print(f"💡 请创建文件夹并放入图片")
            print(f"   Docker 模式: 图片应放在 {config.local_image_folder}")
            return
        
        # 检查图片
        files = [f for f in os.listdir(config.local_image_folder) 
                if f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))]
        if not files:
            print(f"❌ 错误: 图片文件夹中没有图片")
            print(f"💡 请在 {config.local_image_folder} 中放入至少 1 张图片")
            return
        
        print(f"✅ 配置检查通过")
        print(f"   - API Key: 已配置")
        print(f"   - 本地图片文件夹: {config.local_image_folder}")
        print(f"   - MCP 服务器路径: {config.image_folder}")
        print(f"   - 图片数量: {len(files)} 张")
        
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return
    
    # 2. 检查依赖
    print("\n📦 步骤 2/4: 检查依赖...")
    try:
        import openai
        import requests
        print("✅ 依赖包已安装")
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("💡 请运行: pip install -r requirements.txt")
        return
    
    # 3. 测试 MCP 连接
    print("\n🔌 步骤 3/4: 测试 MCP 连接...")
    try:
        from mcp_client import MCPClient
        
        client = MCPClient(config.mcp_server_url)
        is_logged_in = client.check_login_status()
        
        print(f"✅ MCP 连接成功")
        print(f"   - 服务器: {config.mcp_server_url}")
        print(f"   - 登录状态: {'✅ 已登录' if is_logged_in else '❌ 未登录'}")
        
        if not is_logged_in:
            print("\n⚠️ 警告: 未登录小红书")
            print("💡 请先使用 MCP 客户端扫码登录")
            print("   可以使用 Claude Desktop 或 MCP Inspector")
            
            choice = input("\n是否继续运行？(y/n): ").strip().lower()
            if choice != 'y':
                print("已取消")
                return
    
    except Exception as e:
        print(f"❌ MCP 连接失败: {e}")
        print(f"\n💡 请检查:")
        print(f"   1. MCP 服务器是否正在运行？")
        print(f"   2. 地址是否正确？{config.mcp_server_url}")
        print(f"   3. 防火墙是否阻止了连接？")
        
        choice = input("\n是否继续运行？(y/n): ").strip().lower()
        if choice != 'y':
            print("已取消")
            return
    
    # 4. 选择运行模式
    print("\n" + "="*70)
    print("🎯 步骤 4/4: 选择运行模式")
    print("="*70)
    print("1. 测试连接（推荐首次运行）")
    print("2. 简单示例（不爬取参考资料）")
    print("3. 完整示例（爬取参考资料）")
    print("4. 自动配图示例（AI 生成内容 + 自动下载配图）✨")
    print("5. 主程序（交互式）")
    print("="*70)
    
    choice = input("请选择 (1-5，默认 1): ").strip() or "1"
    
    print("\n" + "="*70)
    
    if choice == "1":
        print("运行测试连接...")
        print("="*70 + "\n")
        import test_connection
        test_connection.test_environment()
    
    elif choice == "2":
        print("运行简单示例...")
        print("="*70 + "\n")
        import example_simple
        example_simple.simple_publish()
    
    elif choice == "3":
        print("运行完整示例...")
        print("="*70 + "\n")
        import example_with_crawl
        example_with_crawl.crawl_and_publish()
    
    elif choice == "4":
        print("运行自动配图示例...")
        print("="*70 + "\n")
        import example_auto_images
        example_auto_images.auto_image_publish()
    
    elif choice == "5":
        print("运行主程序...")
        print("="*70 + "\n")
        import main
        main.main()
    
    else:
        print("❌ 无效选择")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 程序错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
