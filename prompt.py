from memory import memory


def build_messages(user_input):
    messages = []

    if memory["persona"]:
        messages.append({"role": "system", "content": memory["persona"]})

    if memory["summary"]:
        messages.append(
            {"role": "system", "content": f"以下是先前對話摘要：{memory['summary']}"}
        )

    messages.extend(memory["recent"])

    messages.append({"role": "user", "content": user_input})

    return messages
