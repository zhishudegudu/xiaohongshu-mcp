# 🚀 完整配置和调试指南

## 📋 前提条件检查清单

在开始之前，请确认以下条件：

### ✅ 必需条件
- [ ] **Python 3.8+** 已安装在 Windows 上
- [ ] **PyCharm** 已安装
- [ ] **小红书 MCP 服务器** 正在运行（Go 程序）
- [ ] **Gemini API Key** 已获取（从 https://aistudio.google.com/app/apikey）
- [ ] **网络连接** 正常（能访问 Google API）

### 📍 确认 MCP 服务器状态

**步骤1：检查 MCP 服务器是否运行**

在 Windows 命令行中运行：
```cmd
netstat -ano | findstr :18060
```

如果看到输出，说明服务器正在运行。

**步骤2：在浏览器中测试**

打开浏览器访问：
```
http://127.0.0.1:18060
```

如果能看到页面（即使是错误页面），说明服务器正在运行。

---

## 🔧 配置步骤

### 步骤 1：修改 config.py

在 PyCharm 中打开 `zidong/config.py`，修改以下配置：

```python
@dataclass
class Config:
    """全局配置"""
    
    # ========== 必须修改 ==========
    
    # 1. 填入你的 Gemini API Key
    gemini_api_key: str = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXX"  # ← 改这里
    
    # 2. MCP 服务器地址
    # 如果 Python 和 MCP 在同一台 Windows 机器上：
    mcp_server_url: str = "http://127.0.0.1:18060/mcp"
    
    # 如果 MCP 在其他机器上（比如 WSL 或远程服务器）：
    # mcp_server_url: str = "http://192.168.21.59:18060/mcp"
    
    # 3. 图片文件夹路径（Windows 格式）
    # 方式1：使用 r 前缀（推荐）
    image_folder: str = r"C:\Users\你的用户名\Pictures\xiaohongshu"
    
    # 方式2：使用正斜杠
    # image_folder: str = "C:/Users/你的用户名/Pictures/xiaohongshu"
    
    # ========== 可选配置 ==========
    
    crawl_limit: int = 10          # 每次爬取的数量
    auto_publish: bool = False     # 是否自动发布（建议先设为 False）
```

### 步骤 2：创建图片文件夹

1. 打开 Windows 资源管理器
2. 创建文件夹，例如：`C:\Users\wu\Pictures\xiaohongshu`
3. 在文件夹中放入至少 3 张图片（.jpg, .png, .jpeg 格式）

### 步骤 3：安装 Python 依赖

在 PyCharm 终端中运行：

```bash
# 切换到 zidong 目录
cd zidong

# 安装依赖
pip install -r requirements.txt
```

或者在 PyCharm 中：
1. 打开 `requirements.txt`
2. PyCharm 会提示 "Install requirements"
3. 点击安装

---

## 🧪 调试步骤

### 第一步：测试连接

运行测试脚本检查配置：

```bash
python test_connection.py
```

**预期输出：**
```
============================================================
🔍 环境检测
============================================================

📌 操作系统: Windows 10
📌 Python 版本: 3.11.0

⚙️ 配置信息:
   - MCP 服务器: http://127.0.0.1:18060/mcp
   - 图片文件夹: C:\Users\wu\Pictures\xiaohongshu
   - Gemini 模型: gemini-1.5-pro
   - API Key: 已配置

📁 图片文件夹检查:
   ✅ 文件夹存在
   ✅ 找到 5 张图片
   示例: image1.jpg

🔌 MCP 服务器连接测试:
   ✅ 连接成功！
   登录状态: ✅ 已登录

============================================================
📊 检测完成
============================================================
```

**如果出现错误，请看下面的故障排除部分。**

### 第二步：测试简单生成（不爬取）

运行简单示例：

```bash
python example_simple.py
```

这个脚本会：
1. 使用 Gemini 生成内容
2. 随机选择 3 张图片
3. 显示预览
4. 等待你确认发布

### 第三步：测试完整流程（爬取+生成）

运行完整示例：

```bash
python example_with_crawl.py
```

这个脚本会：
1. 搜索"上海美食推荐"
2. 爬取 10 条参考内容
3. 清洗数据
4. 基于参考资料生成新内容
5. 显示预览
6. 等待你确认发布

### 第四步：运行主程序（交互式）

运行主程序：

```bash
python main.py
```

主程序会提供交互式界面，让你选择：
- 生成模式（从零开始 / 基于参考资料）
- 输入主题
- 输入搜索关键词
- 确认发布

---

## 🐛 故障排除

### ❌ 问题 1：无法连接 MCP 服务器

**错误信息：**
```
❌ 连接失败: 无法连接到 MCP 服务器
```

**解决方案：**

1. **检查 MCP 服务器是否运行**
   ```cmd
   # 在命令行中运行
   netstat -ano | findstr :18060
   ```
   
2. **检查地址是否正确**
   - 如果 Python 和 MCP 在同一台机器：使用 `http://127.0.0.1:18060/mcp`
   - 如果 MCP 在 WSL：使用 `http://localhost:18060/mcp`
   - 如果 MCP 在远程机器：使用 `http://IP地址:18060/mcp`

3. **检查防火墙**
   - Windows 防火墙可能阻止了连接
   - 临时关闭防火墙测试

4. **测试端口连通性**
   ```cmd
   # 在浏览器中访问
   http://127.0.0.1:18060
   ```

