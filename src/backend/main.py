from fastapi import FastAPI
from .auth import routes as auth_routes

app = FastAPI(title="Secure Auth API")

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Secure Auth API"}
