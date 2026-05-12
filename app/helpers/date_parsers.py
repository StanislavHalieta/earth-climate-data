from datetime import datetime, timedelta

def decimal_to_date(decimal_year):
    year = int(decimal_year)
    remainder = decimal_year - year
    
    # Визначаємо перший день року
    base_date = datetime(year, 1, 1)
    
    # Визначаємо кількість днів у році (365 або 366)
    days_in_year = (datetime(year + 1, 1, 1) - base_date).days
    
    # Додаємо дробову частку до базової дати
    result_date = base_date + timedelta(days=remainder * days_in_year)
    
    # Повертаємо у форматі YYYY-MM-DD
    return result_date.strftime('%d-%m-%Y')