from app.models import ProjectApplication, Project
from flask import abort
from app import db
from datetime import datetime


class ProjectApplicationService:
    
    @staticmethod
    def apply(user_id, project_id, motivation, skills):
        project = Project.query.get_or_404(project_id)
        
        if project.status not in ("APPROVED", "ACTIVE"):
            abort(400, "Project not accepting applications")
            
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
    def get_application_list():
        return ProjectApplication.query.order_by(
            ProjectApplication.created_at.desc()
        ).all()
        
        
    @staticmethod
    def get_application(application_id):
        return ProjectApplication.query.get_or_404(application_id)
        
       
    @staticmethod
    def review(reviewer_id, application_id, decision):
        application = ProjectApplication.query.get_or_404(application_id)
        project = application.project
        
        if project.owner_id != reviewer_id:
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
    
    
        