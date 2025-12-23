from flask import Blueprint

v1_bp = Blueprint("api_v1", __name__)

# Register Blueprints
from app.blueprints.auth.routes import auth_bp
from app.blueprints.communities.routes import communities_bp
from app.blueprints.posts.routes import posts_bp
from app.blueprints.votes.routes import vote_bp
from app.blueprints.feeds.routes import feeds_bp
from app.blueprints.comments import comments_bp
from app.blueprints.projects import projects_bp
from app.blueprints.project_application import project_applications_bp
from app.blueprints.health import health_bp


v1_bp.register_blueprint(auth_bp, url_prefix="/auth/")
v1_bp.register_blueprint(communities_bp, url_prefix="/communities/")
v1_bp.register_blueprint(posts_bp, url_prefix="/posts/")
v1_bp.register_blueprint(vote_bp, url_prefix="/votes/")
v1_bp.register_blueprint(feeds_bp, url_prefix="/feeds/")
v1_bp.register_blueprint(comments_bp, url_prefix="/comments/")
v1_bp.register_blueprint(projects_bp, url_prefix="/projects/")
v1_bp.register_blueprint(project_applications_bp, url_prefix="/applications/")
v1_bp.register_blueprint(health_bp)