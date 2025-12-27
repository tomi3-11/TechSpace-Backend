from app import db
from app.models import Community, CommunityMembership
from slugify import slugify
from sqlalchemy import func


class CommunityService:
    
    @staticmethod
    def serialize_community(community, user=None):
        is_member = False
        if user:
            is_member = bool(
                CommunityMembership.query.filter_by(
                    user_id=user.id,
                    community_id=community.id
                ).first()
            )
            
        # total_members
        total_members = CommunityMembership.query.filter_by(
            community_id=community.id
        ).count()
            
        return {
            "id": community.id,
            "name": community.name,
            "slug": community.slug,
            "description": community.description,
            "created_at": community.created_at.isoformat(),
            "is_member": is_member,
            "total_members": total_members
        }
    
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
        
        
        
    @staticmethod
    def join_comminity(user, community):
        existing = CommunityMembership.query.filter_by(
            user_id=user.id,
            community_id=community.id
        ).first()
        
        if existing:
            return {
                "message": "Already a member"
            }, 400
            
        membership = CommunityMembership(
            user_id=user.id,
            community_id=community.id
        )
        db.session.add(membership)
        db.session.commit()
        
        return {
            "message": "Joined a community"
        }, 200
        
        
    @staticmethod
    def leave_community(user, community):
        membership = CommunityMembership.query.filter_by(
            user_id=user.id,
            community_id=community.id
        ).first()
        
        if not membership:
            return {
                "message": "Not a member"
            }, 400
            
        if membership.role == "owner":
            return {
                "message": "Owner cannot leave a community"
            }, 403
            
        db.session.delete(membership)
        db.session.commit()
        
        return {
            "message": "Left the community"
        }, 200
        
        
    @staticmethod
    def list_members(community):
        memberships = CommunityMembership.query.filter_by(
            community_id=community.id
        ).all()
        
        return [
            {
                "username": m.user.username,
                "role": m.role,
                "joined_at": m.joined_at.isoformat()
            }
            for m in memberships
        ]