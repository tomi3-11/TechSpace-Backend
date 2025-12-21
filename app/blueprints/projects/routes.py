from flask_restful import Api
from .resources import ProjectListResource, ProjectResource, ProjectTransitionResource, ProjectVoteResource

def register_routes(bp):
    api = Api(bp)
    
    # Endpoints
    api.add_resource(ProjectListResource, "/")
    api.add_resource(ProjectResource, "/<int:project_id>/")
    api.add_resource(ProjectVoteResource, "/<int:project_id>/vote/")
    api.add_resource(ProjectTransitionResource, "/<int:project_id>/transition/")