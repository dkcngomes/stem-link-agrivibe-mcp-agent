from fastapi import FastAPI
from agrivibe.api import knowledge, ask

app = FastAPI(
    title="AgriVibe API",
    description="AgriVibe is a multi-agent agriculture knowledge system for Sri Lanka",
    version="0.1.0",
)

# Introcucing the knowledge and ask routers to the main FastAPI application
app.include_router(knowledge.router)
app.include_router(ask.router)

#default health check endpoint
@app.get("/health", tags=["System", "Health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
