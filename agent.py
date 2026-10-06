import json

from llm import call_llm
from logger import get_logger
from tools.registry import TOOL_FUNCTIONS

logger = get_logger("agent")


def run_agent(user_input: str) -> str:
    """
    运行 Agent：
    1. 把用户任务发送给模型
    2. 模型决定是否调用工具
    3. 执行工具
    4. 把工具结果返回给模型
    5. 循环直到任务完成
    """

    history = [
        {
            "role": "user",
            "content": user_input,
        }
    ]

    step = 0

    while True:
        step += 1

        logger.info("Agent 第 %s 轮开始", step)

        if step > 10:
            logger.error("Agent 超过最大执行轮数")
            raise RuntimeError("Agent 超过最大执行轮数")

        response = call_llm(history)

        tool_call = None

        for item in response.output:
            if item.type == "function_call":
                tool_call = item
                break

        if tool_call is None:
            logger.info("Agent 任务完成")
            return response.output_text

        logger.info("模型决定调用工具：%s", tool_call.name)
        logger.info("模型提供参数：%s", tool_call.arguments)

        arguments = json.loads(tool_call.arguments)

        try:
            if tool_call.name not in TOOL_FUNCTIONS:
                raise ValueError(f"未知工具：{tool_call.name}")

            tool_function = TOOL_FUNCTIONS[tool_call.name]

            result = tool_function(**arguments)

            tool_output = str(result)

            logger.info("工具执行成功：%s", tool_output)

        except Exception as e:
            tool_output = f"工具执行失败：{type(e).__name__}: {e}"

            logger.error(tool_output)

        history.append(
            {
                "type": "function_call",
                "call_id": tool_call.call_id,
                "name": tool_call.name,
                "arguments": tool_call.arguments,
            }
        )

        history.append(
            {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": tool_output,
            }
        )
