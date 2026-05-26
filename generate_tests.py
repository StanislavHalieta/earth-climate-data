import os
import sys

def create_test_file(source_path):
    if "__init__.py" in source_path or source_path.startswith("tests/") or "handler.py" in source_path or "session.py" in source_path:
        return
    if not source_path.endswith(".py"):
        return

    # Нормалізуємо відображення слешів
    clean_path = source_path.replace("\\", "/")
    filename = os.path.basename(clean_path)

    # Якщо це загальні назви (handler або session), збираємо для них точний шлях
    if filename in ["handler.py", "session.py"]:
        if clean_path.startswith("app/"):
            clean_path = clean_path[4:]
        name_snake_case = clean_path.replace(".py", "").replace("/", "_")
        test_filename = f"test_{name_snake_case}.py"
    else:
        # Для парсерів та утиліт залишаємо просту, чисту назву файлу
        test_filename = f"test_{filename}"

    test_path = os.path.join("tests", test_filename)

    # Захист від перезапису існуючих файлів
    if os.path.exists(test_path):
        return

    os.makedirs("tests", exist_ok=True)

    module_path = source_path.replace(".py", "").replace("/", ".").replace("\\", ".")
    
    template = f"""import pytest
# Автоматично згенерований шаблон для {source_path}
# from {module_path} import ваші_функції

def test_placeholder():
    \"\"\"Тимчасовий тест-заглушка. Замініть його на реальну перевірку.\"\"\"
    assert True
"""

    with open(test_path, "w", encoding="utf-8") as f:
        f.write(template)
    print(f"[CREATED] {test_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        files_to_check = sys.argv[1:]
        for file_path in files_to_check:
            if os.path.exists(file_path):
                create_test_file(file_path)
    else:
        print("Scanning app/ for new files...")
        for root, dirs, files in os.walk("app"):
            for file in files:
                full_path = os.path.join(root, file)
                create_test_file(full_path)
        print("Completed!")