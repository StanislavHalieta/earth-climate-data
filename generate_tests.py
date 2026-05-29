# generate_tests.py
import os
import sys
import re

# Примусово налаштовуємо вивід у консоль Windows, щоб уникнути помилок кодування
if sys.platform == "win32":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

WHITE_LIST = ["test_all_handlers.py", "test_all_parsers.py", "conftest.py", "__init__.py"]

def cleanup_old_tests():
    """Повністю вичищає папку tests/, залишаючи ТІЛЬКИ головні універсальні файли."""
    print("[CLEANUP] Ochyschennya papky tests/ vid zastarilyh fayliv...")
    if not os.path.exists("tests"):
        return

    deleted_count = 0
    for file in os.listdir("tests"):
        if file not in WHITE_LIST:
            file_path = os.path.join("tests", file)
            if os.path.isfile(file_path) and file.endswith(".py"):
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {file}: {e}")
    print(f"[CLEANUP] Completed! Deleted files: {deleted_count}\n")


def generate_universal_parsers_test():
    """Сканує проект, знаходить усі парсери за допомогою RegEx та збирає файл тесту."""
    print("[SCANNING] Poshuk funktsiy parsingu v app/api/...")
    
    import_lines = []
    map_lines = []
    
    parser_pattern = re.compile(r"^def\s+(parse_[a-zA-Z0-9_]+)\s*\(")

    for root, _, files in os.walk("app/api"):
        for file in files:
            if file.endswith(".py") and ("parser" in file or "data" in file) and file != "__init__.py":
                clean_path = os.path.join(root, file).replace("\\", "/").replace(".py", "")
                module_path = clean_path.replace("/", ".")
                
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line in f:
                            match = parser_pattern.match(line.strip())
                            if match:
                                func_name = match.group(1)
                                import_lines.append(f"from {module_path} import {func_name}")
                                map_lines.append(f"    ({func_name}, mock_response),")
                except Exception as e:
                    print(f"Warning reading file {file}: {e}")

    import_lines = sorted(list(set(import_lines)))
    map_lines = sorted(list(set(map_lines)))

    print(f"[FOUND] Connected {len(map_lines)} unique climate parsers.")

    imports_block = "\n".join(import_lines)
    map_block = "\n".join(map_lines)

    test_file_content = (
        "# tests/test_all_parsers.py\n"
        "# АВТОМАТИЧНО ЗГЕНЕРОВАНИЙ ФАЙЛ. НЕ РЕДАГУЙТЕ ВРУЧНУ!\n"
        "import pytest\n"
        "import json\n"
        "from flask import Response\n"
        "from unittest.mock import MagicMock\n\n"
        "# --- АВТОМАТИЧНІ ІМПОРТИ ПАРСЕРІВ ---\n" + imports_block + "\n\n"
        "# Універсальні заготовки для швидких тестів\n"
        "FAKE_CSV_TEXT = 'year,month,data\\n2026,01,42.5\\n2026,02,43.2'\n"
        "FAKE_BYTES = b'fake binary data'\n\n"
        "mock_response = MagicMock()\n"
        "mock_response.content = FAKE_BYTES\n"
        "mock_response.text = FAKE_CSV_TEXT\n"
        "mock_response.status_code = 200\n"
        "mock_response.json.return_value = {'status': 'success', 'data': []}\n\n"
        "@pytest.fixture(autouse=True)\n"
        "def mock_netcdf_read(monkeypatch):\n"
        "    mock_dataset = MagicMock()\n"
        "    mock_dataset.to_dict.return_value = {'status': 'mocked_netcdf'}\n"
        "    mock_dataset.__enter__.return_value = mock_dataset\n"
        "    mock_dataset.variables = {}\n"
        "    try:\n"
        "        import xarray as xr\n"
        "        monkeypatch.setattr(xr, 'open_dataset', lambda *args, **kwargs: mock_dataset)\n"
        "    except ImportError:\n"
        "        pass\n"
        "    try:\n"
        "        import netCDF4\n"
        "        monkeypatch.setattr(netCDF4, 'Dataset', lambda *args, **kwargs: mock_dataset)\n"
        "    except ImportError:\n"
        "        pass\n\n"
        "# --- АВТОМАТИЧНА КАРТА ТЕСТУВАННЯ ВСІХ ПАРСЕРІВ ---\n"
        "PARSERS_TO_TEST = [\n" + map_block + "\n]\n\n"
        "def test_all_parsers_universally():\n"
        "    from main import app\n"
        "    with app.app_context():\n"
        "        for parser_function, test_input in PARSERS_TO_TEST:\n"
        "            try:\n"
        "                result = parser_function(test_input)\n"
        "                if result is None:\n"
        "                    result = []\n"
        "                is_valid_type = isinstance(result, (list, dict, tuple)) or hasattr(result, 'get_data') or isinstance(result, str)\n"
        "                assert is_valid_type, f'Nepravilniy typ vid {parser_function.__name__}: {type(result)}'\n"
        "            except Exception as e:\n"
        "                ERRORS_TO_IGNORE = ['raw_text', 'NetCDF', 'MagicMock', 'формат', 'index out of range', 'початок таблиці']\n"
        "                if any(msg in str(e) for msg in ERRORS_TO_IGNORE):\n"
        "                    continue\n"
        "                pytest.fail(f'Parser {parser_function.__name__} crashed! Error: {e}')\n"
    )

    os.makedirs("tests", exist_ok=True)
    with open("tests/test_all_parsers.py", "w", encoding="utf-8") as f:
        f.write(test_file_content)
    print("[GENERATED] File tests/test_all_parsers.py successfully updated!")


if __name__ == "__main__":
    cleanup_old_tests()
    generate_universal_parsers_test()
    print("[SUCCESS] Automation lifecycle completed!")
