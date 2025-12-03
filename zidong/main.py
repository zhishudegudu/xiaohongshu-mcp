#!/usr/bin/env python3
"""
小红书自动化发布工具 - 主程序

流程：爬取 -> 清洗 -> AI生成 -> 发布
"""
import sys
from config import config
from mcp_client import MCPClient
from content_crawler import ContentCrawler
from ai_generator import AIGenerator
from publisher import Publisher


def main():
    """主流程"""
    print("🚀 小红书自动化发布工具启动...")
    print("="*60)
    
    # 1. 初始化各个模块
    print("\n📦 初始化模块...")
    mcp_client = MCPClient(config.mcp_server_url)
    crawler = ContentCrawler(mcp_client)
    ai_generator = AIGenerator(
        api_key=config.gemini_api_key,
        base_url=config.gemini_base_url,
        model=config.gemini_model
    )
    publisher = Publisher(mcp_client, config.image_folder, config.local_image_folder)
    
    # 2. 检查登录状态
    print("\n🔐 检查登录状态...")
    try:
        is_logged_in = mcp_client.check_login_status()
        if not is_logged_in:
            print("❌ 未登录！请先使用 MCP 工具登录小红书")
            print("💡 提示：可以通过 Claude Desktop 或其他 MCP 客户端调用 get_login_qrcode 工具")
            return
        print("✅ 已登录")
    except Exception as e:
        print(f"⚠️ 无法检查登录状态: {e}")
        print("继续执行...")
    
    # 3. 选择模式
    print("\n" + "="*60)
    print("请选择生成模式:")
    print("1. 从零开始生成（不需要参考资料）")
    print("2. 基于参考资料生成（推荐）")
    print("="*60)
    
    mode = input("请输入模式编号 (1/2，默认2): ").strip() or "2"
    
    # 4. 获取主题
    default_topic = "第一次用Python自动发小红书是什么体验"
    topic = input(f"\n📝 请输入主题 (默认: {default_topic}): ").strip() or default_topic
    
    # 5. 生成内容
    try:
        if mode == "1":
            # 模式1：从零开始生成
            print(f"\n🎨 模式1: 从零开始生成内容...")
            result = ai_generator.generate_from_scratch(topic)
            tags = None  # 从零开始模式没有tags
        
        else:
            # 模式2：基于参考资料生成
            print(f"\n🎨 模式2: 基于参考资料生成内容...")
            
            # 获取搜索关键词
            keyword = input(f"🔍 请输入搜索关键词 (默认: {topic}): ").strip() or topic
            
            # 爬取参考资料
            print(f"\n📥 步骤1: 爬取参考资料...")
            reference_data = crawler.get_reference_materials(
                keyword=keyword,
                limit=config.crawl_limit
            )
            
            # 显示参考资料摘要
            print(f"\n📊 参考资料摘要:")
            print(f"   - 标题数量: {len(reference_data.get('titles', []))}")
            print(f"   - 内容数量: {len(reference_data.get('contents', []))}")
            print(f"   - 标签数量: {len(reference_data.get('tags', []))}")
            print(f"   - 总点赞数: {reference_data.get('total_likes', 0)}")
            
            # AI生成
            print(f"\n🤖 步骤2: AI生成内容...")
            result = ai_generator.generate_from_references(topic, reference_data)
            tags = result.get("tags", [])
        
        # 提取生成结果
        title = result.get("title", "")
        content = result.get("content", "")
        
        if not title or not content:
            print("❌ 生成失败：内容为空")
            return
        
        print(f"\n✅ 内容生成成功！")
        
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 6. 发布内容
    print(f"\n📤 步骤3: 发布内容...")
    try:
        success = publisher.publish(
            title=title,
            content=content,
            tags=tags,
            image_count=3,  # 使用3张图片
            auto_confirm=config.auto_publish
        )
        
        if success:
            print("\n" + "="*60)
            print("🎉 任务完成！内容已成功发布到小红书")
            print("="*60)
        else:
            print("\n任务已取消")
    
    except Exception as e:
        print(f"❌ 发布失败: {e}")
        import traceback
        traceback.print_exc()


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
