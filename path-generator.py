import os
import tkinter as tk
from tkinter import filedialog, messagebox

def generate_directory_structure_file(path, prefix=""):
    tree = ""

    try:
        items = os.listdir(path)
    except Exception as e:
        return f"Nie można odczytać zawartości katalogu {path}: {e}"

    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            tree += f"{prefix}├── {item}\n"
        elif os.path.isdir(item_path):
            tree += f"{prefix}├── {item}\n"
            tree += generate_directory_structure_file(item_path, prefix + "│   ")

    return tree

def generate_structure():
    input_path = input_path_entry.get()

    if not os.path.isdir(input_path):
        messagebox.showerror("Błąd", "Podana ścieżka jest nieprawidłowa")
        return

    tree = generate_directory_structure_file(input_path)

    if same_location_var.get() == 1:
        output_path = os.path.join(os.getcwd(), "struktura.txt")
        output_path_entry.delete(0, tk.END)
        output_path_entry.insert(tk.END, output_path)
        browse_output_button.config(state=tk.DISABLED)
    else:
        output_path = output_path_entry.get()
        if not output_path:
            messagebox.showerror("Błąd", "Podana ścieżka zapisu jest pusta")
            return
        browse_output_button.config(state=tk.NORMAL)

    try:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(tree)
        messagebox.showinfo("Sukces", f"Zapisano strukturę drzewa do pliku {output_path}")
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie można zapisać struktury drzewa do pliku {output_path}: {e}")

root = tk.Tk()
root.title("Generowanie struktury katalogu")

window_width = 500
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

same_location_var = tk.IntVar(value=1)

# Wyśrodkowanie ścieżki generacji struktury
input_path_label = tk.Label(root, text="Ścieżka generacji struktury:")
input_path_label.pack()
input_path_frame = tk.Frame(root)
input_path_frame.pack()
input_path_entry = tk.Entry(input_path_frame)
input_path_entry.pack(side="left")

def browse_input_path():
    input_path = filedialog.askdirectory()
    if input_path:
        input_path_entry.delete(0, tk.END)
        input_path_entry.insert(tk.END, input_path)

browse_input_button = tk.Button(input_path_frame, text="Przeglądaj", command=browse_input_path)
browse_input_button.pack(side="left")

# Wyśrodkowanie ścieżki zapisu
output_path_label = tk.Label(root, text="Ścieżka zapisu:")
output_path_label.pack()
output_path_frame = tk.Frame(root)
output_path_frame.pack()
output_path_entry = tk.Entry(output_path_frame)
output_path_entry.pack(side="left")

def browse_output_path():
    output_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")))
    if output_path:
        same_location_var.set(0)
        output_path_entry.delete(0, tk.END)
        output_path_entry.insert(tk.END, output_path)

browse_output_button = tk.Button(output_path_frame, text="Przeglądaj", command=browse_output_path)
browse_output_button.pack(side="left")

same_location_checkbutton = tk.Checkbutton(root, text="Zapisz w tej samej lokalizacji", variable=same_location_var)
same_location_checkbutton.pack()

# Standardowy przycisk "Generuj strukturę"
generate_button = tk.Button(root, text="Generuj strukturę", command=generate_structure)
generate_button.pack()

root.mainloop()
