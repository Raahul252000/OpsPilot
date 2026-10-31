import uvicorn
from fastapi import FastAPI
from app.routes.incident import router as incident_router

app = FastAPI(
    title="OpsPilot",
    description="AI Incident Investigation and Resolution Assistant",
    version="0.1.0",
)

app.include_router(incident_router)

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "opspilot",
        }


if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)