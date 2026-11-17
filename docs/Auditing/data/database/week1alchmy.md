PS C:\Users\Admin\Documents\caseloop> Get-ChildItem -Recurse -Filter "models.py" | Select-String "__tablename__"

backend\app\models\models.py:15:  __tablename__ = "users"
backend\app\models\models.py:30:  __tablename__ = "responses"
backend\app\models\models.py:53:  __tablename__ = "response_events"
backend\app\models\models.py:66:  __tablename__ = "assignments"
backend\app\models\models.py:77:  __tablename__ = "audit_logs"