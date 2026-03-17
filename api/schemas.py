from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ActivityLogCreate(BaseModel):
    app_name: str
    app_type: str
    mouse_x: Optional[float] = None
    mouse_y: Optional[float] = None
    key_strokes: Optional[str] = None
    timestamp: Optional[datetime] = None

class ActivityLogResponse(ActivityLogCreate):
    id: int
    user_id: int
    image_path: str
    cluster_id: Optional[int] = None
    is_interruption: bool

    class Config:
        from_attributes = True

class ClusterBase(BaseModel):
    name: str
    description: Optional[str]
    is_approved: bool

class ClusterResponse(ClusterBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class AnomalyResponse(BaseModel):
    id: int
    user_id: int
    cluster_id: Optional[int]
    activity_log_id: int
    detected_at: datetime
    description: str
    optimization_suggestion: Optional[str]
    
    class Config:
        from_attributes = True
