from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Community, Post
from app.blueprints.posts.service import PostService


posts_bp = Blueprint("posts", __name__)
api = Api(posts_bp)


class PostListCreateResource(Resource):
    def get(self, slug):
        community = Community.query.filter_by(slug=slug).first_or_404()
        post_type = request.args.get("type")
        posts = PostService.list_posts(community, post_type)
        return posts
    
    @jwt_required()
    def post(self, slug):
        user = User.query.get_or_404(get_jwt_identity())
        community = Community.query.filter_by(slug=slug).first_or_404()
        data = request.get_json()
        
        response, status = PostService.create_post(user, community, data)
        return response, status
    
    
class PostDetailResource(Resource):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        
        return jsonify({
            "id": str(post.id),
            "title": post.title,
            "content": post.content,
            "post_type": post.post_type,
            "score": post.score,
            "author": post.author.username,
            "community": post.community.slug,
            "created_at": post.created_at.isoformat()
        })
        
        
        
# endpoints
api.add_resource(PostListCreateResource, "/communities/<string:slug>/posts/")
api.add_resource(PostDetailResource, "/<uuid:post_id>/")