from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.blueprints.comments.service import CommentService
from app.models import User


def comment_response(comment):
    return jsonify(comment.to_dict())


def comments_response(comments):
    return jsonify([comment.to_dict() for comment in comments])


class CommentListResource(Resource):
    @jwt_required()
    def post(self, post_id):
        user = User.query.get_or_404(get_jwt_identity())
        data = request.get_json()
        content = data.get("content")
        comment = CommentService.create_comment(user.id, post_id, content)
        return comment_response(comment)
    
    
    def get(self, post_id):
        comments = CommentService.get_comments(post_id)
        return comments_response(comments)
    
    
class CommentResource(Resource):
    @jwt_required()
    def put(self, comment_id):
        user = User.query.get_or_404(get_jwt_identity())
        data = request.get_json()
        content = data.get("content")
        comment = CommentService.update_comment(comment_id, user.id, content)
        return comment_response(comment)
    
    @jwt_required()
    def delete(self, comment_id):
        user = User.query.get_or_404(get_jwt_identity())
        CommentService.delete_comment(comment_id, user.id)
        return {
            "message": "Comment deleted successfully"
        }, 200
        
        
class CommentReplyResource(Resource):
    @jwt_required()
    def post(self, comment_id):
        user = User.query.get_or_404(get_jwt_identity())
        data = request.get_json()
        content = data.get("content")
        reply = CommentService.add_reply(comment_id, user.id, content)
        return comment_response(reply)
