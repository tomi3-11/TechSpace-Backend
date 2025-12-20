from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Post
from app.blueprints.votes.service import VoteService


vote_bp = Blueprint("votes", __name__, url_prefix="/api/v1/votes/")
api = Api(vote_bp)


class PostVoteResource(Resource):
    @jwt_required()
    def post(self, post_id):
        user = User.query.get_or_404(get_jwt_identity())
        post = Post.query.get_or_404(post_id)
        
        data = request.get_json()
        value = data.get("value")
        
        response, status = VoteService.cast_vote(user, post, value)
        return response, status
    
    
# Endpoints
api.add_resource(PostVoteResource, "/posts/<uuid:post_id>/vote/")