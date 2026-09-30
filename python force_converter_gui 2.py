import math
import tkinter as tk
from tkinter import ttk


def convert_force():
    try:
        value = float(value_entry.get().strip())
        unit = unit_box.get().strip().lower()

        if not math.isfinite(value) or value < 0:
            raise ValueError

        if unit == "kn":
            kn = value
        elif unit == "n":
            kn = value / 1000
        elif unit == "kgf":
            kn = value * 9.80665 / 1000
        else:
            raise ValueError

        newton = kn * 1000
        kgf = newton / 9.80665

        result = f"{newton:,.2f} N\n{kgf:,.2f} kgf"
        result_label.config(text=result, foreground="#7CFC00")

        history_list.insert(
            tk.END,
            f"{value:g} {unit} → {newton:,.2f} N, {kgf:,.2f} kgf"
        )

    except ValueError:
        result_label.config(
            text="잘못된 입력",
            foreground="#FF6B6B"
        )


def add_number(number):
    value_entry.insert(tk.END, number)


def delete_last():
    current = value_entry.get()
    value_entry.delete(0, tk.END)
    value_entry.insert(0, current[:-1])


def clear_input():
    value_entry.delete(0, tk.END)
    result_label.config(
        text="변환 결과",
        foreground="#7CFC00"
    )
    value_entry.focus()


window = tk.Tk()
window.title("공학용 힘 단위 변환기")
window.geometry("620x650")
window.configure(bg="#202124")
window.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Calc.TButton",
    font=("맑은 고딕", 12, "bold"),
    padding=12,
    background="#3C4043",
    foreground="white"
)
style.map(
    "Calc.TButton",
    background=[("active", "#5F6368")]
)

tk.Label(
    window,
    text="ENGINEERING FORCE CALCULATOR",
    font=("맑은 고딕", 17, "bold"),
    bg="#202124",
    fg="#00BFFF"
).pack(pady=(18, 10))

display_frame = tk.Frame(window, bg="#111111", bd=3, relief="sunken")
display_frame.pack(padx=25, fill="x")

value_entry = tk.Entry(
    display_frame,
    font=("Consolas", 24, "bold"),
    justify="right",
    bg="#111111",
    fg="#7CFC00",
    insertbackground="white",
    bd=0
)
value_entry.pack(fill="x", padx=12, pady=12)

unit_frame = tk.Frame(window, bg="#202124")
unit_frame.pack(pady=12)

tk.Label(
    unit_frame,
    text="입력 단위",
    font=("맑은 고딕", 11, "bold"),
    bg="#202124",
    fg="white"
).grid(row=0, column=0, padx=8)

unit_box = ttk.Combobox(
    unit_frame,
    values=("kN", "N", "kgf"),
    width=10,
    font=("맑은 고딕", 11)
)
unit_box.set("kN")
unit_box.grid(row=0, column=1, padx=8)

keypad = tk.Frame(window, bg="#202124")
keypad.pack(pady=5)

buttons = [
    ("7", 0, 0), ("8", 0, 1), ("9", 0, 2),
    ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
    ("1", 2, 0), ("2", 2, 1), ("3", 2, 2),
    ("0", 3, 0), (".", 3, 1), ("←", 3, 2),
]

for text, row, column in buttons:
    command = delete_last if text == "←" else lambda value=text: add_number(value)
    ttk.Button(
        keypad,
        text=text,
        command=command,
        style="Calc.TButton",
        width=8
    ).grid(row=row, column=column, padx=4, pady=4)

ttk.Button(
    keypad,
    text="C",
    command=clear_input,
    style="Calc.TButton",
    width=8
).grid(row=4, column=0, padx=4, pady=4)

ttk.Button(
    keypad,
    text="변환",
    command=convert_force,
    style="Calc.TButton",
    width=18
).grid(row=4, column=1, columnspan=2, padx=4, pady=4)

result_label = tk.Label(
    window,
    text="변환 결과",
    font=("Consolas", 18, "bold"),
    bg="#111111",
    fg="#7CFC00",
    width=28,
    height=2
)
result_label.pack(pady=15)

tk.Label(
    window,
    text="변환 기록",
    font=("맑은 고딕", 12, "bold"),
    bg="#202124",
    fg="white"
).pack()

history_list = tk.Listbox(
    window,
    width=65,
    height=7,
    bg="#111111",
    fg="white",
    selectbackground="#3C4043",
    font=("맑은 고딕", 10)
)
history_list.pack(padx=20, pady=8)

value_entry.focus()
window.mainloop()