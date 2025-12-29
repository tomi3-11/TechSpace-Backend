from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS
from redis import Redis
import os


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)
scheduler = BackgroundScheduler()
redis_client = Redis(
    host=os.environ.get("REDIS_HOST"),
    port=os.environ.get("REDIS_PORT"),
    db=os.environ.get("REDIS_DB"),
    socket_timeout=5
)


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # Enable CORS
    CORS(
        app,
        resources={r"/api/v1/*": {"origins": [
            "https://techmspace.dev",
            "https://www.techmspace.dev",
            "http://localhost:3000"
            ]}},
        supports_credentials=True
    )
    
    
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    
    if not app.config.get("TESTING"):
        scheduler.start()
    
    # Register versioned Blueprints
    from app.blueprints.v1 import v1_bp
    
    app.register_blueprint(v1_bp, url_prefix="/api/v1")
    
    return app
