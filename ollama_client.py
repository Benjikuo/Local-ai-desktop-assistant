import ollama
from prompt import build_messages


def chat(user_input, model="qwen2.5:7b-instruct"):
    messages = build_messages(user_input)

    response = ollama.chat(
        model=model,
        messages=messages,
    )

    # 👉 更新短期記憶（可先保留 5 筆）
    from memory import memory

    memory["recent"].append({"role": "user", "content": user_input})
    memory["recent"].append(
        {"role": "assistant", "content": response["message"]["content"]}
    )
    memory["recent"] = memory["recent"][-10:]

    return response["message"]["content"]