### ❌ 问题 2：图片文件夹不存在

**错误信息：**
```
❌ 文件夹不存在！
```

**解决方案：**

1. 检查路径格式是否正确（Windows 路径）
2. 确保文件夹已创建
3. 检查路径中的用户名是否正确

**正确的路径格式：**
```python
# ✅ 正确
image_folder = r"C:\Users\wu\Pictures\xiaohongshu"
image_folder = "C:/Users/wu/Pictures/xiaohongshu"

# ❌ 错误
image_folder = "/home/wu/images"  # Linux 路径
image_folder = "C:\Users\wu\Pictures\xiaohongshu"  # 缺少 r 前缀
```

### ❌ 问题 3：Gemini API 错误

**错误信息：**
```
❌ 生成失败: Invalid API key
```

**解决方案：**

1. **检查 API Key 是否正确**
   - 访问 https://aistudio.google.com/app/apikey
   - 复制完整的 API Key
   - 确保没有多余的空格

2. **检查 API 配额**
   - Gemini API 有免费配额限制
   - 检查是否超出配额

3. **检查网络连接**
   - 确保能访问 Google 服务
   - 可能需要代理

### ❌ 问题 4：未登录小红书

**错误信息：**
```
登录状态: ❌ 未登录
```

**解决方案：**

你需要先使用 MCP 客户端登录小红书。有两种方式：

**方式 1：使用 Claude Desktop（推荐）**
1. 安装 Claude Desktop
2. 配置 MCP 服务器
3. 在对话中说："帮我登录小红书"
4. 扫描二维码

**方式 2：使用 MCP Inspector**
1. 访问 MCP Inspector 网页
2. 连接到你的 MCP 服务器
3. 调用 `get_login_qrcode` 工具
4. 扫描二维码

**方式 3：直接访问 API（临时方案）**
```python
# 创建一个临时脚本 login.py
from mcp_client import MCPClient

client = MCPClient("http://127.0.0.1:18060/mcp")
# 调用获取二维码的方法
# 然后用小红书 App 扫码
```

---

## 📝 完整运行流程示例

### 场景：发布一篇美食笔记

```bash
# 1. 测试连接
python test_connection.py

# 2. 运行主程序
python main.py

# 3. 按照提示操作：
#    - 选择模式: 2 (基于参考资料)
#    - 输入主题: 上海网红美食探店
#    - 输入关键词: 上海美食
#    - 等待生成...
#    - 查看预览
#    - 按回车确认发布
```

---

## 🎯 PyCharm 运行配置

### 方法 1：直接运行

1. 在 PyCharm 中打开 `main.py`
2. 右键点击文件
3. 选择 "Run 'main'"

### 方法 2：配置运行配置

1. Run → Edit Configurations
2. 点击 "+" → Python
3. 配置如下：
   - **Name**: 小红书自动发布
   - **Script path**: 选择 `main.py`
   - **Working directory**: 选择 `zidong` 文件夹
   - **Python interpreter**: 选择你的 Python 解释器
4. 点击 "OK"
5. 点击运行按钮

### 方法 3：使用终端

在 PyCharm 底部的 Terminal 中：
```bash
cd zidong
python main.py
```

---

## 🔐 环境变量配置（推荐）

为了安全，建议使用环境变量存储敏感信息：

### Windows 临时设置（当前终端）

```cmd
set GEMINI_API_KEY=你的API_Key
set IMAGE_FOLDER=C:\Users\wu\Pictures\xiaohongshu
set MCP_SERVER_URL=http://127.0.0.1:18060/mcp
```

### Windows 永久设置

1. 右键"此电脑" → "属性"
2. "高级系统设置" → "环境变量"
3. 在"用户变量"中添加：
   - 变量名：`GEMINI_API_KEY`，值：你的 API Key
   - 变量名：`IMAGE_FOLDER`，值：`C:\Users\wu\Pictures\xiaohongshu`
   - 变量名：`MCP_SERVER_URL`，值：`http://127.0.0.1:18060/mcp`

### PyCharm 中设置环境变量

1. Run → Edit Configurations
2. 在 "Environment variables" 中添加
3. 格式：`KEY=VALUE;KEY2=VALUE2`

---

## 📊 调试技巧

### 1. 查看详细日志

在代码中添加调试信息：

```python
# 在 main.py 开头添加
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. 分步测试

不要一次运行完整流程，分步测试：

```python
# 只测试爬取
from content_crawler import ContentCrawler
from mcp_client import MCPClient

client = MCPClient("http://127.0.0.1:18060/mcp")
crawler = ContentCrawler(client)
data = crawler.get_reference_materials("美食", limit=5)
print(data)
```

### 3. 使用 PyCharm 调试器

1. 在代码行号左侧点击，设置断点
2. 右键 → "Debug 'main'"
3. 逐步执行，查看变量值

---

## ✅ 成功标志

当你看到以下输出，说明一切正常：

```
🚀 小红书自动化发布工具启动...
============================================================

📦 初始化模块...

🔐 检查登录状态...
✅ 已登录

============================================================
请选择生成模式:
1. 从零开始生成（不需要参考资料）
2. 基于参考资料生成（推荐）
============================================================
```

---

## 📞 需要帮助？

如果遇到问题：

1. 先运行 `python test_connection.py` 检查配置
2. 查看上面的故障排除部分
3. 检查 Python 版本：`python --version`
4. 检查依赖安装：`pip list`
5. 查看 MCP 服务器日志
