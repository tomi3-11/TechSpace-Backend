from app import db
from app.models import Vote, Post

ALLOW_VALUES = {1, -1}


class VoteService:
    
    @staticmethod
    def cast_vote(user, post, value):
        if value not in ALLOW_VALUES:
            return {
                "message": "Invalid vote value"
            }, 400
            
        vote = Vote.query.filter_by(user_id=user.id, post_id=post.id).first()
        
        def format_response(message, user_vote):
            return {
                "message": message,
                "new_score": post.score,
                "user_vote": user_vote
            }
        
        if vote:
            # Same vote -> remove
            if vote.value == value:
                post.score -= value
                db.session.delete(vote)
                db.session.commit()
                return format_response("Vote removed", 0), 200
                
            # Change vote
            post.score -= vote.value
            vote.value = value
            post.score += value
            db.session.commit()
            return format_response("Vote Updated", value), 200
            
        # New Vote
        vote = Vote(
            user_id=user.id,
            post_id=post.id,
            value=value
        )
        
        post.score += value
        db.session.add(vote)
        db.session.commit()
        
        return format_response("Vote recorded", value), 201