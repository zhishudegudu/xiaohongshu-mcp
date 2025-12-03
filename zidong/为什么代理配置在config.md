# 为什么代理配置放在 config.py？

## 原因

### 1. 符合单一职责原则
- `config.py` - 负责所有配置管理（API Key、服务器地址、代理等）
- `ai_generator.py` - 负责 AI 内容生成的业务逻辑

### 2. 集中管理配置
所有配置项都在一个文件中，方便查找和修改：
```
config.py
├── Gemini API 配置
├── MCP 服务器配置
├── 图片文件夹配置
├── 代理配置 ⬅️ 新增
└── 其他配置
```

### 3. 执行顺序保证
`config.py` 在程序启动时最先被导入，确保代理设置在所有网络请求之前生效：

```python
# 其他模块导入 config 时，代理已经设置好了
from config import config  # ← 此时代理已生效
from ai_generator import AIGenerator  # ← 使用时代理已就绪
```

### 4. 避免重复配置
如果将来有其他模块也需要访问外部 API（如图片上传、数据分析等），不需要重复设置代理。

## 代码结构对比

### ❌ 不好的做法（放在 ai_generator.py）
```python
# ai_generator.py
import os
os.environ["http_proxy"] = "..."  # 只对这个模块生效？

# content_crawler.py
import os
os.environ["http_proxy"] = "..."  # 需要重复设置

# publisher.py
import os
os.environ["http_proxy"] = "..."  # 又要重复设置
```

### ✅ 好的做法（放在 config.py）
```python
# config.py
import os
os.environ["http_proxy"] = "..."  # 全局生效，一次配置

# ai_generator.py
from config import config  # 自动继承代理设置

# content_crawler.py
from config import config  # 自动继承代理设置

# publisher.py
from config import config  # 自动继承代理设置
```

## 总结

将代理配置放在 `config.py` 是最佳实践，因为：
1. **职责清晰** - 配置归配置，业务归业务
2. **易于维护** - 所有配置集中管理
3. **避免重复** - 一次设置，全局生效
4. **执行可靠** - 最先加载，确保生效
