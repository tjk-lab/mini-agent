from types import SimpleNamespace

import agent


def test_agent_returns_direct_answer(monkeypatch):
    """
    测试：
    如果模型不调用工具，
    Agent 应该直接返回模型答案。
    """

    def fake_call_llm(history):
        return SimpleNamespace(
            output=[],
            output_text="你好，我是测试 Agent。",
        )

    monkeypatch.setattr(
        agent,
        "call_llm",
        fake_call_llm,
    )

    result = agent.run_agent("你好")

    assert result == "你好，我是测试 Agent。"


def test_agent_can_call_calculator(monkeypatch):
    """
    测试：
    模型先调用 calculator，
    Agent 执行工具后，
    再调用一次模型得到最终答案。
    """

    call_count = 0
    received_histories = []

    def fake_call_llm(history):
        nonlocal call_count

        call_count += 1

        # 保存当前 history，方便后面检查
        received_histories.append(
            list(history)
        )

        # 第一次调用模型：
        # 模型要求使用 calculator
        if call_count == 1:
            tool_call = SimpleNamespace(
                type="function_call",
                name="calculator",
                arguments='{"a": 10, "b": 20, "operator": "+"}',
                call_id="test-call-001",
            )

            return SimpleNamespace(
                output=[tool_call],
                output_text="",
            )

        # 第二次调用模型：
        # 模型看到工具结果以后给最终答案
        return SimpleNamespace(
            output=[],
            output_text="计算结果是 30。",
        )

    monkeypatch.setattr(
        agent,
        "call_llm",
        fake_call_llm,
    )

    result = agent.run_agent(
        "帮我计算 10 + 20"
    )

    assert result == "计算结果是 30。"

    # Agent 应该调用模型两次
    assert call_count == 2

    # 第二次调用模型时，
    # history 中应该已经包含工具执行结果
    second_history = received_histories[1]

    tool_outputs = [
        item
        for item in second_history
        if item.get("type")
        == "function_call_output"
    ]

    assert len(tool_outputs) == 1

    assert (
        tool_outputs[0]["output"]
        == "30"
    )


def test_agent_recovers_from_tool_error(monkeypatch):
    """
    测试：
    即使工具执行失败，
    Agent 也不能直接崩溃，
    而应该把错误信息返回给模型。
    """

    call_count = 0
    received_histories = []

    def fake_call_llm(history):
        nonlocal call_count

        call_count += 1

        received_histories.append(
            list(history)
        )

        # 第一次故意让模型做除以 0
        if call_count == 1:
            tool_call = SimpleNamespace(
                type="function_call",
                name="calculator",
                arguments='{"a": 10, "b": 0, "operator": "/"}',
                call_id="test-call-error",
            )

            return SimpleNamespace(
                output=[tool_call],
                output_text="",
            )

        # 第二次模型收到错误以后给用户解释
        return SimpleNamespace(
            output=[],
            output_text="不能除以 0。",
        )

    monkeypatch.setattr(
        agent,
        "call_llm",
        fake_call_llm,
    )

    result = agent.run_agent(
        "帮我计算 10 / 0"
    )

    assert result == "不能除以 0。"

    assert call_count == 2

    second_history = received_histories[1]

    tool_outputs = [
        item
        for item in second_history
        if item.get("type")
        == "function_call_output"
    ]

    assert len(tool_outputs) == 1

    assert "工具执行失败" in (
        tool_outputs[0]["output"]
    )

    assert "ValueError" in (
        tool_outputs[0]["output"]
    )