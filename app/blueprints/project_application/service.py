from app.models import ProjectApplication, Project, ProjectStatus
from flask import abort
from app import db
from datetime import datetime


class ProjectApplicationService:
    
    @staticmethod
    def apply(user_id, project_id, motivation, skills):
        project = Project.query.get_or_404(project_id)
        
        if project.status not in (ProjectStatus.APPROVED, ProjectStatus.ACTIVE):
            # abort(400, "Project not accepting applications")
            return {"message": "Project not accepting applications"}, 400
            
        existing = ProjectApplication.query.filter_by(
            user_id=user_id, project_id=project_id
        ).first()
        
        if existing:
            # abort(400, "User has already applied")
            return {"message": "User has already applied"}, 400
            
        application = ProjectApplication(
            user_id=user_id,
            project_id=project_id,
            motivation=motivation,
            skills=skills
        )
        
        db.session.add(application)
        db.session.commit()
        
        return application
        
        
    @staticmethod
    def get_application_for_project(project_id):
        return ProjectApplication.query.filter_by(
            project_id=project_id
        ).order_by(ProjectApplication.created_at.desc()).all()
        
       
    @staticmethod
    def review(reviewer_id, application_id, decision):
        application = ProjectApplication.query.get_or_404(application_id)
        project = application.project
        
        if (
            project.owner_id != reviewer_id or application.reviewer.role in ("MODERATOR", "ADMIN")
        ):
            abort(403, "Not authorized to review applications")
            
        if decision not in ("ACCEPTED", "REJECTED"):
            abort(400, "Invalid decision")
            
        application.status = decision
        application.reviewed_by_id = reviewer_id
        application.reviewed_at = datetime.utcnow()
        
        db.session.commit()
        return application
    
    @staticmethod
    def get_user_applications(user_id):
        return ProjectApplication.query.filter_by(user_id=user_id).order_by(
            ProjectApplication.created_at.desc()
        ).all()
    
    
        