from flask import Blueprint
from .routes import register_routes

projects_bp = Blueprint("projects", __name__)

register_routes(projects_bp)