from agent import run_agent


answer = run_agent(
    "请读取所有输入 txt 文件，总结它们的内容，并把总结写入 summary.txt。"
)

print("\nAgent 最终回答：")
print(answer)