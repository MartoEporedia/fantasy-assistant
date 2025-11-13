from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import players, auth, auctions, rosters, advice, community
from app.core.config import settings

app = FastAPI(
    title="Fantasy Assistant API",
    description="API for Fantasy Football (Serie A) Assistant",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(players.router, prefix="/api/players", tags=["players"])
app.include_router(auctions.router, prefix="/api/auctions", tags=["auctions"])
app.include_router(rosters.router, prefix="/api/rosters", tags=["rosters"])
app.include_router(advice.router, prefix="/api/advice", tags=["advice"])
app.include_router(community.router, prefix="/api/community", tags=["community"])

@app.get("/")
async def root():
    return {
        "message": "Fantasy Assistant API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
