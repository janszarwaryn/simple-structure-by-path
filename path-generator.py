import os
import wx
import wx.lib.agw.hyperlink as hl

def generate_directory_structure_file(path, prefix="", depth=0, max_depth=None, start=""):
    tree = ""

    if max_depth is not None and depth > max_depth:
        return tree

    try:
        items = os.listdir(path)
    except Exception as e:
        return f"Nie można odczytać zawartości katalogu {path}: {e}"

    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            tree += f"{prefix}├─F─ {start}{item}\n"  # Dodanie prefiksu "start" do linii dla plików
        elif os.path.isdir(item_path):
            tree += f"{prefix}├── {item}\n"
            tree += generate_directory_structure_file(item_path, prefix + "│   ", depth + 1, max_depth, start)

    return tree

def generate_structure(event):
    input_path = input_path_entry.GetValue()

    if not os.path.isdir(input_path):
        wx.MessageBox("Podana ścieżka jest nieprawidłowa", "Błąd", wx.OK | wx.ICON_ERROR)
        return

    try:
        max_depth = int(depth_entry.GetValue())
        if max_depth < 0:
            wx.MessageBox("Głębokość musi być nieujemna", "Błąd", wx.OK | wx.ICON_ERROR)
            return
    except ValueError:
        wx.MessageBox("Głębokość musi być liczbą całkowitą", "Błąd", wx.OK | wx.ICON_ERROR)
        return

    if max_depth == 0:
        max_depth = None

    tree = f"{os.path.basename(input_path)}\n"  # Show the root directory
    tree += generate_directory_structure_file(input_path, max_depth=max_depth, start="start")

    if same_location_check.GetValue():
        output_path = os.path.join(os.getcwd(), "struktura.txt")
        output_path_entry.SetValue(output_path)
        browse_output_button.Disable()
    else:
        output_path = output_path_entry.GetValue()
        if not output_path:
            wx.MessageBox("Podana ścieżka zapisu jest pusta", "Błąd", wx.OK | wx.ICON_ERROR)
            return
        browse_output_button.Enable()

    try:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(tree)
        wx.MessageBox(f"Zapisano strukturę drzewa do pliku {output_path}", "Sukces", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Nie można zapisać struktury drzewa do pliku {output_path}: {e}", "Błąd", wx.OK | wx.ICON_ERROR)

def browse_input_path(event):
    input_path_dialog = wx.DirDialog(None, "Wybierz ścieżkę")
    if input_path_dialog.ShowModal() == wx.ID_OK:
        input_path_entry.SetValue(input_path_dialog.GetPath())
    input_path_dialog.Destroy()

def browse_output_path(event):
    output_path_dialog = wx.FileDialog(None, "Wybierz ścieżkę zapisu", wildcard="Pliki tekstowe (*.txt)|*.txt",
                                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    if output_path_dialog.ShowModal() == wx.ID_OK:
        output_path_entry.SetValue(output_path_dialog.GetPath())
    output_path_dialog.Destroy()

app = wx.App()
frame = wx.Frame(None, title="Generowanie struktury katalogu", size=(500, 400))  # Zmiana rozmiaru okna

screen_width, screen_height = wx.GetDisplaySize()
x = (screen_width - 500) // 2  # Wycentrowanie na ekranie
y = (screen_height - 400) // 2
frame.SetPosition((x, y))

panel = wx.Panel(frame)
vbox = wx.BoxSizer(wx.VERTICAL)

# Ścieżka generacji struktury
input_path_label = wx.StaticText(panel, label="Ścieżka generacji struktury:")
vbox.Add(input_path_label, 0, wx.ALL, 5)

input_path_panel = wx.Panel(panel)
input_path_hbox = wx.BoxSizer(wx.HORIZONTAL)

input_path_entry = wx.TextCtrl(input_path_panel)
input_path_hbox.Add(input_path_entry, 1, wx.EXPAND)

browse_input_button = wx.Button(input_path_panel, label="Przeglądaj")
browse_input_button.Bind(wx.EVT_BUTTON, browse_input_path)
input_path_hbox.Add(browse_input_button, 0, wx.LEFT, 5)

input_path_panel.SetSizer(input_path_hbox)
vbox.Add(input_path_panel, 0, wx.EXPAND | wx.ALL, 5)

# Ścieżka zapisu
output_path_label = wx.StaticText(panel, label="Ścieżka zapisu:")
vbox.Add(output_path_label, 0, wx.ALL, 5)

output_path_panel = wx.Panel(panel)
output_path_hbox = wx.BoxSizer(wx.HORIZONTAL)

output_path_entry = wx.TextCtrl(output_path_panel)
output_path_hbox.Add(output_path_entry, 1, wx.EXPAND)

browse_output_button = wx.Button(output_path_panel, label="Przeglądaj")
browse_output_button.Bind(wx.EVT_BUTTON, browse_output_path)
output_path_hbox.Add(browse_output_button, 0, wx.LEFT, 5)

output_path_panel.SetSizer(output_path_hbox)
vbox.Add(output_path_panel, 0, wx.EXPAND | wx.ALL, 5)

# Zapis w tej samej lokalizacji (domyślnie zaznaczone)
same_location_check = wx.CheckBox(panel, label="Zapisz w tej samej lokalizacji")
same_location_check.SetValue(True)  # Ustawienie domyślnie zaznaczonej opcji
vbox.Add(same_location_check, 0, wx.ALL, 5)

# Głębokość
depth_label = wx.StaticText(panel, label="Głębokość:")
vbox.Add(depth_label, 0, wx.ALL, 5)

depth_entry = wx.TextCtrl(panel, value="0")  # Default depth value
vbox.Add(depth_entry, 0, wx.EXPAND | wx.ALL, 5)

# Przycisk "Generuj strukturę"
generate_button = wx.Button(panel, label="Generuj strukturę")
generate_button.Bind(wx.EVT_BUTTON, generate_structure)
vbox.Add(generate_button, 0, wx.ALIGN_CENTER | wx.ALL, 10)

panel.SetSizer(vbox)
frame.Show()
app.MainLoop()
