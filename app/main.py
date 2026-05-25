from fastapi import FastAPI

from app.routes.triage import router as triage_router

app = FastAPI(title="FlockSRE", description="AI-powered delivery ops triage agent")

app.include_router(triage_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
