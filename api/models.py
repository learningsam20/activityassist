from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    image_path = Column(String)  # Path to local storage or S3 URI
    app_name = Column(String, index=True)
    app_type = Column(String)
    mouse_x = Column(Float, nullable=True)
    mouse_y = Column(Float, nullable=True)
    key_strokes = Column(String, nullable=True)
    is_interruption = Column(Boolean, default=False)
    
    # Optional cluster assignment after AI processing
    cluster_id = Column(Integer, ForeignKey("sequence_clusters.id"), nullable=True)
    
class SequenceCluster(Base):
    __tablename__ = "sequence_clusters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String) # AI proposed name or SME approved name
    description = Column(Text, nullable=True)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship to logs
    logs = relationship("ActivityLog", backref="cluster")

class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    cluster_id = Column(Integer, ForeignKey("sequence_clusters.id"), nullable=True)
    activity_log_id = Column(Integer, ForeignKey("activity_logs.id"))
    detected_at = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(Text)
    optimization_suggestion = Column(Text, nullable=True)
