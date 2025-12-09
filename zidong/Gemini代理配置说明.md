# Gemini API 代理配置说明

## 问题

如果你遇到以下错误：

```
openai.BadRequestError: Error code: 400 - User location is not supported for the API use.
```

这是因为 **Google Gemini API 限制了某些地区的访问**。

## 解决方案

### 方法 1: 使用代理（推荐）

#### 1. 准备代理

你需要一个支持的地区（如美国、日本）的代理服务器。

常见代理软件：
- **Clash** (推荐)
- **V2Ray**
- **Shadowsocks**

#### 2. 获取代理地址

启动代理软件后，通常会提供本地代理地址：

- HTTP 代理：`http://127.0.0.1:7890`
- SOCKS5 代理：`socks5://127.0.0.1:7890`

端口号可能不同，请查看你的代理软件设置。

#### 3. 设置环境变量

**PowerShell（临时设置）：**
```powershell
# 设置代理
$env:GEMINI_PROXY="http://127.0.0.1:7890"

# 验证
echo $env:GEMINI_PROXY

# 运行程序
python example_simple.py
```

**PowerShell（永久设置）：**
```powershell
# 方法 1: 使用 setx（需要重启终端）
setx GEMINI_PROXY "http://127.0.0.1:7890"

# 方法 2: 系统环境变量
# Win + R → sysdm.cpl → 高级 → 环境变量
# 新建用户变量：
#   变量名：GEMINI_PROXY
#   变量值：http://127.0.0.1:7890
```

**Linux/Mac：**
```bash
# 临时设置
export GEMINI_PROXY="http://127.0.0.1:7890"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export GEMINI_PROXY="http://127.0.0.1:7890"' >> ~/.bashrc
source ~/.bashrc
```

#### 4. 测试

```bash
python example_simple.py
```

如果看到：
```
🌐 使用代理: http://127.0.0.1:7890
🧠 Gemini 正在创作主题：...
```

说明代理配置成功！

### 方法 2: 使用其他 AI 服务

如果无法使用代理，可以考虑：

#### OpenAI GPT

```python
# config.py
gemini_api_key = "sk-..."  # OpenAI API Key
gemini_base_url = "https://api.openai.com/v1/"
gemini_model = "gpt-4o-mini"
```

#### 国内 AI 服务

- **通义千问**：https://dashscope.aliyun.com/
- **文心一言**：https://cloud.baidu.com/
- **智谱 AI**：https://open.bigmodel.cn/

需要修改 `ai_generator.py` 适配不同的 API 格式。

## 常见问题

### Q1: 代理设置后还是报错？

**检查代理是否正常：**
```bash
curl -x http://127.0.0.1:7890 https://www.google.com
```

如果能访问 Google，说明代理正常。

### Q2: 代理端口号是多少？

不同软件默认端口不同：
- **Clash**: 7890
- **V2Ray**: 10808
- **Shadowsocks**: 1080

查看你的代理软件设置。

### Q3: HTTP 还是 SOCKS5？

两种都支持：
- `http://127.0.0.1:7890`
- `socks5://127.0.0.1:7890`

优先使用 HTTP 代理。

### Q4: 代理影响 MCP 服务器连接吗？

**不会！** 代码已经处理：
- Gemini API：使用代理
- MCP 服务器（localhost）：不使用代理

### Q5: 可以不设置代理吗？

如果你的地区支持 Gemini API，可以不设置：
```powershell
# 不设置 GEMINI_PROXY 环境变量
python example_simple.py
```

程序会直接连接 Gemini API。

## 配置检查清单

- [ ] 代理软件已启动
- [ ] 获取代理地址（如 `http://127.0.0.1:7890`）
- [ ] 设置环境变量 `GEMINI_PROXY`
- [ ] 验证环境变量：`echo $env:GEMINI_PROXY`
- [ ] 测试代理：`curl -x http://127.0.0.1:7890 https://www.google.com`
- [ ] 运行程序：`python example_simple.py`

## 示例：完整流程

```powershell
# 1. 启动代理软件（如 Clash）

# 2. 设置环境变量
$env:GEMINI_PROXY="http://127.0.0.1:7890"
$env:GEMINI_API_KEY="你的API_Key"

# 3. 验证
echo $env:GEMINI_PROXY
echo $env:GEMINI_API_KEY

# 4. 运行
python example_simple.py
```

## 总结

- ✅ **推荐方案**：使用代理 + Gemini API
- ✅ **备用方案**：使用 OpenAI GPT 或国内 AI 服务
- ✅ **配置简单**：只需设置 `GEMINI_PROXY` 环境变量
- ✅ **不影响其他功能**：MCP 服务器连接不受影响

**现在可以正常使用 Gemini API 了！** 🎉
