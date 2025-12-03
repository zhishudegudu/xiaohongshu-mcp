# Docker 容器图片路径配置

## 问题说明

MCP 服务器运行在 Docker 容器中，只能访问容器内挂载的目录。

## Docker 挂载配置

根据你的 Docker 配置：
- **宿主机路径**: `E:\docker-xiaohongshu\images`
- **容器内路径**: `/app/images`

## Python 代码配置

### 1. 图片路径配置

在 `config.py` 中已经配置为容器内路径：

```python
def get_default_image_folder() -> str:
    if platform.system() == "Windows":
        # Docker 容器挂载路径（容器内路径）
        return "/app/images"
    else:
        return "/home/wu/images"
```

### 2. 使用方法

**步骤 1**: 将图片放到宿主机目录
```
E:\docker-xiaohongshu\images\
├── 1.jpg
├── 2.jpg
└── 3.jpg
```

**步骤 2**: Python 代码使用容器内路径
```python
# 自动使用 /app/images
publisher = Publisher(mcp_client, config.image_folder)

# 或者手动指定
images = [
    "/app/images/1.jpg",
    "/app/images/2.jpg",
    "/app/images/3.jpg"
]
publisher.publish(title, content, tags, images=images)
```

**步骤 3**: 运行发布
```bash
python example_simple.py
```

## 路径映射关系

| 宿主机路径 | 容器内路径 | Python 代码使用 |
|-----------|-----------|----------------|
| `E:\docker-xiaohongshu\images\1.jpg` | `/app/images/1.jpg` | `/app/images/1.jpg` |
| `E:\docker-xiaohongshu\images\2.jpg` | `/app/images/2.jpg` | `/app/images/2.jpg` |

## 注意事项

### ✅ 正确做法
```python
# 使用容器内路径
images = ["/app/images/1.jpg"]
```

### ❌ 错误做法
```python
# 不要使用宿主机路径（容器访问不到）
images = [r"E:\docker-xiaohongshu\images\1.jpg"]
images = [r"E:\新建文件夹\1.jpg"]
```

## 验证配置

### 1. 检查图片是否在正确位置
```bash
# 在宿主机检查
dir E:\docker-xiaohongshu\images
```

### 2. 检查容器是否能访问
```bash
# 进入容器
docker exec -it <container_id> /bin/sh

# 查看挂载的图片
ls -la /app/images
```

### 3. 测试发布
```bash
python example_simple.py
```

## 常见问题

### Q: 提示"图片文件不存在"？
A: 检查：
1. 图片是否在 `E:\docker-xiaohongshu\images\` 目录
2. Python 代码使用的是 `/app/images/` 路径（不是 `E:\` 路径）
3. Docker 容器的挂载配置是否正确

### Q: 如何添加新图片？
A: 直接复制到 `E:\docker-xiaohongshu\images\` 目录即可

### Q: 可以使用子目录吗？
A: 可以，例如：
```
E:\docker-xiaohongshu\images\food\1.jpg
→ /app/images/food/1.jpg
```

## 总结

**关键点：**
1. 图片放在：`E:\docker-xiaohongshu\images\`
2. 代码使用：`/app/images/xxx.jpg`
3. 不要混用宿主机路径和容器路径

**当前配置已正确设置，直接使用即可！**
