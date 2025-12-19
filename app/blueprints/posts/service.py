from app import db
from app.models import Post, CommunityMembership

ALLOWED_POST_TYPES = {"discussion", "proposal"}

class PostService:
    
    @staticmethod
    def create_post(user, community, data):
        title = data.get("title")
        content = data.get("content")
        post_type = data.get("post_type", "discussion")
        
        if not title or not content:
            return {
                "message": "Title and content are required"
            }, 400
            
        if post_type not in ALLOWED_POST_TYPES:
            return {
                "message": "Invalid post type"
            }, 400
            
        membership = CommunityMembership.query.filter_by(
            user_id=user.id,
            community_id=community.id
        ).first()
        
        if not membership:
            return {
                "message": "Join a community to start posting"
            }, 403
            
        post = Post(
            title=title,
            content=content,
            post_type=post_type,
            author_id=user.id,
            community_id=community.id
        )
        
        db.session.add(post)
        db.session.commit()
        
        return {
            "message": "Post created successfully",
            "post_id": str(post.id)
        }, 201
        
        
    @staticmethod
    def list_posts(community, post_type=None):
        query = Post.query.filter_by(community_id=community.id)
        
        if post_type:
            query = query.filter_by(post_type=post_type)
            
        posts = query.order_by(Post.created_at.desc()).all()
        
        return [
            {
                "id": str(p.id),
                "title": p.title,
                "post_type": p.post_type,
                "score": p.score,
                "author": p.author.username,
                "created_at": p.created_at.isoformat()
            }
            for p in posts
        ]