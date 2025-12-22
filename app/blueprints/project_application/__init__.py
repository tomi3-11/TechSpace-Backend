from flask import Blueprint
from .routes import register_routes

project_applications_bp = Blueprint("applications", __name__, url_prefix="/api/v1/applications/")

register_routes(project_applications_bp)