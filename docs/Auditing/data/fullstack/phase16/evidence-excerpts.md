# Evidence Excerpts

## backend-authorization-pytest.txt

Command: backend/venv/Scripts/python.exe -m pytest -q tests/test_assignments.py -k "api_requires_session or admin_sign_in or admin_provisioned or admin_password_reset or demo_seed_requires or responder_only or session_logout or public_registration"
Working directory: backend

....F....
