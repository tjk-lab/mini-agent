from agent import run_agent


print("MiniAgent 已启动。")
print("输入 exit 可以退出程序。")


while True:
    # input() 会停在这里，等待你在终端输入内容
    user_input = input("\n你：")

    # 如果用户输入 exit，就退出整个程序
    if user_input.strip().lower() == "exit":
        print("MiniAgent 已退出。")
        break

    # 把这一条任务交给 Agent
    answer = run_agent(user_input)

    # 输出 Agent 最终回答
    print("\nAgent：")
    print(answer)