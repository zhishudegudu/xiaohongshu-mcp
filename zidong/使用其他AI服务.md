# 使用其他 AI 服务替代 Gemini

如果无法访问 Gemini API，可以使用以下替代方案：

## 方案 1: OpenAI GPT（推荐）

### 优点
- 全球可用，无地区限制
- API 稳定
- 效果好

### 配置

```python
# config.py
gemini_api_key = "sk-..."  # OpenAI API Key
gemini_base_url = "https://api.openai.com/v1/"
gemini_model = "gpt-4o-mini"  # 或 "gpt-4o", "gpt-3.5-turbo"
```

### 获取 API Key
https://platform.openai.com/api-keys

### 价格
- gpt-4o-mini: $0.15/1M tokens (便宜)
- gpt-4o: $2.50/1M tokens

## 方案 2: 国内 AI 服务

### 2.1 通义千问（阿里云）

```python
# 需要修改 ai_generator.py 适配 DashScope API
# https://dashscope.aliyun.com/
```

### 2.2 文心一言（百度）

```python
# 需要修改 ai_generator.py 适配文心 API
# https://cloud.baidu.com/
```

### 2.3 智谱 AI

```python
# 需要修改 ai_generator.py 适配智谱 API
# https://open.bigmodel.cn/
```

## 方案 3: OpenAI 兼容的第三方服务

很多第三方服务提供 OpenAI 兼容的 API，可以直接使用：

```python
# config.py
gemini_api_key = "你的API_Key"
gemini_base_url = "https://第三方服务地址/v1/"
gemini_model = "gpt-3.5-turbo"
```

## 推荐方案

**OpenAI GPT-4o-mini**
- 价格便宜
- 效果好
- 无地区限制
- 直接替换配置即可使用

```python
# config.py
gemini_api_key = os.getenv("OPENAI_API_KEY", "sk-...")
gemini_base_url = "https://api.openai.com/v1/"
gemini_model = "gpt-4o-mini"
```

然后：
```bash
python example_simple.py
```

就可以正常使用了！
