import tkinter as tk
import subprocess
import threading


class CmdConsole:
    def __init__(self):
        self.process = subprocess.Popen(
            ["cmd"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=None,  # 或指定路徑
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

        threading.Thread(target=self.read_output, daemon=True).start()

    def send(self, command):
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()

    def read_output(self):
        for line in self.process.stdout:
            output_box.insert(tk.END, line)
            output_box.see(tk.END)


def on_enter(event=None):
    cmd = entry.get()
    output_box.insert(tk.END, f"> {cmd}\n")
    console.send(cmd)
    entry.delete(0, tk.END)


root = tk.Tk()
root.title("Tkinter CMD 對話框")

entry = tk.Entry(root, width=60)
entry.pack(padx=10, pady=5)
entry.bind("<Return>", on_enter)

output_box = tk.Text(root, height=20, width=80)
output_box.pack(padx=10, pady=10)

console = CmdConsole()

root.mainloop()
