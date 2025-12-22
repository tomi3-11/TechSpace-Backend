from flask_restful import Api
from .resources import ProjectApplicationCreateResource, CurrentUserApplicationsResource, ProjectApplicationReviewResource

def register_routes(bp):
    api = Api(bp)
    
    # Endpoints
    api.add_resource(ProjectApplicationCreateResource, "/projects/<int:project_id>/applications/")
    api.add_resource(ProjectApplicationReviewResource, "/projects/<int:project_id>/applications/<int:application_id>/review/")
    api.add_resource(CurrentUserApplicationsResource, "/mine/")