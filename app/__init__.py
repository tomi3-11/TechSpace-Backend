from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from apscheduler.schedulers.background import BackgroundScheduler


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)
scheduler = BackgroundScheduler()


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    
    scheduler.start()
    
    # Register Blueprints
    from app.blueprints.auth.routes import auth_bp
    from app.blueprints.communities.routes import communities_bp
    from app.blueprints.posts.routes import posts_bp
    from app.blueprints.votes.routes import vote_bp
    from app.blueprints.feeds.routes import feeds_bp
    
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(communities_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(vote_bp)
    app.register_blueprint(feeds_bp)
    
    return app