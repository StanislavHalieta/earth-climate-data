import gzip
import io

def decompress_gz_file(raw_gz_bytes: bytes, as_text: bool = False) -> any:
    """
    Розпаковує байтовий потік .gz архіву прямо в оперативну пам'ять.
    
    :param raw_gz_bytes: Сирі байти завантаженого .gz файлу (наприклад, response.content)
    :param as_text: Якщо True — повертає декодований текст (str), якщо False — чисті байти (bytes)
    """
    try:
        # Загортаємо сирі байти в буфер, щоб gzip міг з ними працювати як з файлом
        compressed_stream = io.BytesIO(raw_gz_bytes)
        
        with gzip.open(compressed_stream, 'rb') as f_in:
            decompressed_bytes = f_in.read()
            
        if as_text:
            # Декодуємо в текст, якщо всередині текстовий файл (CSV/TXT)
            return decompressed_bytes.decode('utf-8')
            
        return decompressed_bytes

    except Exception as e:
        print(f"❌ Помилка під час розпакування в пам'ять: {e}")
        raise e