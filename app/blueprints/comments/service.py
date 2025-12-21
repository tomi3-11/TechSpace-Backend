from app.models import Comment, Post, db
from flask import abort
from flask_jwt_extended import get_jwt_identity


class CommentService:
    
    @staticmethod
    def create_comment(author_id, post_id, content, parent_id=None):
        post = Post.query.get_or_404(post_id)
        comment = Comment(
            content=content,
            author_id=author_id,
            post_id=post.id,
            parent_id=parent_id
        )
        db.session.add(comment)
        db.session.commit()
        return comment
    
    
    @staticmethod
    def get_comments(post_id):
        post = Post.query.get_or_404(post_id)
        
        comments = (
            Comment.query.filter_by(post_id=post_id, parent_id=None).order_by(Comment.created_at.asc()).all()
        )
        return comments
    
    
    @staticmethod
    def update_comment(comment_id, author_id, content):
        comment = Comment.query.get_or_404(comment_id)
        if comment.author_id != author_id:
            return {
               "message": "Not authorized to edit this comment" 
            }, 403
            
        comment.content = content
        db.session.commit()
        return comment
    
    
    @staticmethod
    def delete_comment(comment_id, author_id):
        comment = Comment.query.get_or_404(comment_id)
        if comment.author_id != author_id:
            abort(403, description="Not authorized to delete this comment")
            
        db.session.delete(comment)
        db.session.commit()
        return True
    
    
    @staticmethod
    def add_reply(comment_id, author_id, content):
        parent = Comment.query.get_or_404(comment_id)
        reply = Comment(
            content=content,
            author_id=author_id,
            post_id=parent.post_id,
            parent_id=parent.id
        )
        db.session.add(reply)
        db.session.commit()
        return reply