# Sneakzone Sprint 2 — Registration and Login

## Start

1. Open this folder in VS Code.
2. Open a terminal.
3. `python -m pip install -r requirements.txt`
4. `python app.py`
5. Visit http://127.0.0.1:5000

Windows may use `py` instead of `python`.

## Endpoints
- POST `/api/register`: JSON `{ "name": "...", "email": "...", "password": "..." }`
- POST `/api/login`: JSON `{ "email": "...", "password": "..." }`
- GET `/api/me`: current session
- POST `/api/logout`: clear session

SQLite stores account records in `users.db` (ignored by Git). Passwords are hashed.

## Important integration notes
This is a local demonstration module. Merge routes/templates into the shared Sneakzone project, and avoid defining `/api/login` twice if your team already has it. Replace the dev-only Flask secret with a secure environment variable for any hosted deployment. Do not commit user databases or secrets. Session cookies only work across the website and API when cookie/CORS settings are configured appropriately. Test checkout authentication after integration.

## Suggested test cases
1. Valid registration -> 201 and success message.
2. Duplicate email -> 409.
3. Invalid email -> 400.
4. Short password -> 400.
5. Valid login -> 200 and welcome.
6. Wrong password -> 401.
7. Unknown email -> 401.
8. Refresh while logged in -> remains logged in.
9. Logout -> session cleared.
10. GET `/api/me` after logout -> 401.

Record actual results and screenshots in Confluence; don't claim tests passed without executing them.
