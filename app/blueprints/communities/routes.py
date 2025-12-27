from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Community
from app.blueprints.communities.service import CommunityService


communities_bp = Blueprint("communities", __name__)
api = Api(communities_bp)


class CommunityListResource(Resource):
    def get(self):
        user = None
        
        if get_jwt_identity():
            user = User.query.get_or_404(get_jwt_identity())
            
        communities = Community.query.all()
        return [
            CommunityService.serialize_community(c, user)git 
            for c in communities
        ]
        
        
    @jwt_required()
    def post(self):
        data = request.get_json()
        user = User.query.get_or_404(get_jwt_identity())
        response, status = CommunityService.create_community(user, data)
        return response, status
    
    
class CommunityDetailResource(Resource):
    def get(self, slug):
        community = Community.query.filter_by(slug=slug).first_or_404()
        
        return jsonify({
            "name": community.name,
            "slug": community.slug,
            "description": community.description,
            "created_at": community.created_at.isoformat()
        })
        
        
class CommunityJoinResource(Resource):
    @jwt_required()
    def post(self, slug):
        user = User.query.get_or_404(get_jwt_identity())
        community = Community.query.filter_by(slug=slug).first_or_404()
        response, status = CommunityService.join_comminity(user, community)
        return response, status


class CommunityLeaveResource(Resource):
    @jwt_required()
    def post(self, slug):
        user = User.query.get_or_404(get_jwt_identity())
        community = Community.query.filter_by(slug=slug).first_or_404()
        response, status = CommunityService.leave_community(user, community)
        
        return response, status
    
    
class CommunityMemberResource(Resource):
    def get(self, slug):
        community = Community.query.filter_by(slug=slug).first_or_404()
        members = CommunityService.list_members(community)
        return members
    
    
# Endpoints
api.add_resource(CommunityListResource, "/")
api.add_resource(CommunityDetailResource, "/<string:slug>/")
api.add_resource(CommunityJoinResource, "/<string:slug>/join/")
api.add_resource(CommunityLeaveResource, "/<string:slug>/leave/")
api.add_resource(CommunityMemberResource, "/<string:slug>/members/")