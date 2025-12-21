from flask import Blueprint
from .routes import register_routes

projects_bp = Blueprint("projects", __name__, url_prefix="/api/v1/projects/")

register_routes(projects_bp)