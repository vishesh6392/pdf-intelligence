from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

from app.api.upload import router as upload_router
from app.api.queryApi import router as query_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="RAG Teacher Service",
        description="AI service for document-based teaching & explanation",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Node.js will sit in front later
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(
        upload_router,
        prefix="/v1/documents",
        tags=["Documents"]
    )

    app.include_router(
        query_router,
        prefix="/api"
    )

    @app.get("/health", tags=["System"])
    def health():
        return {
            "status": "ok",
            "service": "rag-teacher",
            "version": "1.0.0"
        }

    return app


app = create_app()
