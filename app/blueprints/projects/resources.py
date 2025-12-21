from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import ProjectStatus, User
from app.blueprints.projects.service import ProjectService


class ProjectListResource(Resource):
    def get(self):
        projects = ProjectService.list_projects()
        return jsonify([p.to_dict() for p in projects])
    
    @jwt_required()
    def post(self):
        user = User.query.get_or_404(get_jwt_identity())
        data = request.get_json()
        project, status = ProjectService.create_project(data, user.id)
        return project, status
    
    
class ProjectResource(Resource):
    def get(self, project_id):
        project = ProjectService.get_project(project_id)
        return jsonify(project.to_dict())
    
    @jwt_required()
    def put(self, project_id):
        user = User.query.get_or_404(get_jwt_identity())
        data = request.get_json()
        project = ProjectService.get_project(project_id)
        updated = ProjectService.update_project(project, data, user.id)
        return jsonify(updated.to_dict())
    
    @jwt_required()
    def delete(self, project_id):
        user = User.query.get_or_404(get_jwt_identity())
        project = ProjectService.get_project(project_id)
        ProjectService.delete_project(project, user.id)
        return {
            "message": "Project withdrawn"
        }, 200
        
        
class ProjectVoteResource(Resource):
    @jwt_required()
    def post(self, project_id):
        user = User.query.get_or_404(get_jwt_identity())
        data = request.get_json()
        value = data.get("value")
        project = ProjectService.get_project(project_id)
        score = ProjectService.vote(project, user.id, value)
        return {
            "vote_score": score
        }, 200
        
        
class ProjectTransitionResource(Resource):
    @jwt_required()
    def post(self, project_id):
        user = User.query.get_or_404(get_jwt_identity())
        data = request.get_json()
        status_str = data.get("status")
        new_status = ProjectStatus(status_str)
        
        project = ProjectService.get_project(project_id)
        updated = ProjectService.transition(project, new_status, user.id)
        return jsonify(updated.to_dict())
        
        