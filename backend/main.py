from os import getenv
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from dotenv import load_dotenv

from routers import auth, folders, files, sharing, dashboard

app = FastAPI()

load_dotenv()

frontend_url = getenv("FRONTEND_URL", "http://localhost:5173")
origins = [url.strip().rstrip("/") for url in frontend_url.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# Create tables in the database
init_db()


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(folders.router, prefix="/folders", tags=["Folders"])
app.include_router(files.router, prefix="/files", tags=["Files"])
app.include_router(sharing.router, prefix="/share", tags=["File Sharing"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])


router = APIRouter()



