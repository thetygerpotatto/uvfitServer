# uvfitServer

FastAPI backend for the [UVfit](https://github.com/thetygerpotatto/uvfit) mobile app: user registration and login with **bcrypt** password hashing and **JWT** auth, plus profile and health data endpoints, backed by **SQLAlchemy** (Azure SQL). Deployed to **Azure App Service** through GitHub Actions.

## Configuration
Set these environment variables (in Azure: App Service → Configuration):

| Variable | Description |
|---|---|
| `DATABASE_URL` | SQLAlchemy connection string, e.g. `mssql+pyodbc://user:pass@host:1433/db?driver=ODBC+Driver+18+for+SQL+Server` |
| `JWT_SECRET_KEY` | Long random string used to sign tokens (`python -c "import secrets;print(secrets.token_urlsafe(48))"`) |

## Run locally
```sh
pip install -r requirements.txt
export DATABASE_URL=sqlite:///./dev.db JWT_SECRET_KEY=dev-only
uvicorn main:app --reload
```
