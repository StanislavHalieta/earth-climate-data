import io
import zipfile
import logging

logger = logging.getLogger(__name__)

def extract_file_from_zip_parser(zip_binary_content, target_filename=None, as_bytes=False):
    try:
        if not zip_binary_content or not isinstance(zip_binary_content, bytes):
            logger.error("❌ Передано некоректний або порожній бінарний контент ZIP")
            return None

        # Перетворюємо байти на файлоподібний об'єкт у пам'яті
        zip_stream = io.BytesIO(zip_binary_content)
        
        with zipfile.ZipFile(zip_stream) as archive:
            # Отримуємо список усіх файлів в архіві
            file_list = archive.namelist()
            if not file_list:
                logger.error("❌ ZIP-архів порожній")
                return None
            
            # Визначаємо, який файл ми хочемо витягнути
            if target_filename:
                if target_filename not in file_list:
                    logger.error(f"❌ Файл '{target_filename}' не знайдено в архіві. Доступні: {file_list}")
                    return None
                file_to_extract = target_filename
            else:
                # Якщо файл не вказано — беремо перший ліпший
                file_to_extract = file_list[0]
                logger.info(f"📦 Автоматично обрано перший файл з архіву: {file_to_extract}")
            
            # Зчитуємо дані файлу
            with archive.open(file_to_extract) as extracted_file:
                raw_data = extracted_file.read()
                
            if as_bytes:
                return raw_data
            
            # Декодуємо байти в текст (для .txt чи .csv файлів)
            try:
                return raw_data.decode('utf-8')
            except UnicodeDecodeError:
                # Якщо utf-8 не зжував (іноді старі файли NOAA йдуть в cp1251 або latin-1)
                logger.warning(f"⚠️ Не вдалося декодувати {file_to_extract} в UTF-8. Пробуємо latin-1...")
                return raw_data.decode('latin-1')

    except zipfile.BadZipFile:
        logger.error("❌ Помилка: Передані байти не є валідним ZIP-архівом")
        return None
    except Exception as e:
        logger.error(f"❌ Помилка при розпакуванні ZIP: {str(e)}", exc_info=True)
        return None