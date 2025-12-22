from flask import Blueprint
from .routes import register_routes

project_applications_bp = Blueprint("applications", __name__)

register_routes(project_applications_bp)