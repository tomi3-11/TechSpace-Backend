from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from app.blueprints.feeds.service import FeedService


feeds_bp = Blueprint("feeds", __name__)
api = Api(feeds_bp)


def feed_response(pagination):
    return jsonify({
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
        "results": [
            post.to_dict() for post in pagination.items
        ]
    })
    
    
class LatestFeedResource(Resource):
    def get(self):
        page = request.args.get("page", 1, int)
        per_page = request.args.get("per_page", 20, int)
        post_type = request.args.get("type")
        
        data = FeedService.latest(
            page, per_page, post_type
        )
        
        return feed_response(data)
    
    
class TopFeedResource(Resource):
    def get(self):
        page = request.args.get("page", 1, int)
        per_page = request.args.get("per_page", 20, int)
        
        return feed_response(
            FeedService.top(page, per_page)
        )
        
        
class TrendingFeedResource(Resource):
    def get(self):
        page = request.args.get("page", 1, int)
        per_page = request.args.get("per_page", 20, int)
        
        return feed_response(
            FeedService.trending(page, per_page)
        )
        
        
class ProposalFeedResource(Resource):
    def get(self):
        page = request.args.get("page", 1, int)
        per_page = request.args.get("per_page", 20, int)
        
        return feed_response(
            FeedService.proposals(page, per_page)
        )
        
        
class CommunityFeedResource(Resource):
    def get(self, slug):
        page = request.args.get("page", 1, int)
        per_page = request.args.get("per_page", 20, int)
        
        return feed_response(
            FeedService.community(slug, page, per_page)
        )
        
        
# endpoints
api.add_resource(LatestFeedResource, "/latest/")
api.add_resource(TopFeedResource, "/top/")
api.add_resource(TrendingFeedResource, "/trending/")
api.add_resource(ProposalFeedResource, "/proposals/")
api.add_resource(CommunityFeedResource, "/community/<string:slug>/")