from flask_restful import Api
from .resources import CommentListResource, CommentReplyResource, CommentResource

def register_routes(bp):
    api = Api(bp)
    
    api.add_resource(CommentListResource, "/post/<uuid:post_id>/")
    api.add_resource(CommentResource, "/<uuid:comment_id>/")
    api.add_resource(CommentReplyResource, "/<uuid:comment_id>/replies/")