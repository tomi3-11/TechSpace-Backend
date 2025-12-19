from flask import Blueprint, request, jsonify
from flask_restful import API, Resource
from app.blueprints.auth.service import AuthService


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
    
    
api.add_resource(RegisterResource, "/register")
api.add_resource(LoginResource, "/login")
api.add_resource(PasswordResetRequestResource, "/password-reset")
api.add_resource(PasswordResetConfirmResource, "/password-reset/confirm")