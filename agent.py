import json

from llm import call_llm

# 导入我们真正可以执行的工具
from tools.calculator import calculator
from tools.file_tools import list_files, read_file, write_file


def run_agent(user_input: str) -> str:
    """
    一个可以循环调用工具的简单 Agent。
    """

    # history = Agent 的任务记录本
    history = [
        {
            "role": "user",
            "content": user_input,
        }
    ]

    step = 0

    while True:
        step += 1

        print(f"\n===== Agent 第 {step} 轮 =====")

        # 防止模型一直调用工具导致死循环
        if step > 10:
            raise RuntimeError("Agent 超过最大执行轮数")

        # 把当前所有历史交给 DeepSeek
        response = call_llm(history)

        # 先假设模型这一轮不需要工具
        tool_call = None

        # 检查 DeepSeek 返回的内容里有没有工具调用
        for item in response.output:
            if item.type == "function_call":
                tool_call = item
                break

        # 没有工具调用：
        # 说明模型认为任务已经完成
        if tool_call is None:
            return response.output_text

        print(f"模型决定调用工具：{tool_call.name}")
        print(f"模型提供参数：{tool_call.arguments}")

        # 把模型给我们的 JSON 参数转换成 Python 数据
        arguments = json.loads(tool_call.arguments)

        # --------------------------------
        # 根据模型选择的工具，真正执行 Python 函数
        # --------------------------------

        if tool_call.name == "calculator":
            result = calculator(**arguments)

        elif tool_call.name == "list_files":
            result = list_files()

        elif tool_call.name == "read_file":
            result = read_file(**arguments)

        elif tool_call.name == "write_file":
            result = write_file(**arguments)
            
        else:
            raise ValueError(f"未知工具：{tool_call.name}")

        print(f"工具执行结果：{result}")

        # 记录：模型刚才要求调用了什么工具
        history.append(
            {
                "type": "function_call",
                "call_id": tool_call.call_id,
                "name": tool_call.name,
                "arguments": tool_call.arguments,
            }
        )

        # 记录：工具真正返回了什么结果
        history.append(
            {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": str(result),
            }
        )

        # 没有 return
        # 所以 while 会进入下一轮