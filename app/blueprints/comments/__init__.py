from flask import Blueprint

comments_bp = Blueprint("comments", __name__, url_prefix="/api/v1/comments/")

from .routes import register_routes
register_routes(comments_bp)