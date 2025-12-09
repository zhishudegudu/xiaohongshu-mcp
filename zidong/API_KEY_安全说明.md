# API Key 安全配置说明

## ⚠️ 重要警告

**你的 API Key 已泄露！** Google 检测到你的 API Key 被公开到 GitHub，已自动禁用。

## 立即处理步骤

### 1. 获取新的 API Key

1. 访问 Google AI Studio：https://aistudio.google.com/app/apikey
2. 删除旧的 API Key（已泄露的）
3. 创建新的 API Key
4. **不要**把新的 API Key 写在代码里！

### 2. 使用环境变量设置 API Key

**PowerShell（推荐）：**
```powershell
# 临时设置（当前会话有效）
$env:GEMINI_API_KEY="你的新API_Key"

# 验证
echo $env:GEMINI_API_KEY

# 运行程序
python example_auto_images.py
```

**永久设置（Windows）：**
```powershell
# 方法 1: 使用 setx（需要重启终端）
setx GEMINI_API_KEY "你的新API_Key"

# 方法 2: 系统环境变量
# 1. Win + R 输入 sysdm.cpl
# 2. 高级 → 环境变量
# 3. 新建用户变量：
#    变量名：GEMINI_API_KEY
#    变量值：你的新API_Key
```

**Linux/Mac：**
```bash
# 临时设置
export GEMINI_API_KEY="你的新API_Key"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export GEMINI_API_KEY="你的新API_Key"' >> ~/.bashrc
source ~/.bashrc
```

### 3. 验证配置

```bash
python -c "import os; print('API Key:', os.getenv('GEMINI_API_KEY', '未设置'))"
```

### 4. 清理 Git 历史（重要！）

旧的 API Key 仍然在 Git 历史中，需要清理：

```bash
# 方法 1: 使用 BFG Repo-Cleaner（推荐）
# 下载 BFG: https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --replace-text passwords.txt
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 方法 2: 使用 git filter-branch
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch zidong/config.py" \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送（⚠️ 危险操作，会覆盖远程历史）
git push origin --force --all
```

**注意：** 如果仓库是公开的，即使清理了历史，API Key 也可能已经被其他人获取。**必须使用新的 API Key！**

## 最佳实践

### ✅ 正确做法

1. **使用环境变量**
   ```python
   api_key = os.getenv("GEMINI_API_KEY")
   ```

2. **使用 .env 文件**
   ```bash
   # .env 文件
   GEMINI_API_KEY=你的API_Key
   ```
   
   ```python
   # Python 代码
   from dotenv import load_dotenv
   load_dotenv()
   api_key = os.getenv("GEMINI_API_KEY")
   ```

3. **添加 .gitignore**
   ```
   .env
   config_custom.py
   ```

### ❌ 错误做法

1. **硬编码在代码中**
   ```python
   api_key = "AIzaSyXXXXXXXXXXXX"  # ❌ 危险！
   ```

2. **提交到 Git**
   ```bash
   git add config.py  # 包含 API Key ❌
   git commit -m "添加配置"
   git push
   ```

3. **分享截图时暴露**
   - 截图中包含 API Key
   - 日志中打印 API Key

## 当前配置

`config.py` 已修改为：
```python
gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
```

现在必须通过环境变量设置 API Key。

## 使用步骤

### 每次使用前

```powershell
# 1. 设置 API Key
$env:GEMINI_API_KEY="你的新API_Key"

# 2. 验证
python 验证配置.py

# 3. 运行程序
python example_auto_images.py
```

### 一劳永逸（推荐）

将 API Key 添加到系统环境变量，以后就不用每次设置了。

## 检查清单

- [ ] 获取新的 API Key
- [ ] 删除旧的 API Key
- [ ] 设置环境变量 `GEMINI_API_KEY`
- [ ] 验证配置：`python 验证配置.py`
- [ ] 测试运行：`python example_simple.py`
- [ ] 清理 Git 历史（如果仓库是公开的）
- [ ] 添加 `.gitignore`
- [ ] 重新提交代码

## 相关资源

- Google AI Studio: https://aistudio.google.com/app/apikey
- BFG Repo-Cleaner: https://rtyley.github.io/bfg-repo-cleaner/
- Git 清理敏感数据: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

## 总结

**永远不要把 API Key 写在代码里！**

✅ 使用环境变量
✅ 使用 .env 文件
✅ 添加 .gitignore
✅ 定期轮换 API Key
