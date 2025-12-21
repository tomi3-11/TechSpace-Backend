from datetime import datetime
from app import db
import uuid
from werkzeug.security import check_password_hash, generate_password_hash
from enum import Enum


class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    role = db.Column(db.String(20), default="user")

    avatar_url = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
class Community(db.Model):
    __tablename__ = "communities"
    
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    creator_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    
class CommunityMembership(db.Model):
    __tablename__ = "community_memberships"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    community_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("communities.id"), nullable=False)
    role = db.Column(db.String(20), default="member")
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="community_memberships")
    community = db.relationship("Community", backref="memberships")

    __table_args__ = (
        db.UniqueConstraint("user_id", "community_id", name="unique_membership"),
    )
    
    
class Post(db.Model):
    __tablename__ = "posts"
    
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    post_type = db.Column(db.String(20), nullable=False, default="discussion")    
    author_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    community_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("communities.id"), nullable=False)
    
    score = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    author = db.relationship("User", backref="posts")
    community = db.relationship("Community", backref="posts")
    
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "type": self.post_type,
            "score": self.score,
            "author": self.author.username,
            "community": self.community.slug,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active
        }
    
    
class Vote(db.Model):
    __tablename__ = "votes"
    
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("posts.id"), nullable=False)
    value = db.Column(db.Integer, nullable=False) # +1 or -1
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint("user_id", "post_id", name="unique_user_post_vote"),
    )
    
    user = db.relationship("User", backref="votes")
    post = db.relationship("Post", backref="votes")
    
    
class Comment(db.Model):
    __tablename__ = "comments"
    
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    post_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("posts.id"),nullable=False)
    author_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    parent_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("comments.id"), nullable=True)
    
    post = db.relationship("Post", backref="comments")
    author = db.relationship("User")
    replies = db.relationship("Comment", backref=db.backref("parent", remote_side=[id]), lazy="dynamic")
    
    def to_dict(self, include_replies=True):
        data = {
            "id": self.id,
            "content": self.content,
            "author": self.author.username,
            "post_id": self.post_id,
            "parent_id": self.parent_id,
            "created_at": self.created_at.isoformat()
        }
        if include_replies:
            data["replies"] = [reply.to_dict() for reply in self.replies.order_by(Comment.created_at.asc())]
        return data
    
    
class ProjectStatus(Enum):
    PROPOSED = "PROPOSED"
    APPROVED = "APPROVED"
    RECRUITING = "RECRUITING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"
    
    
class Project(db.Model):
    __tablename__ = "projects"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    problem_statement = db.Column(db.Text, nullable=False)
    proposed_solution = db.Column(db.Text, nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    
    status = db.Column(
        db.Enum(ProjectStatus),
        default=ProjectStatus.PROPOSED,
        nullable=False
    )
    
    vote_score = db.Column(db.Integer, default=0)
    proposal_deadline = db.Column(db.DateTime, nullable=False)
    
    owner_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    community_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("communities.id"), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    owner = db.relationship("User", backref=db.backref("own_projects", lazy="dynamic"))
    community = db.relationship("Community", backref=db.backref("projects", lazy="dynamic"))
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "problem_statement": self.problem_statement,
            "proposed_solution": self.proposed_solution,
            "sector": self.sector,
            "status": self.status.value,
            "vote_score": self.vote_score,
            "proposal_deadline": self.proposal_deadline.isoformat(),
            "community": self.community.name if self.community else None,
            "owner": self.owner.username if self.owner else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class ProjectVote(db.Model):
    __tablename__ = "project_votes"
    
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint("user_id", "project_id", name="unique_project_vote"),
    )
