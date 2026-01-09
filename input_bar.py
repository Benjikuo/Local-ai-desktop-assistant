import tkinter as tk
from ollama_client import chat


# ================== 工具：畫圓角矩形 ==================
def round_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    points = [
        x1 + r,
        y1,
        x2 - r,
        y1,
        x2,
        y1,
        x2,
        y1 + r,
        x2,
        y2 - r,
        x2,
        y2,
        x2 - r,
        y2,
        x1 + r,
        y2,
        x1,
        y2,
        x1,
        y2 - r,
        x1,
        y1 + r,
        x1,
        y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


# ================== 回呼：送出給模型 ==================
def send_to_ai(event=None):
    user_input = user_text.get().strip()
    if not user_input:
        return

    output_text.set("AI 思考中…")
    win.update_idletasks()

    try:
        reply = chat(user_input)
        output_text.set(reply)
    except Exception as e:
        output_text.set(f"錯誤：{e}")

    user_text.set("")


# ================== 主視窗 ==================
win = tk.Tk()
win.title("AI")
win.geometry("560x180+680+900")
win.config(bg="#000000")
win.attributes("-alpha", 0.88)

# （如果你之後要無邊框可打開）
# win.overrideredirect(True)


# ================== 變數 ==================
user_text = tk.StringVar()
output_text = tk.StringVar(value="請輸入內容，按 Enter 或 ➔")


# ================== 圓角搜尋框（Canvas） ==================
canvas = tk.Canvas(win, width=440, height=50, bg="#000000", highlightthickness=0)
canvas.grid(row=0, column=0, padx=(12, 4), pady=12, sticky="w")

# 圓角背景
round_rect(canvas, 0, 0, 440, 50, r=18, fill="#2A2A2A", outline="")

# Entry（嵌入 Canvas）
entry = tk.Entry(
    win,
    textvariable=user_text,
    bg="#2A2A2A",
    fg="#ffffff",
    font=("微軟正黑體", 14, "bold"),
    insertbackground="#ffffff",
    bd=0,
    relief="flat",
)

canvas.create_window(18, 25, window=entry, anchor="w", width=360)

entry.bind("<Return>", send_to_ai)
entry.focus()


# ================== 送出按鈕 ==================
send_btn = tk.Button(
    win,
    text="➔",
    command=send_to_ai,
    bg="#000000",
    fg="#ffffff",
    font=("微軟正黑體", 18),
    bd=0,
    activebackground="#111111",
    cursor="hand2",
)
send_btn.grid(row=0, column=1, padx=(0, 12))


# ================== AI 回覆區 ==================
output = tk.Label(
    win,
    textvariable=output_text,
    wraplength=520,
    justify="left",
    bg="#000000",
    fg="#dddddd",
    font=("微軟正黑體", 11),
)
output.grid(row=1, column=0, columnspan=2, padx=14, pady=(6, 10), sticky="w")


win.mainloop()
