#!/usr/bin/env python3
"""
测试单张图片发布 - 查看详细错误
"""
import requests
import json

def test_publish():
    """测试发布单张图片"""
    url = "http://127.0.0.1:18060/api/v1/publish"
    
    data = {
        "title": "测试发布",
        "content": "测试内容",
        "images": ["/app/images/th.jpg"],
        "tags": ["测试"]
    }
    
    print("="*60)
    print("🧪 测试发布")
    print("="*60)
    print(f"\n📤 发送数据:")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    
    try:
        print(f"\n🔗 请求 URL: {url}")
        response = requests.post(url, json=data, timeout=300)
        
        print(f"\n📊 响应状态码: {response.status_code}")
        print(f"📄 响应内容:")
        print(response.text)
        
        if response.status_code == 200:
            print("\n✅ 发布成功！")
        else:
            print(f"\n❌ 发布失败: {response.status_code}")
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")

if __name__ == "__main__":
    test_publish()
