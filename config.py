import os
import secrets
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATION = False
    
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    
    # Mail configs
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    # Cache configs
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = os.environ.get("REDIS_URL")
    
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)     
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)     
    
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
