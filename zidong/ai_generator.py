"""
AI内容生成模块
"""
import json
from typing import Dict, Any, Optional
from openai import OpenAI


class AIGenerator:
    """AI内容生成器（基于Gemini）"""
    
    def __init__(self, api_key: str, base_url: str, model: str = "gemini-1.5-pro"):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
    
    def generate_from_scratch(self, topic: str) -> Dict[str, str]:
        """
        从零开始生成内容（原有方法）
        
        Args:
            topic: 主题
        
        Returns:
            包含title和content的字典
        """
        print(f"🧠 Gemini 正在创作主题：{topic}")
        
        prompt = f"""
        你是一个资深的小红书博主。请以此主题写一篇笔记：【{topic}】

        要求：
        1. 标题：吸引眼球，带Emoji，不超过20字。
        2. 正文：
           - 口语化，多用短句。
           - 情绪价值拉满，甚至可以带点争议性。
           - 必须包含大量 Emoji 穿插在文中。
           - 结尾带 5 个相关的热门 Tag。
        3. 格式：严格返回 JSON 格式，包含 'title' 和 'content' 两个字段。
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a creative writer. Output valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def generate_from_references(self, topic: str, reference_data: Dict[str, Any]) -> Dict[str, str]:
        """
        基于参考资料生成内容（新方法）
        
        Args:
            topic: 主题
            reference_data: 参考资料（来自content_crawler）
        
        Returns:
            包含title、content和tags的字典
        """
        print(f"🧠 Gemini 正在基于 {len(reference_data.get('titles', []))} 条参考资料创作...")
        
        # 构建参考资料摘要
        ref_summary = self._build_reference_summary(reference_data)
        
        prompt = f"""
        你是一个资深的小红书博主。请基于以下参考资料，创作一篇关于【{topic}】的笔记。

        === 参考资料 ===
        {ref_summary}

        === 创作要求 ===
        1. 标题：吸引眼球，带Emoji，不超过20字
        2. 正文：
           - 参考热门内容的风格，但要有自己的创新
           - 口语化，多用短句
           - 情绪价值拉满
           - 必须包含大量 Emoji 穿插在文中
           - 不要直接抄袭参考内容，要融会贯通
        3. 标签：从参考资料中选择5-8个最相关的热门标签
        4. 格式：严格返回 JSON 格式，包含 'title'、'content' 和 'tags' 三个字段
        
        注意：tags字段应该是一个字符串数组，例如 ["美食", "探店", "生活"]
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a creative writer specialized in Xiaohongshu content. Output valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        print(f"✅ 生成完成: {result.get('title', 'N/A')}")
        
        return result
    
    def _build_reference_summary(self, reference_data: Dict[str, Any]) -> str:
        """构建参考资料摘要"""
        summary_parts = []
        
        # 热门标题
        if reference_data.get("titles"):
            titles_text = "\n".join([f"- {t}" for t in reference_data["titles"][:5]])
            summary_parts.append(f"热门标题示例:\n{titles_text}")
        
        # 热门标签
        if reference_data.get("tags"):
            tags_text = ", ".join(reference_data["tags"])
            summary_parts.append(f"\n热门标签: {tags_text}")
        
        # 最受欢迎的内容
        if reference_data.get("top_content"):
            top = reference_data["top_content"]
            summary_parts.append(f"\n最受欢迎的内容 ({top['likes']} 赞):\n标题: {top['title']}\n内容片段: {top['content'][:200]}...")
        
        # 内容片段
        if reference_data.get("contents"):
            contents_preview = "\n".join([f"- {c[:100]}..." for c in reference_data["contents"][:3]])
            summary_parts.append(f"\n其他内容片段:\n{contents_preview}")
        
        return "\n".join(summary_parts)
    
    def generate_image_keywords(self, title: str, content: str, count: int = 3) -> list[str]:
        """
        根据标题和内容生成图片搜索关键词
        
        Args:
            title: 标题
            content: 内容
            count: 需要的关键词数量
        
        Returns:
            英文关键词列表（用于图片搜索）
        """
        print(f"🎨 生成图片搜索关键词...")
        
        prompt = f"""
        请根据以下小红书笔记的标题和内容，生成 {count} 个适合搜索配图的英文关键词。
        
        标题：{title}
        内容：{content[:300]}...
        
        要求：
        1. 关键词必须是英文（用于 Unsplash 搜索）
        2. 关键词要具体、视觉化（例如：coffee, food, sunset）
        3. 关键词要符合小红书的美学风格
        4. 返回 JSON 格式：{{"keywords": ["word1", "word2", "word3"]}}
        
        示例：
        - 美食类 → ["food", "dessert", "coffee"]
        - 旅行类 → ["travel", "beach", "sunset"]
        - 时尚类 → ["fashion", "style", "outfit"]
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Output valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        keywords = result.get("keywords", [])
        
        print(f"   关键词: {', '.join(keywords)}")
        
        return keywords
