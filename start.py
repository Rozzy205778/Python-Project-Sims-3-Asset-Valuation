import tkinter as tk
import classes.gems as gems

root = tk.Tk()
gems.Options(root).pack(side="top", fill="both", expand=True)
root.mainloop()