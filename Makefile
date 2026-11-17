# CaseLoop Enterprise Makefile
.PHONY: help backend frontend audit seed db-up db-down db-logs

help:
	@echo "CaseLoop Automation Commands:"
	@echo "  make api     - Start FastAPI backend"
	@echo "  make ui      - Start React Vite frontend"
	@echo "  make audit   - Run directory audit tree script"
	@echo "  make seed    - Run database demo seeder"
	@echo "  make bash    - Enable shell to run commands/files"
	@echo "  make db-up   - Start PostgreSQL dockers click docker desktop -engine must run"
	@echo "  make db-down - Stop PostgreSQL container"
	@echo "  make db-logs - View PostgreSQL container logs"
	@echo "  make pip     - using pip in windows becasue of security policies"
	@echo "  make almebic - alembic is affected by security too"

api:
	cd backend && venv\Scripts\activate && python -m uvicorn app.main:app --reload --port 8000

ui:
	cd frontend && npm run dev

audit:
	powershell -ExecutionPolicy Bypass -File .\scripts\audit_tree.ps1

seed:
	cd backend && venv\Scripts\activate && python -m app.seed

bash:
	powershell -ExecutionPolicy Bypass

db-up:
	docker compose up -d db

db-down:
	docker compose down

db-logs:
	docker compose logs -f postgres

pip:
	python -m pip install python-dotenv

alembic:
	python -m alembic upgrade head