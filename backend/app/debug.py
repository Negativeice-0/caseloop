# 1. Verify database connection and check user records
from app.core.database import SessionLocal
from app.models import models
db = SessionLocal()
users = db.query(models.User).all()
print("Registered Users:", [(u.email, u.role, getattr(u, 'is_superuser', None)) for u in users])

# 2. Print all registered FastAPI routes to verify endpoints exist
from app.main import app
for route in app.routes:
    if hasattr(route, "path"):
        print(route.path, route.methods)