from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Community, Post
from app.blueprints.posts.service import PostService


posts_bp = Blueprint("posts", __name__)
api = Api(posts_bp)


class PostListCreateResource(Resource):
    @jwt_required(optional=True)
    def get(self, slug):
        community = Community.query.filter_by(slug=slug).first_or_404()
        post_type = request.args.get("type")
        
        user = None
        if get_jwt_identity():
            user = User.query.get_or_404(get_jwt_identity())
            
        posts = PostService.list_posts(community, post_type)
        return [
            PostService.serialize_post(p, user)
            for p in posts
        ]
    
    @jwt_required()
    def post(self, slug):
        user = User.query.get_or_404(get_jwt_identity())
        community = Community.query.filter_by(slug=slug).first_or_404()
        data = request.get_json()
        
        response, status = PostService.create_post(user, community, data)
        return response, status
    
    
class PostDetailResource(Resource):
    @jwt_required(optional=True)
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        
        user = None
        if get_jwt_identity():
            user = User.query.get_or_404(get_jwt_identity())
            
        return PostService.serialize_post(post, user)
        
        
        
# endpoints
api.add_resource(PostListCreateResource, "/communities/<string:slug>/posts/")
api.add_resource(PostDetailResource, "/<uuid:post_id>/")