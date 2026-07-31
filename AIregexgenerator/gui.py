import tkinter as tk
from tkinter import messagebox
from regex_generator import generate_regex
from regex_explainer import explain_regex
from regex_tester import test_regex

# ---------------- WINDOW ---------------- #

root = tk.Tk()
root.title("🤖 AI Regex Generator")
root.geometry("900x750")
root.configure(bg="#F4F6F9")

regex_var = tk.StringVar()

# ---------------- FUNCTIONS ---------------- #

def generate():

    description = desc_entry.get("1.0", tk.END).strip()

    if description == "":
        messagebox.showwarning("Warning", "Please enter a regex description.")
        return

    status.config(text="Generating...", fg="blue")
    root.update()

    try:
        print("Generating regex...")

        regex = generate_regex(description)

        print("Generated:", regex)

        regex_var.set(regex)

        explanation = explain_regex(regex)

        explain_box.config(state="normal")
        explain_box.delete("1.0", tk.END)
        explain_box.insert(tk.END, explanation)
        explain_box.config(state="disabled")

        status.config(text="Regex generated successfully ✔", fg="green")

    except Exception as e:

        print(e)

        status.config(text="Generation Failed", fg="red")

        messagebox.showerror(
            "Error",
            str(e)
        )


def test():

    regex = regex_var.get().strip()

    text = test_entry.get().strip()

    if regex == "":
        messagebox.showwarning("Warning", "Generate a regex first.")
        return

    result = test_regex(regex, text)

    result_label.config(text=result)


def copy_regex():

    regex = regex_var.get()

    if regex == "":
        return

    root.clipboard_clear()
    root.clipboard_append(regex)

    messagebox.showinfo("Copied", "Regex copied successfully.")


def clear():

    desc_entry.delete("1.0", tk.END)

    regex_var.set("")

    explain_box.config(state="normal")
    explain_box.delete("1.0", tk.END)
    explain_box.config(state="disabled")

    test_entry.delete(0, tk.END)

    result_label.config(text="")

    status.config(text="")


# ---------------- TITLE ---------------- #

title = tk.Label(
    root,
    text="🤖 AI REGEX GENERATOR",
    font=("Segoe UI", 24, "bold"),
    bg="#F4F6F9",
    fg="#1E3A8A"
)

title.pack(pady=20)

# ---------------- DESCRIPTION ---------------- #

tk.Label(
    root,
    text="Regex Description",
    font=("Segoe UI", 12, "bold"),
    bg="#F4F6F9"
).pack()

desc_entry = tk.Text(
    root,
    width=70,
    height=5,
    font=("Segoe UI", 11)
)

desc_entry.pack(pady=10)

# ---------------- GENERATE ---------------- #

generate_btn = tk.Button(
    root,
    text="Generate Regex",
    font=("Segoe UI", 12, "bold"),
    bg="#2563EB",
    fg="white",
    padx=20,
    pady=5,
    command=generate
)

generate_btn.pack()

status = tk.Label(
    root,
    text="",
    font=("Segoe UI", 10),
    bg="#F4F6F9"
)

status.pack(pady=5)

# ---------------- REGEX ---------------- #

tk.Label(
    root,
    text="Generated Regex",
    font=("Segoe UI", 12, "bold"),
    bg="#F4F6F9"
).pack()

regex_entry = tk.Entry(
    root,
    textvariable=regex_var,
    width=80,
    font=("Consolas", 12)
)

regex_entry.pack(pady=10)

# ---------------- EXPLANATION ---------------- #

tk.Label(
    root,
    text="Explanation",
    font=("Segoe UI", 12, "bold"),
    bg="#F4F6F9"
).pack()

explain_box = tk.Text(
    root,
    width=80,
    height=10,
    font=("Segoe UI", 11),
    state="disabled"
)

explain_box.pack(pady=10)

# ---------------- TEST ---------------- #

tk.Label(
    root,
    text="Test String",
    font=("Segoe UI", 12, "bold"),
    bg="#F4F6F9"
).pack()

test_entry = tk.Entry(
    root,
    width=60,
    font=("Segoe UI", 11)
)

test_entry.pack(pady=10)

tk.Button(
    root,
    text="Test Regex",
    font=("Segoe UI", 12, "bold"),
    bg="#16A34A",
    fg="white",
    command=test
).pack(pady=10)

# ---------------- RESULT ---------------- #

result_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 14, "bold"),
    bg="#F4F6F9",
    fg="green"
)

result_label.pack()

# ---------------- BUTTONS ---------------- #

frame = tk.Frame(root, bg="#F4F6F9")

frame.pack(pady=20)

tk.Button(
    frame,
    text="Copy Regex",
    width=15,
    command=copy_regex
).grid(row=0, column=0, padx=10)

tk.Button(
    frame,
    text="Clear",
    width=15,
    command=clear
).grid(row=0, column=1, padx=10)

tk.Button(
    frame,
    text="Exit",
    width=15,
    command=root.destroy
).grid(row=0, column=2, padx=10)

root.mainloop()