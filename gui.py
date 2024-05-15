import tkinter as tk

root = tk.Tk()
root.title('Simple GUI')
root.geometry('200x100')

count = 0

def incrementCount():
    global count
    count += 1
    label.config(text=f"Count: {count}")

label = tk.Label(root, text="Count: 0")
label.pack()

button = tk.Button(root, text="Increment", command=incrementCount)
button.pack()

root.mainloop()