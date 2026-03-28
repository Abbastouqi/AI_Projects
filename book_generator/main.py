from fastapi import FastAPI
from book_generator.api.routes import router
from book_generator.api.schemas import HealthResponse

app = FastAPI(
    title="Book Generator API",
    description="Automated book generation with human-in-the-loop editing",
    version="1.0.0",
)

app.include_router(router)


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health():
    return {"status": "ok"}
