import sys
import os
from dotenv import load_dotenv

# 1. Load root .env file
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(root_env)
print(f"📁 Loaded environment from: {root_env}")

# 2. Add backend root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from app.core.config import settings
    print(f"✅ Config loaded. Target Database URL: {settings.DATABASE_URL}")

    # Correct import paths based on your project structure
    from app.core.database import SessionLocal
    from app.models.models import User

    db = SessionLocal()
    users = db.query(User).all()
    
    print("\n--- DATABASE USER AUDIT ---")
    if not users:
        print("⚠️ Connected to database, but the users table is completely empty!")
    else:
        print(f"✅ Found {len(users)} user(s) in the database:")
        for u in users:
            name = getattr(u, 'full_name', getattr(u, 'name', 'N/A'))
            print(f"   - Email: {u.email} | Name: {name} | Superuser: {u.is_superuser}")
            
    db.close()

except Exception as e:
    print(f"\n❌ ERROR DURING AUDIT: {e}")
    import traceback
    traceback.print_exc()