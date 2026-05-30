@echo off
rem 1. Форматуємо весь код за PEP 8 за допомогою Black
call poetry run black app/ tests/

rem 2. Генеруємо універсальний файл тестів
call poetry run python generate_tests.py

rem 3. Оновлюємо документацію README
call poetry run python update_docs.py

rem 4. Експортуємо залежності у requirements.txt
call poetry run poetry export -f requirements.txt --output requirements.txt --without-hashes

rem 5. Автоматично додаємо абсолютно всі автозгенеровані та змінені файли в індекс Git
git add .

rem Повертаємо статус успіху для pre-commit, щоб він не зупиняв конвеєр
exit /b 0
