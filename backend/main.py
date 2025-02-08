from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

# ✅ Create FastAPI app instance
app = FastAPI()

# ✅ CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include API routes
app.include_router(router)

# ✅ Default test route
@app.get("/")
async def root():
    return {"message": "MediShare Backend is running!"}