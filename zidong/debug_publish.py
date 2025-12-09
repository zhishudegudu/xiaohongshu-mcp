#!/usr/bin/env python3
"""
调试发布问题
"""
import requests
import json

# 测试数据 - 使用之前成功的图片
data = {
    "title": "测试标题",
    "content": "测试内容",
    "images": ["/app/images/auto_random_3475.jpg"],
    "tags": []
}

print("="*60)
print("🔍 调试发布请求")
print("="*60)
print(f"\n📤 请求数据:")
print(json.dumps(data, indent=2, ensure_ascii=False))

# 发送请求
url = "http://127.0.0.1:18060/api/v1/publish"
print(f"\n🌐 请求 URL: {url}")

try:
    response = requests.post(
        url,
        json=data,
        timeout=180,
        proxies={"http": None, "https": None}
    )
    
    print(f"\n📊 响应状态码: {response.status_code}")
    print(f"📋 响应头:")
    for key, value in response.headers.items():
        print(f"   {key}: {value}")
    
    print(f"\n📄 响应内容:")
    try:
        result = response.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except:
        print(response.text)
    
    if response.status_code != 200:
        print(f"\n❌ 错误: HTTP {response.status_code}")
        response.raise_for_status()
    else:
        print(f"\n✅ 请求成功")
        
except Exception as e:
    print(f"\n💥 异常: {e}")
    import traceback
    traceback.print_exc()
