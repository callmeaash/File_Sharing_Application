# FileVault (File Management System)

A full-stack file sharing and management application featuring a Google Drive-like Vue 3 frontend and a robust FastAPI backend. It allows users to upload, manage, organize, and securely share both files and folders with flexible access controls.

## Features

- **Google Drive-like UI**: A clean, monochrome interface built with Vue 3 and Tailwind CSS v4.
- **User Authentication**: Secure user registration and login with JWT token-based authentication.
- **File Management**: Upload (including drag-and-drop support), download, and delete files.
- **Folder Organization**: Create, rename, delete, and navigate hierarchical folder structures.
- **Secure Sharing (Files & Folders)**:
  - **Private (Only Me)**: Restricted access to the owner.
  - **Public Link (Anyone with link)**: Generate shareable links for public access without authentication.
  - **Timed Access**: Generate links that automatically expire after a set duration (minutes, hours, days).
  - *Recursive permissions ensures that sharing a folder correctly applies access to all its contents.*
- **Dashboard Analytics**: Track total files, overall storage usage, and total download counts.
- **Per-User Storage**: Isolated secure storage directories for each user.

## Tech Stack

### Frontend
- **Framework**: Vue 3 (Composition API)
- **Routing**: Vue Router
- **Styling**: Tailwind CSS v4
- **HTTP Client**: Axios
- **Build Tool**: Vite

### Backend
- **Framework**: FastAPI
- **Database**: SQLModel with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens) with OAuth2
- **Password Hashing**: Bcrypt via Passlib
- **Environment**: Python-dotenv

## Project Structure

```text
File_Management_System/
├── backend/                   # FastAPI Server
│   ├── main.py                # App initialization and router setup
│   ├── models.py              # SQLModel database models
│   ├── schemas.py             # Pydantic request/response models
│   ├── database_operations.py # Centralized database CRUD operations
│   ├── routers/               # API endpoint definitions (auth, files, folders, sharing, dashboard)
│   └── uploads/               # Auto-generated user file storage directory
└── frontend/                  # Vue 3 Client Application
    ├── index.html             # Main HTML entry point
    ├── vite.config.js         # Vite bundler configuration
    ├── package.json           # Frontend dependencies
    └── src/
        ├── main.js            # Vue application setup
        ├── router.js          # Client-side routing definitions
        ├── api.js             # Axios instance with auth interceptors
        ├── style.css          # Tailwind and global CSS
        ├── components/        # Reusable UI (Sidebar, FolderCard, FileCard, ShareModal, etc.)
        └── views/             # Page components (Login, Drive, Dashboard, SharedFolderView, etc.)
```

## Setup Instructions

### 1. Requirements
- Node.js (v18+)
- Python (3.8+)

### 2. Backend Setup
Navigate to the backend directory and set up the Python environment:

```bash
cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Create a .env file in the backend directory:
echo "DATABASE_URL=sqlite:///./test.db" > .env
echo "SECRET_KEY=your-secret-key-here" >> .env
echo "ALGORITHM=HS256" >> .env
echo "ACCESS_TOKEN_EXPIRE_MINUTES=1440" >> .env

# Run the backend development server
uvicorn main:app --reload
```

### 3. Frontend Setup
Open a new terminal, navigate to the frontend directory, and start the development server:

```bash
cd frontend

# Install Node dependencies
npm install

# Run the frontend development server
npm run dev
```

## Key API Endpoints
- **Authentication**: `POST /auth/register`, `POST /auth/login`
- **Files**: `POST /files/` (Upload), `DELETE /files/{id}`, `GET /files/{id}` (Download)
- **Folders**: `POST /folders/`, `GET /folders/`, `PATCH /folders/{id}`
- **Sharing**: 
  - `PATCH /share/file/{id}/access`, `PATCH /share/folder/{id}/access`
  - `GET /share/file/{token}`, `GET /share/folder/{token}` (Public retrieval)
- **Dashboard**: `GET /dashboard/dashboard`
