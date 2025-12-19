from flask import Blueprint, request, jsonify
from flask_restful import API, Resource
from app.blueprints.auth.service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User


auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth/")
api = API(auth_bp)


class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        result, status = AuthService.register_user(data)
        return jsonify(result), status
    
    
class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        result, status = AuthService.login_user(data)
        return jsonify(result), status
    
    
class LogoutResource(Resource):
    def post(self):
        data = AuthService.login_user()
        return jsonify(data)
    
    
class TokenRefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        data = AuthService.refresh(identity)
        return jsonify(data)
    
    
class PasswordResetRequestResource(Resource):
    def post(self):
        data = request.get_json()
        result, status = AuthService.request_password_reset(data)
        return jsonify(result), status
    
    
class PasswordResetConfirmResource(Resource):
    def post(self):
        data = request.get_json()
        result, status = AuthService.reset_password(data)
        return jsonify(result), status
    
    
class CurrentUserResource(Resource):
    @jwt_required
    def get(self):
        identity = get_jwt_identity()
        user = User.query.get(identity)
        data = AuthService.user_payload(user)
        return jsonify(data), 200
    
    
api.add_resource(RegisterResource, "/register/")
api.add_resource(LoginResource, "/login/")
api.add_resource(LogoutResource, "/logout/")
api.add_resource(TokenRefreshResource, "/token/refresh/")
api.add_resource(PasswordResetRequestResource, "/password/reset/")
api.add_resource(PasswordResetConfirmResource, "/password/reset/confirm")
api.add_resource(CurrentUserResource, "/user/")