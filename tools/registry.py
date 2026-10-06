from tools.calculator import calculator
from tools.file_tools import list_files, read_file, write_file


# 给 Python Agent 使用：
# 工具名字 -> 真正的 Python 函数
TOOL_FUNCTIONS = {
    "calculator": calculator,
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
}


# 给大模型使用：
# 告诉模型有哪些工具，以及每个工具怎么调用
TOOL_SCHEMAS = [
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
    {
        "type": "function",
        "name": "list_files",
        "description": "列出 workspace/input 目录中的所有文件。",
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "type": "function",
        "name": "read_file",
        "description": "读取 workspace/input 中指定文本文件的内容。",
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
        "description": "把文本写入 workspace/output 中的指定文件。",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "输出文件名，例如 summary.txt",
                },
                "content": {
                    "type": "string",
                    "description": "需要写入的文本内容",
                },
            },
            "required": ["filename", "content"],
        },
    },
]