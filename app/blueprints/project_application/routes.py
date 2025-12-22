from flask_restful import Api
from .resources import ProjectApplicationCreateResource, SingleApplicationResource, CurrentUserApplicationsResource, ProjectReviewApplicationReviewResource

def register_routes(bp):
    api = Api(bp)
    
    # Endpoints
    api.add_resource(ProjectApplicationCreateResource, "/")
    api.add_resource(ProjectReviewApplicationReviewResource, "/<int:project_id>/review/")
    api.add_resource(SingleApplicationResource, "/<int:project_id>/")
    api.add_resource(CurrentUserApplicationsResource, "/mine/")