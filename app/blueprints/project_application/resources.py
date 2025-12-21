from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, ProjectApplication
from .service import ProjectApplicationService


class ProjectApplicationCreateResource(Resource):
    @jwt_required()
    def post(self, project_id):
        user = User.query.get_or_404(get_jwt_identity())
        data = request.get_json()
        motivation=data.get("motivation")
        skills = data.get("skills")
        
        if not motivation or not skills:
            return {
                "message": "motivation and skills are required"
            }, 400
        
        application = ProjectApplicationService.apply(
            user.id, project_id, motivation, skills
        )
        
        return jsonify(application.to_dict()), 201
    
    def get(self):
        applications = ProjectApplicationService.get_application_list()
        return jsonify([a.to_dict() for a in applications]), 200
    
class SingleApplicationResource(Resource):
    def get(self, application_id):
        application = ProjectApplicationService.get_application(application_id)
        return jsonify(application.to_dict())
    
    
class ProjectReviewApplicationReviewResource(Resource):
    @jwt_required()
    def post(self, project_id, application_id):
        user = User.query.get_or_404(get_jwt_identity())
        data = request.get_json()
        decision = data.get("status")
        
        application = ProjectApplicationService(
            reviewer_id=user.id,
            application_id=application_id,
            decision=decision
        )
        
        return jsonify(application.to_dict()), 200
    
    
class CurrentUserApplicationsResource(Resource):
    @jwt_required()
    def get(self):
        user = User.query.get_or_404(get_jwt_identity())
        applications = ProjectApplicationService.get_user_applications(user.id)
        return jsonify([a.to_dic() for a in applications]), 200
        