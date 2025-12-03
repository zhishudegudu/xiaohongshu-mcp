# 小红书自动化发布工具

基于 Gemini Pro 的小红书内容自动生成和发布工具。

## 🎯 功能特性

### 两种生成模式

1. **从零开始生成**：直接让 AI 根据主题创作内容
2. **基于参考资料生成**（推荐）：
   - 爬取小红书热门内容
   - 清洗和提取关键信息
   - AI 融合参考资料生成新内容
   - 自动提取热门标签

### 完整流程

```
爬取参考资料 → 数据清洗 → AI生成 → 自动发布
```

## 📦 项目结构

```
zidong/
├── config.py          # 配置管理
├── mcp_client.py      # MCP客户端封装
├── content_crawler.py # 爬取和清洗模块
├── ai_generator.py    # AI生成模块
├── publisher.py       # 发布模块
├── main.py           # 主程序
├── requirements.txt   # 依赖包
└── README.md         # 说明文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd zidong
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件或直接修改 `config.py`：

```bash
# Gemini API Key
export GEMINI_API_KEY="your_gemini_api_key"

# MCP服务器地址
export MCP_SERVER_URL="http://127.0.0.1:18060/mcp"

# 图片文件夹路径（Docker 容器内路径）
export IMAGE_FOLDER="/app/images"
```

**⚠️ 图片路径配置（重要）：**

支持两种运行模式，通过环境变量 `USE_DOCKER` 控制：

**Docker 模式**（MCP 服务器在容器中）：
```bash
$env:USE_DOCKER="true"
python example_simple.py
```
- 图片放到：`E:\xiao\xiaohongshu-mcp\docker\images\`
- 自动使用容器路径：`/app/images/`

**本地模式**（MCP 服务器直接运行，默认）：
```bash
python example_simple.py
```
- 图片放到：`E:\新建文件夹\`
- 直接使用本地路径

详见 [图片路径配置.md](./图片路径配置.md)

### 3. 配置代理（如需要）

如果访问 Gemini API 需要代理，编辑 `config.py` 文件顶部（第 12-13 行）：

```python
# 取消注释并修改为你的代理端口
os.environ["http_proxy"] = "http://127.0.0.1:1080"
os.environ["https_proxy"] = "http://127.0.0.1:1080"
```

**常见代理端口：**
- Clash: `7890`
- V2Ray: `1080` 或 `10808`
- Shadowsocks: `1080`

### 4. 确保小红书已登录

使用 MCP 客户端（如 Claude Desktop）调用 `get_login_qrcode` 工具扫码登录。

### 5. 运行程序

```bash
python main.py
```

## 💡 使用示例

### 模式1：从零开始生成

```
请选择生成模式: 1
请输入主题: 第一次用Python自动发小红书是什么体验
```

### 模式2：基于参考资料生成（推荐）

```
请选择生成模式: 2
请输入主题: 美食探店
请输入搜索关键词: 上海美食推荐
```

程序会：
1. 搜索"上海美食推荐"相关的热门笔记
2. 提取标题、内容、标签等信息
3. 让 AI 基于这些参考资料生成新内容
4. 自动选择图片并发布

## ⚙️ 配置说明

### config.py 主要配置项

```python
# Gemini配置
gemini_api_key: str        # Gemini API Key
gemini_model: str          # 模型名称（默认：gemini-1.5-pro）

# MCP服务器配置
mcp_server_url: str        # MCP服务器地址

# 图片配置
image_folder: str          # 图片文件夹路径

# 爬取配置
crawl_limit: int           # 爬取数量限制（默认：10）

# 发布配置
auto_publish: bool         # 是否自动发布（默认：False）
```

## 🔧 模块说明

### 1. mcp_client.py - MCP客户端

封装了与小红书MCP服务器的交互：
- `check_login_status()` - 检查登录状态
- `search_feeds()` - 搜索内容
- `get_feed_detail()` - 获取详情
- `publish_content()` - 发布内容

### 2. content_crawler.py - 内容爬取器

负责爬取和清洗数据：
- `crawl_reference_content()` - 爬取参考内容
- `clean_and_extract()` - 清洗和提取数据
- `get_reference_materials()` - 一站式获取参考资料

### 3. ai_generator.py - AI生成器

使用 Gemini Pro 生成内容：
- `generate_from_scratch()` - 从零开始生成
- `generate_from_references()` - 基于参考资料生成

### 4. publisher.py - 发布器

负责内容发布：
- `get_random_images()` - 随机选择图片
- `publish()` - 发布内容

## 📝 注意事项

1. **API Key 安全**：不要将 API Key 提交到代码仓库
2. **登录状态**：发布前确保已登录小红书
3. **图片准备**：
   - 将图片放到宿主机目录：`E:\docker-xiaohongshu\images\`
   - Python 代码使用容器路径：`/app/images/`
   - 不要混用宿主机路径和容器路径
4. **发布频率**：避免频繁发布，以免被平台限制
5. **内容审核**：建议手动审核生成的内容后再发布

## 🎨 后续优化方向

1. **读取海量参考资料**：
   - 支持批量爬取多个关键词
   - 支持从本地文件读取参考资料
   - 支持从数据库读取历史数据

2. **内容质量提升**：
   - 添加内容去重检测
   - 添加敏感词过滤
   - 支持自定义 Prompt 模板

3. **发布策略**：
   - 支持定时发布
   - 支持批量发布
   - 支持发布后数据统计

4. **多平台支持**：
   - 同时发布到多个平台
   - 根据平台特性调整内容格式

## 📄 License

MIT
