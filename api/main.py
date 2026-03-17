from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
import os
import shutil
import uuid

from . import models, schemas, auth, database
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Activity Assist API")

# Setup CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STORAGE_TYPE = os.getenv("STORAGE_TYPE", "local")
LOCAL_STORAGE_PATH = os.getenv("LOCAL_STORAGE_PATH", "./storage")

if STORAGE_TYPE == "local":
    os.makedirs(LOCAL_STORAGE_PATH, exist_ok=True)

# ----------------- AUTH ENDPOINTS -----------------

@app.post("/auth/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/auth/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = auth.timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# ----------------- AGENT ENDPOINTS -----------------

@app.post("/agent/log", response_model=schemas.ActivityLogResponse)
async def create_activity_log(
    file: UploadFile = File(...),
    app_name: str = Form(...),
    app_type: str = Form("unknown"),
    mouse_x: float = Form(None),
    mouse_y: float = Form(None),
    key_strokes: str = Form(None),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    # Save file
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'png'
    file_name = f"{uuid.uuid4()}.{file_extension}"
    
    if STORAGE_TYPE == "local":
        file_path = os.path.join(LOCAL_STORAGE_PATH, file_name)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        image_uri = file_path
    else:
        # TBD: S3 upload
        image_uri = f"s3://placeholder/{file_name}"
        
    db_log = models.ActivityLog(
        user_id=current_user.id,
        image_path=image_uri,
        app_name=app_name,
        app_type=app_type,
        mouse_x=mouse_x,
        mouse_y=mouse_y,
        key_strokes=key_strokes
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

# ----------------- ANALYTICS ENDPOINTS -----------------

@app.get("/analytics/clusters", response_model=List[schemas.ClusterResponse])
def get_clusters(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.SequenceCluster).all()

@app.post("/analytics/clusters/{cluster_id}/approve")
def approve_cluster(cluster_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    cluster = db.query(models.SequenceCluster).filter(models.SequenceCluster.id == cluster_id).first()
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    cluster.is_approved = True
    db.commit()
    return {"message": "Cluster approved"}

@app.get("/analytics/anomalies", response_model=List[schemas.AnomalyResponse])
def get_anomalies(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Anomaly).all()
