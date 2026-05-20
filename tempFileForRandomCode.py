from tkinter import *
from tkinter import ttk

root = Tk()

canvas = Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)

scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

for i in range(20):
    item = ttk.Frame(scrollable_frame, padding=10)

    ttk.Label(item, text=f"Item {i}").pack(side="left")
    ttk.Button(item, text="Open").pack(side="right")

    item.pack(fill="x", pady=5)

root.mainloop()