from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

from app.api.upload import router as upload_router
from app.api.queryApi import router as query_router
from app.api.status import router as status_router
from app.core.syncS3 import start_background_sync

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
        prefix="/api",
        tags=["Documents"]
    )

    app.include_router(
        query_router,
        prefix="/api"
    )

    app.include_router(
        status_router,
        prefix="/api"
    )


    @app.on_event("startup")
    def startup_event():
        start_background_sync()


    @app.get("/health", tags=["System"])
    def health():
        return {
            "status": "ok",
            "service": "rag-teacher",
            "version": "1.0.0"
        }

    return app


app = create_app()
