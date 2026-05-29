from fastapi import FastAPI
from app.api.routes import ping, links

app = FastAPI(title="Link Shortener")

app.include_router(ping.router, prefix="/ping", tags=["ping"])
app.include_router(links.router, prefix="/links", tags=["links"])