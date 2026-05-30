import json


def helper_extract_json(data):
    """Допоміжна функція для витягування чистого JSON з об'єктів Response Flask."""
    if hasattr(data, "get_data"):
        return data.get_data(as_text=True)
    if isinstance(data, (dict, list)):
        return json.dumps(data)
    return str(data)
