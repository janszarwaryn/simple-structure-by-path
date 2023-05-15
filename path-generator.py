import os

def generate_directory_structure_file(path, prefix=""):
    tree = ""

    # Próbuj odczytać zawartość katalogu
    try:
        items = os.listdir(path)
    except Exception as e:
        return f"Nie można odczytać zawartości katalogu {path}: {e}"

    # Dodaj pliki i podkatalogi do drzewa
    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            tree += f"{prefix}├── {item}\n"
        elif os.path.isdir(item_path):
            tree += f"{prefix}├── {item}\n"
            tree += generate_directory_structure_file(item_path, prefix + "│   ")

    return tree

# Wprowadź ścieżkę głównego katalogu, który chcesz sprawdzić
main_directory = r"C:\Users\siara\Downloads\www\vue3-node-app\src"

# Generuj strukturę drzewa
tree = generate_directory_structure_file(main_directory)

# Wydrukuj strukturę drzewa
print(tree)

# Próbuj zapisać strukturę drzewa do pliku
try:
    output_file = r"C:\Users\siara\Downloads\struktura_katalogu.txt"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(tree)
    print(f"Zapisano strukturę drzewa do pliku {output_file}")
except Exception as e:
    print(f"Nie można zapisać struktury drzewa do pliku {output_file}: {e}")
