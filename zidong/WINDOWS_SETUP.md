# Windows 环境配置指南

## 🪟 在 Windows 上运行本项目

### 1️⃣ 前置条件

- ✅ Python 3.8+ (已安装)
- ✅ PyCharm (已安装)
- ✅ 小红书 MCP 服务器正在运行

### 2️⃣ MCP 服务器位置判断

你的 MCP 服务器可能在两个地方运行：

#### **情况A：MCP 在 WSL (Linux子系统) 中运行**
```python
# config.py 中使用
mcp_server_url = "http://localhost:18060/mcp"
# 或者使用 WSL 的 IP 地址
mcp_server_url = "http://192.168.21.59:18060/mcp"
```

#### **情况B：MCP 在 Windows 上运行**
```python
# config.py 中使用
mcp_server_url = "http://localhost:18060/mcp"
# 或
mcp_server_url = "http://127.0.0.1:18060/mcp"
```

### 3️⃣ 配置步骤

#### **步骤1：修改配置文件**

在 PyCharm 中打开 `config.py`，修改以下配置：

```python
# 1. 填入你的 Gemini API Key
gemini_api_key: str = "你的真实API Key"

# 2. 设置图片文件夹（Windows路径格式）
image_folder: str = r"C:\Users\你的用户名\Pictures\xiaohongshu"
# 注意：路径前面加 r 或者使用 / 代替 \

# 3. 设置 MCP 服务器地址
mcp_server_url: str = "http://localhost:18060/mcp"
```

#### **步骤2：创建图片文件夹**

在 Windows 资源管理器中创建图片文件夹，例如：
```
C:\Users\wu\Pictures\xiaohongshu\
```

然后放入一些图片（.jpg, .png, .jpeg 格式）

#### **步骤3：安装依赖**

在 PyCharm 的终端中运行：
```bash
cd zidong
pip install -r requirements.txt
```

或者在 PyCharm 中：
1. 打开 `requirements.txt`
2. PyCharm 会提示安装依赖
3. 点击 "Install requirements"

### 4️⃣ 运行方式

#### **方式1：在 PyCharm 中运行**

1. 打开 `main.py` 或 `example_with_crawl.py`
2. 右键点击文件
3. 选择 "Run 'main'" 或 "Run 'example_with_crawl'"

#### **方式2：在终端中运行**

```bash
cd C:\path\to\xiaohongshu-mcp\zidong
python main.py
```

### 5️⃣ 常见问题

#### ❓ 问题1：路径错误
```
错误：找不到图片文件夹 /home/wu/images
```

**解决方案**：
- 检查 `config.py` 中的 `image_folder` 是否使用了 Windows 路径格式
- 确保路径存在且包含图片文件

#### ❓ 问题2：无法连接 MCP 服务器
```
错误：无法连接到 MCP 服务器: http://192.168.21.59:18060/mcp
```

**解决方案**：
1. 检查 MCP 服务器是否正在运行
2. 如果 MCP 在 WSL 中，使用 `localhost` 或 WSL 的 IP
3. 在浏览器中访问 `http://localhost:18060` 测试连接

#### ❓ 问题3：Gemini API 错误
```
错误：Invalid API key
```

**解决方案**：
- 检查 API Key 是否正确
- 确保 API Key 有足够的配额
- 访问 https://aistudio.google.com/app/apikey 检查 API Key

### 6️⃣ 推荐的 Windows 路径配置

```python
# config.py 示例配置（Windows）

@dataclass
class Config:
    # Gemini API Key（从 https://aistudio.google.com/app/apikey 获取）
    gemini_api_key: str = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
    # MCP 服务器地址
    mcp_server_url: str = "http://localhost:18060/mcp"
    
    # 图片文件夹（使用你的实际路径）
    image_folder: str = r"C:\Users\wu\Pictures\xiaohongshu"
    # 或者
    # image_folder: str = "C:/Users/wu/Pictures/xiaohongshu"
```

### 7️⃣ 测试连接

创建一个测试脚本 `test_connection.py`：

```python
from config import config
from mcp_client import MCPClient

# 测试 MCP 连接
print(f"MCP 服务器地址: {config.mcp_server_url}")
print(f"图片文件夹: {config.image_folder}")

try:
    client = MCPClient(config.mcp_server_url)
    is_logged_in = client.check_login_status()
    print(f"✅ MCP 连接成功！登录状态: {is_logged_in}")
except Exception as e:
    print(f"❌ MCP 连接失败: {e}")
```

### 8️⃣ 环境变量配置（可选）

如果不想在代码中写 API Key，可以设置环境变量：

**临时设置（当前终端有效）：**
```cmd
set GEMINI_API_KEY=你的API_Key
set IMAGE_FOLDER=C:\Users\wu\Pictures\xiaohongshu
set MCP_SERVER_URL=http://localhost:18060/mcp
```

**永久设置：**
1. 右键"此电脑" → "属性"
2. "高级系统设置" → "环境变量"
3. 在"用户变量"中添加：
   - `GEMINI_API_KEY` = 你的API Key
   - `IMAGE_FOLDER` = C:\Users\wu\Pictures\xiaohongshu
   - `MCP_SERVER_URL` = http://localhost:18060/mcp

### 9️⃣ PyCharm 运行配置

在 PyCharm 中设置运行配置：

1. Run → Edit Configurations
2. 添加新的 Python 配置
3. Script path: 选择 `main.py`
4. Working directory: 选择 `zidong` 文件夹
5. Environment variables: 添加环境变量（可选）

### 🎯 快速开始清单

- [ ] 安装 Python 依赖：`pip install -r requirements.txt`
- [ ] 修改 `config.py` 中的 API Key
- [ ] 修改 `config.py` 中的图片文件夹路径（Windows格式）
- [ ] 创建图片文件夹并放入图片
- [ ] 确认 MCP 服务器正在运行
- [ ] 运行 `python main.py` 测试

### 📞 需要帮助？

如果遇到问题，请检查：
1. Python 版本：`python --version` (需要 3.8+)
2. 依赖安装：`pip list | findstr "openai requests"`
3. MCP 服务器状态：浏览器访问 `http://localhost:18060`
4. 路径格式：确保使用 Windows 路径格式
