from sqlalchemy import desc, func
from app.models import Post, Community, Vote 

class FeedService:
    """
    Docstring for FeedService
    Read-only aggregation service.
    Injects 'user_vote' state for the requesting user.
    """
    
    @staticmethod
    def paginate(query, page, per_page, user_id=None):
        """
        Executes pagination AND injects user_vote status if user_id is provided.
        """
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        if user_id and pagination.items:
            post_ids = [post.id for post in pagination.items]
            
            votes = Vote.query.filter(
                Vote.user_id == user_id,
                Vote.post_id.in_(post_ids)
            ).all()
            
            vote_map = {vote.post_id: vote.value for vote in votes}
            
            for post in pagination.items:
                post.user_vote = vote_map.get(post.id, 0)
        else:
            for post in pagination.items:
                post.user_vote = 0
                
        return pagination
    
    
    @classmethod
    def latest(cls, page, per_page, post_type=None, user_id=None):
        query = Post.query.filter(Post.is_active.is_(True))
        
        if post_type:
            query = query.filter(Post.post_type == post_type)
            
        return cls.paginate(
            query.order_by(Post.created_at.desc()),
            page,
            per_page,
            user_id 
        )
        
        
    @classmethod
    def top(cls, page, per_page, user_id=None):
        query = Post.query.filter(Post.is_active.is_(True))
        
        return cls.paginate(
            query.order_by(Post.score.desc()),
            page,
            per_page,
            user_id
        )
        
    
    @classmethod
    def trending(cls, page, per_page, user_id=None):
        """
        Trending = score / hours_since_posted
        """
        
        hours_since = (
            func.extract("epoch", func.now() - Post.created_at) / 3600
        )
        
        rank = Post.score / func.nullif(hours_since, 1)
        
        query = Post.query.filter(Post.is_active.is_(True))
        
        return cls.paginate(
            query.order_by(desc(rank)),
            page,
            per_page,
            user_id
        )
        
        
    @classmethod
    def proposals(cls, page, per_page, user_id=None):
        query = Post.query.filter(
            Post.is_active.is_(True),
            Post.post_type == "proposal"
        )
        
        return cls.paginate(
            query.order_by(Post.score.desc()),
            page,
            per_page,
            user_id
        )
        
        
    @classmethod
    def community(cls, slug, page, per_page, user_id=None):
        community = Community.query.filter_by(slug=slug).first_or_404()
        
        query = Post.query.filter(
            Post.community_id == community.id,
            Post.is_active.is_(True)
        )
        
        return cls.paginate(
            query.order_by(Post.created_at.desc()),
            page,
            per_page,
            user_id
        )