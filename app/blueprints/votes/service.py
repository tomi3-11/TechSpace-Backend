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
        
        if vote:
            # Same vote -> remove
            if vote.value == value:
                post.score -= value
                db.session.delete(vote)
                db.session.commit()
                return {
                    "message": "Vote removed"
                }, 200
                
            # Change vote
            post.score -= vote.value
            vote.value = value
            post.score += value
            db.session.commit()
            return {
                "message": "Vote updated"
            }, 200
            
        # New Vote
        vote = Vote(
            user_id=user.id,
            post_id=post.id,
            value=value
        )
        
        post.score += value
        db.session.add(value)
        db.session.commit()
        
        return {
            "message": "Vote recorded"
        }, 201