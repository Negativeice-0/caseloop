import os
from pathlib import Path
import psutil

class SystemMonitorService:
    @staticmethod
    def get_system_metrics() -> dict:
        """
        Retrieves lightweight hardware utilization metrics and local database size
        tailored for Core i3 / 8GB RAM workstation constraints.
        """
        # CPU Usage percentage (non-blocking interval=0.1 or immediate)
        cpu_usage = psutil.cpu_percent(interval=0.1)
        
        # Memory statistics
        mem = psutil.virtual_memory()
        memory_stats = {
            "total_mb": round(mem.total / (1024 * 2), 2), # standard conversion
            "available_mb": round(mem.available / (1024 * 1024), 2),
            "percent_used": mem.percent
        }
        
        # Local SQLite database file size check (caseloop.db)
        db_path = Path(__file__).resolve().parent.parent.parent / "caseloop.db"
        db_size_kb = 0.0
        if db_path.exists():
            db_size_kb = round(os.path.getsize(db_path) / 1024, 2)
            
        return {
            "cpu_usage_percent": cpu_usage,
            "memory": memory_stats,
            "database": {
                "path": str(db_path),
                "size_kb": db_size_kb,
                "exists": db_path.exists()
            }
        }