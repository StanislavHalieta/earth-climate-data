# cron_update_data.py
from main import create_app
from app.services import DatabaseService

# Ізольовані функції збору
from app.api.nasa.sync import sync_nasa_data
from app.api.noaa.sync import sync_noaa_data
from app.api.peltier.sync import sync_peltier_data

db = DatabaseService()

def update_climate_metrics():
    print("🔄 Запуск ПОВНОЇ синхронізації ВСІХ доменів із Supabase...")
    app = create_app()
    
    with app.app_context():
        try:
            # 🚀 ПЕРШИМ ДІЛОМ ПЕРЕВІРЯЄМО І СТВОРЮЄМО ТАБЛИЦЮ
            db.create_tables_if_not_exists()
            
            # Тільки після цього збираємо метрики
            sync_nasa_data()
            sync_noaa_data()
            sync_peltier_data()
            
            print("\n=======================================================")
            print("🎉 СИНХРОНІЗАЦІЯ ЗАВЕРШЕНА! СТРУКТУРА КОДУ ІДЕАЛЬНА!")
            print("=======================================================")
            
        except Exception as e:
            print(f"❌ Критична помилка під час виконання крону: {e}")

if __name__ == "__main__":
    update_climate_metrics()
