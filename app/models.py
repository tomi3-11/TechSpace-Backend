from datetime import datetime
from app import db
import uuid
from werkzeug.security import check_password_hash, generate_password_hash

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