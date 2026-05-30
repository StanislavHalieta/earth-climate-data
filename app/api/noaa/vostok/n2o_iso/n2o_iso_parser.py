import io
import pandas as pd


def parse_vostok_n2o_iso_data(raw_bytes):
    # 1. Декодуємо байти. Оригінальний файл NOAA використовує кодування 'cp1252' або 'ISO-8859-1'
    if isinstance(raw_bytes, bytes):
        text_data = raw_bytes.decode("ISO-8859-1")
    else:
        text_data = raw_bytes

    # 2. Розбиваємо на рядки та очищаємо від зайвих пробілів на кінцях
    lines = [line.strip() for line in text_data.splitlines()]

    # 3. Шукаємо точний початок таблиці даних
    start_idx = None
    for idx, line in enumerate(lines):
        if line.startswith("Depth (mbs)"):
            start_idx = idx
            break

    if start_idx is None:
        raise ValueError("Не вдалося знайти початок таблиці даних у файлі NOAA.")

    # 4. Витягуємо лише рядки таблиці (пропускаючи заголовок "Depth (mbs)...")
    # Також фільтруємо порожні рядки та текстовий підпис в самому кінці
    data_lines = []
    for line in lines[start_idx + 1 :]:
        if not line:
            continue
        # Якщо рядок не починається з цифри (наприклад, пусті блоки чи системні знаки) — ігноруємо
        if not line[0].isdigit():
            continue
        data_lines.append(line)

    # 5. Збираємо очищені рядки назад у потік для Pandas
    clean_table_text = "\n".join(data_lines)

    # 6. Читаємо дані. Використовуємо регуляку \s+ для будь-якої кількості пробілів/табуляцій
    # Назви колонок задаємо вручну, щоб уникнути проблем із символами проміле (‰)
    df = pd.read_csv(
        io.StringIO(clean_table_text),
        sep=r"\s+",
        header=None,
        names=["depth_mbs", "gas_age_ka", "n2o_ppbv", "d15n", "d18o"],
        engine="python",
    )

    # 7. Конвертуємо всі значення у числа, некоректні дані стануть NaN
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 8. Замінюємо NaN на None, щоб у підсумковому JSON отримати чисті null
    df = df.astype(object).where(pd.notnull(df), None)

    # 9. Повертаємо готовий список словників (Python-об'єкт)
    return df.to_dict(orient="records")
