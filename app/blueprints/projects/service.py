from datetime import datetime
from flask import abort
from app import db
from app.models import Project, ProjectVote, ProjectStatus
from uuid import UUID


class ProjectService:
    
    @staticmethod
    def is_valid_uuid(val):
        try:
            UUID(str(val))
            return True
        except ValueError:
            return False
    
    
    @staticmethod
    def create_project(data, user_id):
        
        if not ProjectService.is_valid_uuid(data.get("community_id")):
            return {"message": "Invalid or missing community_id"}, 400
        
        project = Project(
            title=data["title"],
            problem_statement=data["problem_statement"],
            proposed_solution=data["proposed_solution"],
            sector=data["sector"],
            proposal_deadline=datetime.fromisoformat(data["proposal_deadline"]),
            owner_id=user_id,
            community_id=data["community_id"],
        )
        db.session.add(project)
        db.session.commit()
        return {
            "message": "Project Created successfully",
            "Details": project.to_dict()
        }, 201
        
        
    @staticmethod
    def list_projects():
        return Project.query.order_by(
            Project.created_at.desc()
        ).all()
        
        
    @staticmethod
    def get_project(project_id):
        return Project.query.get_or_404(project_id)
    
    
    @staticmethod
    def update_project(project, data, user_id):
        if project.owner_id != user_id:
            abort(403, "Not authorized")
            
        if project.status != ProjectStatus.PROPOSED:
            abort(400, "Cannot modify project after proposal phase")
                    
        for field in ["title", "problem_statement", "proposed_solution", "sector"]:
            if field in data:
                setattr(project, field, data[field])
                
        db.session.commit()
        return project
    
    
    @staticmethod
    def delete_project(project, user_id):
        if project.owner_id != user_id:
            abort(403, "Not authorized")
            
        db.session.delete(project)
        db.session.commit()
        
        
    @staticmethod
    def vote(project, user_id, value):
        # ensure voting still open
        if project.proposal_deadline < datetime.utcnow():
            abort(400, "Voting period has ended")

        existing_vote = ProjectVote.query.filter_by(
            user_id=user_id,
            project_id=project.id
        ).first()

        # user changing vote
        if existing_vote:
            # remove old
            project.vote_score -= existing_vote.value

            # if same vote value, treat as remove
            if existing_vote.value == value:
                db.session.delete(existing_vote)
                db.session.commit()

                return {
                    "message": "Vote removed",
                    "new_score": project.vote_score,
                    "user_vote": None
                }, 200

            # otherwise update
            existing_vote.value = value
            project.vote_score += value

            db.session.commit()
            return {
                "message": "Vote updated",
                "new_score": project.vote_score,
                "user_vote": existing_vote.value
            }, 200

        # new vote
        new_vote = ProjectVote(
            user_id=user_id,
            project_id=project.id,
            value=value
        )
        db.session.add(new_vote)
        project.vote_score += value
        db.session.commit()

        return {
            "message": "Vote cast successfully",
            "new_score": project.vote_score,
            "user_vote": value
        }, 201

    
    
    @staticmethod
    def transition(project, new_status, user_id):
        if project.owner_id != user_id:
            abort(403, "Only project owner can transition")
            
        valid_transitions = {
            ProjectStatus.PROPOSED: [ProjectStatus.APPROVED, ProjectStatus.REJECTED],
            ProjectStatus.APPROVED: [ProjectStatus.RECRUITING],
            ProjectStatus.RECRUITING: [ProjectStatus.ACTIVE],
            ProjectStatus.ACTIVE: [ProjectStatus.COMPLETED],
        }
        
        if new_status not in valid_transitions.get(project.status, []):
            abort(400, "Invalid project state transition")
            
        project.status = new_status
        db.session.commit()
        return project
        