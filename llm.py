import os

from dotenv import load_dotenv
from openai import OpenAI


# 读取 .env 文件里的环境变量
load_dotenv()

# 从环境变量里拿 DeepSeek API Key
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("没有找到 DEEPSEEK_API_KEY，请检查 .env 文件")


# 创建 DeepSeek 客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)


# tools 是给 DeepSeek 看的“工具说明书”
#
# 注意：
# 这里只是在告诉模型“有哪些工具、参数是什么”
# 并没有真的执行这些 Python 函数
tools = [
    # -------------------------
    # 工具 1：calculator
    # -------------------------
    {
        "type": "function",
        "name": "calculator",
        "description": "用于进行两个数字之间的基本数学运算。",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "第一个数字",
                },
                "b": {
                    "type": "number",
                    "description": "第二个数字",
                },
                "operator": {
                    "type": "string",
                    "enum": ["+", "-", "*", "/"],
                    "description": "数学运算符",
                },
            },
            "required": ["a", "b", "operator"],
        },
    },

    # -------------------------
    # 工具 2：list_files
    # -------------------------
    {
        "type": "function",
        "name": "list_files",
        "description": "列出 workspace 目录中的所有文件。",
        "parameters": {
            "type": "object",

            # 这个工具不需要任何参数
            "properties": {},
        },
    },

    # -------------------------
    # 工具 3：read_file
    # -------------------------
    {
        "type": "function",
        "name": "read_file",
        "description": "读取 workspace 目录中指定文本文件的内容。",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "要读取的文件名，例如 a.txt",
                },
            },
            "required": ["filename"],
        },
    },

    {
    "type": "function",
    "name": "write_file",
    "description": "把文本内容写入 workspace 目录中的指定文件。",
    "parameters": {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "要写入的文件名，例如 summary.txt",
            },
            "content": {
                "type": "string",
                "description": "要写入文件的文本内容",
            },
            },
        "required": ["filename", "content"],
        },
    },
]


def call_llm(input_items):
    """
    把当前 Agent 的历史记录发给 DeepSeek。
    """

    response = client.responses.create(
    model="deepseek-flash",
    input=input_items,
    tools=tools,
    tool_choice="auto",

    # 暂时关闭 DeepSeek 的 thinking mode。
    # 这样我们当前只需要维护：
    # 用户消息、工具调用、工具结果。
    reasoning={"effort": "none"},
    )

    return response