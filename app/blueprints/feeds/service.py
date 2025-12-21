from sqlalchemy import desc, func
from app.models import Post, Community


class FeedService:
    """
    Docstring for FeedService
    Read-only aggregation service
    No mutations allowed.
    """
    
    @staticmethod
    def paginate(query, page, per_page):
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    
    @classmethod
    def latest(cls, page, per_page, post_type=None):
        query = Post.query.filter(Post.is_active.is_(True))
        
        if post_type:
            query = query.filter(Post.post_type == post_type)
            
        return cls.paginate(
            query.order_by(Post.created_at.desc()),
            page,
            per_page,
        )
        
        
    @classmethod
    def top(cls, page, per_page):
        query = Post.query.filter(Post.is_active.is_(True))
        
        return cls.paginate(
            query.order_by(Post.score.desc()),
            page,
            per_page
        )
        
    
    @classmethod
    def trending(cls, page, per_page):
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
            per_page
        )
        
        
    @classmethod
    def proposals(cls, page, per_page):
        query = Post.query.filter(
            Post.is_active.is_(True),
            Post.post_type == "proposal"
        )
        
        return cls.paginate(
            query.order_by(Post.score.desc()),
            page,
            per_page
        )
        
        
    @classmethod
    def community(cls, slug, page, per_page):
        community = Community.query.filter_by(slug=slug).first_or_404()
        
        query = Post.query.filter(
            Post.community_id == community.id,
            Post.is_active.is_(True)
        )
        
        return cls.paginate(
            query.order_by(Post.created_at.desc()),
            page,
            per_page
        )
