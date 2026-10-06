import json

from llm import call_llm
from tools.calculator import calculator
from tools.file_tools import list_files, read_file, write_file


def run_agent(user_input: str) -> str:
    """
    运行一个最简单的循环 Agent。

    工作流程：
    1. 接收用户任务
    2. 把任务交给 DeepSeek
    3. 如果 DeepSeek 想调用工具，就执行工具
    4. 把工具结果记录下来，再交给 DeepSeek
    5. 重复以上过程
    6. 直到 DeepSeek 不再调用工具，返回最终答案
    """

    # history 可以理解成 Agent 的“任务记录本”
    # 一开始只有用户输入的问题
    history = [
        {
            "role": "user",
            "content": user_input,
        }
    ]

    # 记录当前已经执行了多少轮
    step = 0

    while True:
        # 每进入一次循环，轮数 +1
        step += 1

        print(f"\n===== Agent 第 {step} 轮 =====")

        # 防止 Agent 无限循环，一直消耗 API
        if step > 10:
            raise RuntimeError("Agent 超过最大执行轮数")

        # 把当前完整的 history 发给 DeepSeek
        # DeepSeek 根据已有信息决定下一步做什么
        response = call_llm(history)

        # 默认认为这一轮没有工具调用
        tool_call = None

        # DeepSeek 一次可能返回多个对象
        # 我们逐个检查有没有 function_call
        for item in response.output:
            if item.type == "function_call":
                tool_call = item
                break

        # 如果没发现工具调用
        # 说明 DeepSeek 认为任务已经完成
        if tool_call is None:
            return response.output_text

        print(f"模型决定调用工具：{tool_call.name}")
        print(f"模型提供参数：{tool_call.arguments}")

        # DeepSeek 返回的 arguments 是 JSON 字符串
        # 转换成 Python 可以使用的数据
        arguments = json.loads(tool_call.arguments)

        # -----------------------------
        # 真正执行 Python 工具
        # -----------------------------

        try:
            # 根据模型选择的工具，调用对应的 Python 函数
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

            # 工具执行成功
            tool_output = str(result)

            print(f"工具执行结果：{tool_output}")

        except Exception as e:
            # 工具执行失败时：
            # 不让整个 Agent 程序直接崩掉
            #
            # 而是把错误信息保存下来，
            # 下一轮重新交给 DeepSeek。
            tool_output = f"工具执行失败：{type(e).__name__}: {e}"

            print(tool_output)

        # -----------------------------
        # 把这一轮发生的事情加入 history
        # -----------------------------

        # 记录：
        # “DeepSeek 刚才调用了什么工具”
        history.append(
            {
                "type": "function_call",
                "call_id": tool_call.call_id,
                "name": tool_call.name,
                "arguments": tool_call.arguments,
            }
        )

        # 记录：
        # “工具真正返回了什么”
        #
        # 成功：
        #   tool_output = 正常结果
        #
        # 失败：
        #   tool_output = 错误信息
        history.append(
            {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": tool_output,
            }
        )

        # 注意：
        # 这里没有 return
        #
        # 所以程序会重新回到 while True 顶部
        # DeepSeek 会看到更新后的 history，
        # 然后决定下一步怎么办。
