import os
import sys
import re
import subprocess

# Гарантуємо, що Python бачить папку app як пакет на будь-якій ОС
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.constants.routes import generate_readme_table

def generate_directory_tree(dir_path: str, prefix: str = "") -> list:
    """Рекурсивно генерує текстове дерево папок і файлів."""
    lines = []
    # Папки та розширення, які НЕ треба показувати в README
    ignore_list = ["__pycache__", ".git", ".pytest_cache", ".venv", "poetry.lock"]
    
    try:
        items = sorted(os.listdir(dir_path))
    except FileNotFoundError:
        return lines

    # Фільтруємо ігноровані елементи
    items = [item for item in items if item not in ignore_list and not item.endswith(".pyc")]
    
    for i, item in enumerate(items):
        is_last = (i == len(items) - 1)
        connector = "└── " if is_last else "├── "
        full_path = os.path.join(dir_path, item)
        
        # Додаємо косий слеш для папок, щоб візуально їх відрізняти
        display_name = f"{item}/" if os.path.isdir(full_path) else item
        lines.append(f"{prefix}{connector}{display_name}")
        
        if os.path.isdir(full_path):
            indent = "    " if is_last else "│   "
            lines.extend(generate_directory_tree(full_path, prefix + indent))
            
    return lines

def update_readme():
    README_PATH = "README.md"
    
    if not os.path.exists(README_PATH):
        print(f"Error: {README_PATH} not found.")
        sys.exit(1)

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # --- 1. ОНОВЛЕННЯ ТАБЛИЦІ ЕНДПОІНТІВ ---
    routes_table = generate_readme_table()
    routes_pattern = r"(<!-- START_ROUTES_TABLE -->)(.*?)(<!-- END_ROUTES_TABLE -->)"
    
    if re.search(routes_pattern, content, flags=re.DOTALL):
        replacement = f"\\1\n\n{routes_table}\n\n\\3"
        content = re.sub(routes_pattern, replacement, content, flags=re.DOTALL)

    # --- 2. ОНОВЛЕННЯ ДЕРЕВА ПРОЄКТУ ---
    # Збираємо дерево для папки проекту (включаючи корінь)
    tree_lines = ["app/"] + generate_directory_tree("app")
    
    # Також додамо основні файли з кореня, якщо вони є
    for root_file in ["main.py", "update_docs.py", ".env", "pyproject.toml"]:
        if os.path.exists(root_file):
            tree_lines.append(f"├── {root_file}" if root_file != "pyproject.toml" else f"└── {root_file}")
            
    # Загортаємо дерево в блок коду Markdown для гарного моноширинного шрифту
    tree_markdown = "```tree\n" + "\n".join(tree_lines) + "\n```"
    tree_pattern = r"(<!-- START_STRUCTURE_TREE -->)(.*?)(<!-- END_STRUCTURE_TREE -->)"
    
    if re.search(tree_pattern, content, flags=re.DOTALL):
        replacement = f"\\1\n\n{tree_markdown}\n\n\\3"
        content = re.sub(tree_pattern, replacement, content, flags=re.DOTALL)
    else:
        print("Warning: Markers <!-- START_STRUCTURE_TREE --> not found in README.md")

    # --- 3. ОНОВЛЕННЯ .env ФАЙЛУ  
    env_example_text = get_env_example_text()
    env_pattern = r"(<!-- START_ENV_EXAMPLE -->)(.*?)(<!-- END_ENV_EXAMPLE -->)"
       
    if re.search(env_pattern, content, flags=re.DOTALL):
        replacement = f"\\1\n\n```env\n{env_example_text}\n```\n\n\\3"
        content = re.sub(env_pattern, replacement, content, flags=re.DOTALL)
    
    # --- 4. ЗАПИС У ФАЙЛ ТА СТЕЙДЖИНГ ---
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)
        
    subprocess.run(["git", "add", README_PATH], check=True)
    print("README.md updated successfully with tree and routes!")
    

def get_env_example_text() -> str:
    """
    Читає .env і повертає його точну копію для README у форматі розмітки .env.
    """
    env_path = '.env'
    
    if not os.path.exists(env_path):
        return f"# Помилка: Файл {env_path} не знайдено!"

    try:
        with open(env_path, 'rb') as f:
            raw_content = f.read()
            
        lines = raw_content.decode('utf-8').splitlines()
        example_lines = []
        
        inside_access_block = False

        for line in lines:
            line_stripped = line.strip()
            
            if line_stripped == '#START_ACCESS':
                inside_access_block = True
                example_lines.append(line)
                continue
            elif line_stripped == '#END_ACCESS':
                inside_access_block = False
                example_lines.append(line)
                continue
                
            # Якщо це будь-який коментар (починається з #) — копіюємо один в один
            if line_stripped.startswith('#'):
                example_lines.append(line)
                continue

            # Обробка розкоментованих змінних
            if '=' in line:
                if inside_access_block:
                    # Затираємо значення тільки всередині блоку доступу
                    idx = line.index('=')
                    key_part = line[:idx]
                    example_lines.append(f"{key_part}=")
                else:
                    # Поза блоком залишаємо все повністю заповненим
                    example_lines.append(line)
            else:
                # Порожні рядки
                example_lines.append(line)

        return '\n'.join(example_lines) + '\n'

    except Exception as e:
        return f"# Помилка під час обробки: {e}"
    

if __name__ == "__main__":
    update_readme()