import uuid
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from flask_mail import Message
from app import db, mail
from app.models import User

AVATAR_API = "https://ui-avatars.com/api/?name={}&background=random"


class AuthService:
    
    @staticmethod
    def register_user(data):
        if User.query.filter_by(email=data["email"]).first():
            return {
                "message": "Email already exists"
            }, 400
            
        avatar_url = AVATAR_API.format(data["username"])
        
        user = User(
            username=data["username"],
            email=data["email"],
            avatar_url=avatar_url
        )
        user.set_password(data["password"])
        
        db.session.add(user)
        db.session.commit()
        
        return {
            "message": "User registered successfully"
        }, 201
        
        
    @staticmethod
    def login_user(data):
        user = User.query.filter_by(email=data["email"]).first()
        if not user or not user.check_password(data["password"]):
            return {
                "message": "Invalid credentials"
            }, 401
            
            
        token = create_access_token(identity=str(user.id))
        return {
            "access_token": token
        }, 200
        
        
    @staticmethod
    def request_password_reset(data):
        user = User.query.filter_by(email=data["email"]).first()
        if not user:
            return {
                "message": "User not found"
            }, 404
            
        token = str(uuid.uuid4())
        user.reset_token = token
        user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=30)
        
        db.session.commit()
        
        msg = Message(
            subject="Password Reset",
            recipients=[user.email],
            body=f"Use this token to reset your password: {token}"
        )
        mail.send(msg)
        
        return {
            "message": "Password reset email sent"
        }, 200
        
        
    @staticmethod
    def reset_password(data):
        user = User.query.filter_by(reset_token=data["token"]).first()
        
        if not user or user.reset_token_expiry < datetime.utcnow():
            return {
                "message": "Invalid or expired token"
            }, 400
            
        user.set_password(data["new_password"])
        user.reset_token = None
        user.reset_token_expiry = None
        
        db.session.commit()
        return {
            "message": "Password reset successfully"
        }, 200