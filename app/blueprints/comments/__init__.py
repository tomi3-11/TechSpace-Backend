from flask import Blueprint

comments_bp = Blueprint("comments", __name__)

from .routes import register_routes
register_routes(comments_bp)