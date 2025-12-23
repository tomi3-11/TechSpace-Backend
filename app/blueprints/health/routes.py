from flask_restful import Resource
from sqlalchemy import text
from app import db, redis_client
from flask import jsonify


class DataBaseRedisHealthResource(Resource):
    def get(self):
        checks = {}
        
        # Database check
        try:
            db.session.execute(text("SELECT 1"))
            checks["database"] = "ok"
        except Exception:
            return {
                "status": "error", "database": "down"
            }, 500
            
        # Redis check
        try:
            # ping returns True if successful
            if redis_client.ping():
                checks["redis"] = "ok"
            else:
                checks["redis"] = "down"
        except Exception:
            return {
                "status": "error", "database": "down"
            }, 500
            
        return {"status": "ok", "checks": checks}, 200
    
    