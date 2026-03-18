from models import User, UserFile, Folder, FilePermission, FolderPermission
from typing import Optional
import secrets
from datetime import datetime
from sqlmodel import Session, select
from exceptions import handle_db_errors
from utils import verify_password


class DatabaseOperations:
    """Centralized database operations with built-in error handling"""
    
    def __init__(self, session: Session):
        self.session = session
    
    @handle_db_errors("user creation")
    def create_user(self, email: str, hashed_password: str) -> User:
        new_user = User(email=email, password=hashed_password)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
    
    @handle_db_errors("folder creation")
    def create_folder(self, name: str, owner_id: int, parent_id: Optional[int] = None) -> Folder:
        new_folder = Folder(name=name, owner_id=owner_id, parent_id=parent_id)
        self.session.add(new_folder)
        self.session.commit()
        self.session.refresh(new_folder)
        return new_folder

    @handle_db_errors("folder update")
    def update_folder(self, folder: Folder, name: str) -> Folder:
        folder.name = name
        self.session.add(folder)
        self.session.commit()
        self.session.refresh(folder)
        return folder
    
    @handle_db_errors("folder deletion")
    def delete_folder(self, folder: Folder) -> None:
        self.session.delete(folder)
        self.session.commit()
    
    @handle_db_errors("file upload")
    def upload_file(self, file_data: UserFile) -> UserFile:
        self.session.add(file_data)
        self.session.commit()
        self.session.refresh(file_data)
        
        # Create file permission
        new_permission = FilePermission(file_id=file_data.id)
        self.session.add(new_permission)
        self.session.commit()
        return file_data
    
    @handle_db_errors("file deletion")
    def delete_file(self, file: UserFile) -> None:
        self.session.delete(file)
        self.session.commit()
    
    @handle_db_errors("permission update")
    def update_file_permission(self, permission: FilePermission) -> FilePermission:
        self.session.add(permission)
        self.session.commit()
        self.session.refresh(permission)
        return permission
    
    @handle_db_errors("folder permission update")
    def update_folder_permission(self, permission: FolderPermission) -> FolderPermission:
        self.session.add(permission)
        self.session.commit()
        self.session.refresh(permission)
        return permission
    
    @handle_db_errors("recursive permission update")
    def apply_folder_permissions_recursively(self, folder_id: int, access_type: str, expiry_time: Optional[datetime] = None) -> None:
        """Recursively apply access permissions to all nested folders and files."""

        files = self.session.exec(select(UserFile).where(UserFile.folder_id == folder_id)).all()
        for file in files:
            file_perm = self.session.exec(select(FilePermission).where(FilePermission.file_id == file.id)).first()
            if not file_perm:
                file_perm = FilePermission(file_id=file.id)
                self.session.add(file_perm)
            
            file_perm.access_type = access_type
            file_perm.expiry_time = expiry_time
            if access_type != 'only_me' and not file_perm.share_token:
                file_perm.share_token = secrets.token_urlsafe(32)
            
        subfolders = self.session.exec(select(Folder).where(Folder.parent_id == folder_id)).all()
        for subfolder in subfolders:
            folder_perm = self.session.exec(select(FolderPermission).where(FolderPermission.folder_id == subfolder.id)).first()
            if not folder_perm:
                folder_perm = FolderPermission(folder_id=subfolder.id)
                self.session.add(folder_perm)
            
            folder_perm.access_type = access_type
            folder_perm.expiry_time = expiry_time
            if access_type != 'only_me' and not folder_perm.share_token:
                folder_perm.share_token = secrets.token_urlsafe(32)
                
            # Recursive call for the subfolder
            self.apply_folder_permissions_recursively(subfolder.id, access_type, expiry_time)
            
        self.session.commit()
    
    @handle_db_errors("user authentication")
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with comprehensive error handling"""
        user = self.session.exec(select(User).where(User.email == email)).first()
        
        if not user:
            return None
            
        if not verify_password(password, user.password):
            return None
        return user