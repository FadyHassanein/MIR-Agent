import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from backend.config import mongo_client

from backend.routes.webhook import router as webhook_router
from backend.workers.user_writer import start_user_writer
from backend.workers.chat_logger import start_chat_logger
from backend.workers.session_pruner import start_session_pruner

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ─── Startup ───────────────────────────────────────────────────────────────
    start_user_writer()         
    start_chat_logger()         
    start_session_pruner()

    # Give them a moment to spin up if needed
    await asyncio.sleep(0)
    yield
    # ─── Shutdown ──────────────────────────────────────────────────────────────
    # Close MongoDB connection
    if mongo_client:
        mongo_client.close()

# Create FastAPI with our lifespan manager
app = FastAPI(lifespan=lifespan)

# Include your webhook router (and any others)
app.include_router(webhook_router)
