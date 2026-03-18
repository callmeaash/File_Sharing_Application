from fastapi import APIRouter, status, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os
import secrets
from database import SessionDep
from auth import CurrentUserDep
from sqlmodel import select
from models import UserFile, FilePermission, Folder, FolderPermission
from datetime import datetime, timezone, timedelta
from schemas import FileAccess, AccessCreate
from database_operations import DatabaseOperations


router = APIRouter()

@router.get("/file/{file_id}/access", response_model=FileAccess)
def get_file_access(file_id: int, session: SessionDep, current_user: CurrentUserDep):
    file = session.exec(select(UserFile).where(UserFile.id == file_id)).first()
    if not file or file.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="File not found")
        
    permission = session.exec(select(FilePermission).where(FilePermission.file_id == file_id)).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission


@router.patch("/file/{file_id}/access", response_model=FileAccess)
def change_file_access_type(file_id: int, access_data: AccessCreate, session: SessionDep, current_user: CurrentUserDep):

    file = session.exec(select(UserFile).where(UserFile.id == file_id)).first()
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    if file.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have the right to modify this file"
        )

    if access_data.access_type not in ['only_me', 'anyone_with_link', 'timed_access']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid access type"
        )

    file_permission = session.exec(
        select(FilePermission)
        .where(FilePermission.file_id == file.id)
    ).first()

    if not file_permission:
        file_permission = FilePermission(file_id=file.id)
        session.add(file_permission)
        session.commit()
        session.refresh(file_permission)

    db_ops = DatabaseOperations(session)
    share_token = secrets.token_urlsafe(32)
    if access_data.access_type == 'anyone_with_link':
        file_permission.access_type = access_data.access_type
        file_permission.share_token = share_token

        return db_ops.update_file_permission(file_permission)

    elif access_data.access_type == 'timed_access':
        if access_data.time_unit not in ['days', 'minutes', 'hours']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid time unit, must be ['days', 'minutes', 'hours']"
            )
        if access_data.time_value <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Time value must be positive"
            )
        kwargs = {access_data.time_unit: access_data.time_value}
        expiry_time = datetime.now(timezone.utc) + timedelta(**kwargs)
        file_permission.access_type = access_data.access_type
        file_permission.share_token = share_token
        file_permission.expiry_time = expiry_time
        return db_ops.update_file_permission(file_permission)

    # only_me case
    file_permission.access_type = access_data.access_type
    file_permission.share_token = None
    file_permission.expiry_time = None
    return db_ops.update_file_permission(file_permission)


@router.get("/file/{token}")
def get_file_by_token(token: str, session: SessionDep):
    """
    Endpoint to return file through access link
    """
    file_permission = session.exec(
        select(FilePermission)
        .where(FilePermission.share_token == token)
    ).first()

    if not file_permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid link"
        )
    
    file = session.exec(
            select(UserFile)
            .where(UserFile.id == file_permission.file_id)
        ).first()
    
    if not os.path.exists(file.filepath):
        raise HTTPException(status_code=404, detail="File missing on server")
    
    file_response = FileResponse(
        path=file.filepath,
        filename=file.filename,
        media_type=file.mime_type
    )
    file.download_count += 1
    session.add(file)
    session.commit()
    if file_permission.access_type == 'anyone_with_link':
        return file_response
    
    elif file_permission.access_type == 'timed_access':
        if file_permission.expiry_time < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Link already expired"
            )
        return file_response


@router.get("/folder/{folder_id}/access", response_model=FileAccess)
def get_folder_access(folder_id: int, session: SessionDep, current_user: CurrentUserDep):
    folder = session.exec(select(Folder).where(Folder.id == folder_id)).first()
    if not folder or folder.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Folder not found")
        
    permission = session.exec(select(FolderPermission).where(FolderPermission.folder_id == folder_id)).first()
    if not permission:
        # Default permission
        return FolderPermission(folder_id=folder_id, access_type='only_me')
    return permission


