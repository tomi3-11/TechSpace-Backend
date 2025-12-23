from flask import Blueprint
from .routes import DataBaseRedisHealthResource
from flask_restful import Api

health_bp = Blueprint("health", __name__)
api = Api(health_bp)

api.add_resource(DataBaseRedisHealthResource, "/health")