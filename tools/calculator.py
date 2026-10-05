def calculator(a: float, b: float, operator: str) -> float:
    """
    一个最简单的计算器工具。

    参数：
        a: 第一个数字
        b: 第二个数字
        operator: 运算符，目前支持 + - * /

    返回：
        计算结果
    """

    if operator == "+":
        return a + b

    if operator == "-":
        return a - b

    if operator == "*":
        return a * b

    if operator == "/":
        # 防止出现除以 0
        if b == 0:
            raise ValueError("不能除以 0")
        return a / b

    # 如果模型以后传了奇怪的运算符，我们明确报错
    raise ValueError(f"不支持的运算符: {operator}")
