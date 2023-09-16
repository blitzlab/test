import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .core import config
from .db import session
from app.api.endpoints import user, post
from app.services import auth
from app.db import base_class  # Importing for creating tables

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Create tables if they don't exist yet
    base_class.Base.metadata.create_all(bind=session.engine)

@app.on_event("shutdown")
async def shutdown():
    # You can add any shutdown logic here if needed
    pass

# Include routers
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(post.router, prefix="/post", tags=["post"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Optional: Add a custom exception handler
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc: HTTPException):
    return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)

