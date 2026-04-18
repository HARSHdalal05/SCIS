from fastapi import FastAPI

from .database import Base, engine
from .routers import auth, dashboard, generate, progress, user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FitMorph AI API", version="1.0.0")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(generate.router)
app.include_router(progress.router)
app.include_router(dashboard.router)


@app.get("/")
def healthcheck():
    return {"status": "ok", "service": "FitMorph AI API"}