@router.patch("/folder/{folder_id}/access", response_model=FileAccess)
def change_folder_access_type(folder_id: int, access_data: AccessCreate, session: SessionDep, current_user: CurrentUserDep):
    folder = session.exec(select(Folder).where(Folder.id == folder_id)).first()
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found"
        )
    
    if folder.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have the right to modify this folder"
        )

    if access_data.access_type not in ['only_me', 'anyone_with_link', 'timed_access']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid access type"
        )

    folder_permission = session.exec(
        select(FolderPermission)
        .where(FolderPermission.folder_id == folder.id)
    ).first()

    # Create permission if it doesn't exist yet
    if not folder_permission:
        folder_permission = FolderPermission(folder_id=folder.id)
        session.add(folder_permission)
        session.commit()
        session.refresh(folder_permission)

    db_ops = DatabaseOperations(session)
    share_token = secrets.token_urlsafe(32)

    if access_data.access_type == 'anyone_with_link':
        folder_permission.access_type = access_data.access_type
        folder_permission.share_token = share_token
        result = db_ops.update_folder_permission(folder_permission)
        db_ops.apply_folder_permissions_recursively(folder.id, access_data.access_type)
        return result

    elif access_data.access_type == 'timed_access':
        if access_data.time_unit not in ['days', 'minutes', 'hours']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid time unit, must be ['days', 'minutes', 'hours']"
            )
        if access_data.time_value <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Time value must be positive"
            )
        kwargs = {access_data.time_unit: access_data.time_value}
        expiry_time = datetime.now(timezone.utc) + timedelta(**kwargs)
        folder_permission.access_type = access_data.access_type
        folder_permission.share_token = share_token
        folder_permission.expiry_time = expiry_time
        result = db_ops.update_folder_permission(folder_permission)
        db_ops.apply_folder_permissions_recursively(folder.id, access_data.access_type, expiry_time)
        return result

    # only_me case
    folder_permission.access_type = access_data.access_type
    folder_permission.share_token = None
    folder_permission.expiry_time = None
    result = db_ops.update_folder_permission(folder_permission)
    db_ops.apply_folder_permissions_recursively(folder.id, access_data.access_type)
    return result


@router.get("/folder/{token}")
def get_folder_by_token(token: str, session: SessionDep):
    """
    Endpoint to return folder contents through access link
    """
    folder_permission = session.exec(
        select(FolderPermission)
        .where(FolderPermission.share_token == token)
    ).first()

    if not folder_permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid link"
        )

    if folder_permission.access_type == 'timed_access':
        if folder_permission.expiry_time < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Link already expired"
            )

    folder = session.exec(
        select(Folder).where(Folder.id == folder_permission.folder_id)
    ).first()

    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    files = folder.files
    file_list = [
        {
            "id": f.id,
            "filename": f.filename,
            "filesize": f.filesize,
            "mime_type": f.mime_type,
            "upload_date": str(f.upload_date),
        }
        for f in files
    ]

    return {
        "folder_name": folder.name,
        "files": file_list,
    }

@router.get("/folder/{token}/file/{file_id}")
def download_file_from_shared_folder(token: str, file_id: int, session: SessionDep):
    """
    Endpoint to download a specific file from a shared folder
    """
    folder_permission = session.exec(
        select(FolderPermission)
        .where(FolderPermission.share_token == token)
    ).first()

    if not folder_permission:
        raise HTTPException(status_code=404, detail="Invalid link")

    if folder_permission.access_type == 'timed_access':
        if folder_permission.expiry_time < datetime.now(timezone.utc):
            raise HTTPException(status_code=404, detail="Link already expired")

    # Verify the file is actually in this folder
    file = session.exec(
        select(UserFile)
        .where((UserFile.id == file_id) & (UserFile.folder_id == folder_permission.folder_id))
    ).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found in this folder")
        
    if not os.path.exists(file.filepath):
        raise HTTPException(status_code=404, detail="File missing on server")

    file.download_count += 1
    session.add(file)
    session.commit()
    
    return FileResponse(
        path=file.filepath,
        filename=file.filename,
        media_type=file.mime_type
    )