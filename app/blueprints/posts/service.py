from app import db
from app.models import Post, CommunityMembership, Vote

ALLOWED_POST_TYPES = {"discussion", "proposal"}

class PostService:
    
    @staticmethod
    def serialize_post(post, user=None):
        user_vote = None
        if user:
            vote = Vote.query.filter_by(
                user_id=user.id,
                post_id=post.id
            ).first()
            user_vote = vote.value if vote else None
            
        return {
            "id": str(post.id),
            "title": post.title,
            "content": post.content,
            "post_type": post.post_type,
            "score": post.score,
            "author": post.author.username,
            "community": post.community.slug,
            "created_at": post.created_at.isoformat(),
            "user_vote": user_vote
        }
    
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
            
        return query.order_by(Post.created_at.desc()).all()