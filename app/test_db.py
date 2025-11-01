from database import SessionLocal

try:
    db = SessionLocal()
    print("✅ Database connection successful!")
except Exception as e:
    print("❌ Database connection failed:", e)
finally:
    db.close()
