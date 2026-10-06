import os

from dotenv import load_dotenv
from openai import OpenAI

# 从统一工具注册表读取“给模型看的工具说明”
from tools.registry import TOOL_SCHEMAS


# 加载 .env
load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("没有找到 DEEPSEEK_API_KEY，请检查 .env 文件")


# 创建 DeepSeek 客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)


def call_llm(input_items):
    """
    把 Agent 当前的历史记录发送给 DeepSeek。
    """

    response = client.responses.create(
        model="deepseek-flash",

        # 当前完整历史
        input=input_items,

        # 告诉 DeepSeek 有哪些工具可以使用
        tools=TOOL_SCHEMAS,

        # 模型自己决定是否使用工具
        tool_choice="auto",

        # 暂时关闭 thinking mode，
        # 避免目前还要额外维护 reasoning 历史
        reasoning={"effort": "none"},
    )

    return response