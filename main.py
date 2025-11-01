"""
Time Waster Tracker - 认真地什么都不做。
"""

import tkinter as tk
from tkinter import messagebox
import time, json, os, random
from datetime import datetime

DATA_FILE = "waste_data.json"

quotes = [
    "你不是在浪费时间，只是在体验存在的空虚。",
    "时间被浪费了，但浪费的时间也是时间。",
    "别担心，宇宙在扩张，你也没什么好赶的。",
    "拖延是一种生活方式。",
    "你离成佛只差再浪费五分钟。",
    "今日不做的事，明日也不一定会做。",
]

levels = [
    (0, "浪费入门者"),
    (60, "时间自由主义者"),
    (600, "拖延大师"),
    (3600, "时间哲学家"),
    (86400, "熵之化身"),
]

def resource_path(relative_path):
    # 获取数据文件的正确路径
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_data():
    # 安全加载数据文件，若不存在或损坏则创建新文件
    if not os.path.exists(DATA_FILE):
        # 文件不存在：创建默认数据
        data = {"total_seconds": 0, "history": []}
        save_data(data)
        return data

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 验证关键字段是否存在
        if not isinstance(data, dict) or "total_seconds" not in data:
            raise ValueError("数据文件结构异常")
        return data

    except (json.JSONDecodeError, ValueError, OSError) as e:
        print(f"[警告] 数据文件损坏或无法读取：{e}")
        # 自动重建
        data = {"total_seconds": 0, "history": []}
        save_data(data)
        return data

def save_data(data):
    # 安全保存数据
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_level(total_seconds):
    for sec, name in reversed(levels):
        if total_seconds >= sec:
            return name
    return "未知生命体"

class TimeWasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🕒 时间浪费跟踪器")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.configure(bg="#20232a")

        self.data = load_data()
        self.running = False
        self.start_time = None

        # 标题
        self.title_label = tk.Label(root, text="时间浪费跟踪器", fg="#61dafb", bg="#20232a",
                                    font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=10)

        # 计时标签
        self.session_label = tk.Label(root, text="本次已浪费: 0 秒", fg="white", bg="#20232a", font=("Consolas", 14))
        self.session_label.pack(pady=5)

        self.total_label = tk.Label(root, text=f"累计浪费: {self.data['total_seconds']} 秒 ({get_level(self.data['total_seconds'])})",
                                    fg="#f0db4f", bg="#20232a", font=("Consolas", 12))
        self.total_label.pack(pady=5)

        # 废话输出
        self.quote_label = tk.Label(root, text=random.choice(quotes), wraplength=340, justify="center",
                                    fg="#999", bg="#20232a", font=("KaiTi", 11))
        self.quote_label.pack(pady=20)

        # 按钮
        self.start_button = tk.Button(root, text="开始浪费", command=self.toggle,
                                      bg="#61dafb", fg="black", font=("Helvetica", 12, "bold"), width=15)
        self.start_button.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # 绑定焦点事件
        self.root.bind("<FocusIn>", self.on_focus_in)
        self.root.bind("<FocusOut>", self.on_focus_out)
        
        # 兼容性绑定
        self.root.bind("<Activate>", self.on_focus_in)
        self.root.bind("<Deactivate>", self.on_focus_out)

        self.quote_label = tk.Label(
            root,
            text=random.choice(quotes),
            wraplength=340,
            justify="center",
            fg="#999",
            bg="#20232a",
            font=("KaiTi", 11)
        )

    def toggle(self):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.start_button.config(text="暂停浪费", bg="#f66")
            self.update_timer()
        else:
            self.pause()

    def update_timer(self):
        if not self.running:
            return
        elapsed = int(time.time() - self.start_time)
        total = self.data['total_seconds'] + elapsed
        self.session_label.config(text=f"本次已浪费: {elapsed} 秒")
        self.total_label.config(text=f"累计浪费: {total} 秒 ({get_level(total)})")
        if elapsed % 60 == 0 and elapsed > 0:
            self.quote_label.config(text=random.choice(quotes))
        self.root.after(1000, self.update_timer)

    def pause(self):
        if not self.running:
            return
        self.running = False
        wasted = int(time.time() - self.start_time)
        self.data['total_seconds'] += wasted
        self.data['history'].append({"time": datetime.now().isoformat(), "session": wasted})
        save_data(self.data)

        # 更新界面：锁定最终数值
        self.session_label.config(text=f"本次已浪费: {wasted} 秒")
        self.total_label.config(
            text=f"累计浪费: {self.data['total_seconds']} 秒 ({get_level(self.data['total_seconds'])})"
        )
        self.start_button.config(text="继续浪费", bg="#61dafb")
        self.quote_label.config(text=random.choice(quotes))

        # 重置计时起点，防止继续累加
        self.start_time = None

    def on_focus_out(self, event=None):
        # 延迟一点执行，避免与其他焦点切换导致的“抖动”
        self.root.after(50, self._handle_focus_out)

    def _handle_focus_out(self):
        # 仅在窗口真正失去“窗口焦点”时生效（兼容性检查）
        # focus_displayof() 为 None 时，多半表示窗口没焦点
        if self.root.focus_displayof() is not None:
            # 可能只是控件间切换焦点（不是切出应用），不处理
            return
        if self.running:
            self.pause()
        # 锁定提示语（红色警示）
        self._lock_quote("你分心了，浪费被中断。请专注地什么都不做。", color="#f66", lock_seconds=8)

    def on_focus_in(self, event=None):
        # 窗口重新获得焦点
        if not self.running:
            self.quote_label.config(
                text="欢迎回来。继续你未完成的虚无。", fg="#999"
            )

    def _handle_focus_in(self):
        # 当窗口回到前台时给出提示，但不自动继续计时
        self._lock_quote("欢迎回来。继续你未完成的虚无。", color="#999", lock_seconds=6)

    def _lock_quote(self, text, color="#999", lock_seconds=5):
        # 设置 quote 并在短时间内防止被其它更新覆盖
        # 取消之前可能的解锁计时器（如果有）
        try:
            self.root.after_cancel(self._quote_unlock_id)
        except Exception:
            pass

        # 立即设置
        self.quote_label.configure(text=text, fg=color)

        # 在 lock_seconds 后解除锁定（允许正常轮换）
        def _unlock():
            # 随机恢复一句废话（仅当不在运行计时且没有别的需求）
            if not self.running:
                self.quote_label.configure(text=random.choice(quotes), fg="#999")

        self._quote_unlock_id = self.root.after(int(lock_seconds * 1000), _unlock)


    def on_close(self):
        if self.running:
            self.pause()
        messagebox.showinfo("时间浪费跟踪器", "浪费得不错，浪费进度将自动保存，下次可继续浪费。")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeWasterApp(root)
    root.mainloop()
