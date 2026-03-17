import os
import time
import base64
import sys
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Add parent dir to path to import api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api import models
from api.database import SessionLocal, engine
from langchain_community.llms import Ollama
import json

load_dotenv()

models.Base.metadata.create_all(bind=engine)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
VISION_MODEL = os.getenv("OLLAMA_VISION_MODEL", "llava")

class AIProcessor:
    def __init__(self):
        print(f"Initializing AI Processor with model {VISION_MODEL} at {OLLAMA_BASE_URL}")
        self.llm = Ollama(model=VISION_MODEL, base_url=OLLAMA_BASE_URL)
        
    def image_to_base64(self, image_path):
        try:
            with open(image_path, "rb") as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            print(f"Error reading image {image_path}: {e}")
            return None

    def process_unclustered_logs(self):
        db = SessionLocal()
        try:
            # Get logs without a cluster, try to group them by user/time
            logs = db.query(models.ActivityLog).filter(models.ActivityLog.cluster_id == None).order_by(models.ActivityLog.timestamp.asc()).limit(10).all()
            
            if not logs:
                return
                
            print(f"Processing {len(logs)} unclustered logs...")
            
            # For a real system we would batch these intelligently. Here we'll treat the batch as one sequence.
            # Convert images
            images_b64 = []
            log_details = ""
            for i, log in enumerate(logs):
                b64 = self.image_to_base64(log.image_path)
                if b64:
                    images_b64.append(b64)
                    log_details += f"Step {i+1}: App: {log.app_name}, Keystrokes: {log.key_strokes}\n"

            if not images_b64:
                return

            print("Prompting LLM with visual and keyboard context...")
            
            # In a real implementation using langchain for multimodality with Ollama:
            prompt = f"""
            Analyze this sequence of user actions and the provided screenshots.
            {log_details}
            
            1. What is the user trying to accomplish? (Provide a short title/name)
            2. Provide a brief description of this process.
            3. Are there any steps that seem like context switches / interruptions (e.g., checking email, replying to a message) that are entirely unrelated to the main task?
            
            Return ONLY a JSON object in this format:
            {{"name": "Task Name", "description": "task description", "interruption_step_indices": [index1, index2]}}
            Where the indices match the 0-based array of the provided steps.
            """
            
            # Assuming llm.invoke takes images in standard langchain format (Note: Langchain community Ollama might need specific prompt formatting for images, bypassing that for brevity here and mocking response parsing)
            try:
                # Mocking the actual vision call for now to prevent local LLM crashes unless the user really has llava running
                # response = self.llm.invoke(prompt, images=images_b64) 
                
                # We'll simulate a response for testing
                res_dict = {
                    "name": "General Web Browsing",
                    "description": "User is navigating the web and typing.",
                    "interruption_step_indices": [1] # E.g., step 2 was checking email
                }
                
                # Create a cluster
                cluster = models.SequenceCluster(
                    name=res_dict["name"],
                    description=res_dict["description"]
                )
                db.add(cluster)
                db.commit()
                db.refresh(cluster)
                
                interruptions = res_dict.get("interruption_step_indices", [])
                
                # Assign to logs
                for i, log in enumerate(logs):
                    log.cluster_id = cluster.id
                    if i in interruptions:
                         log.is_interruption = True
                db.commit()
                
                print(f"Created resilient cluster: {cluster.name} (ID: {cluster.id}) with {len(interruptions)} identified interruptions.")
                
            except Exception as e:
                print(f"Error calling LLM: {e}")
                
        finally:
            db.close()

    def detect_anomalies(self):
        db = SessionLocal()
        try:
            # Fetch recent logs that have been clustered to an APPROVED cluster
            # Compare current actions with intended SOP.
            pass # Implementation for anomaly detection comparison
        finally:
            db.close()

    def run(self):
        while True:
            self.process_unclustered_logs()
            self.detect_anomalies()
            time.sleep(30)

if __name__ == "__main__":
    processor = AIProcessor()
    processor.run()
