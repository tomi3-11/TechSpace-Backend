from app import db
from app.models import Community, CommunityMembership
from slugify import slugify


class CommunityService:
    
    @staticmethod
    def create_community(user, data):
        name = data.get("name")
        description = data.get("description", "")
        
        if not name:
            return {
                "message": "Community name is required",
            }, 400
            
        slug = slugify(name)
        
        if Community.query.filter_by(slug=slug).first():
            return {
                "message": "Community already exists"
            }, 400
            
            
        community = Community(
            name=name,
            slug=slug,
            description=description,
            creator_id=user.id
        )
        
        db.session.add(community)
        db.session.flush()
        
        membership = CommunityMembership(
            user_id=user.id,
            community_id=community.id,
            role="owner"
        )
        db.session.add(membership)
        db.session.commit()
        
        return {
            "message": "Comminuty created successfully",
            "slug": slug
        }, 201