from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.blueprints.feeds.service import FeedService

feeds_bp = Blueprint("feeds", __name__)
api = Api(feeds_bp)

def get_optional_user_id():
    try:
        verify_jwt_in_request(optional=True)
        return get_jwt_identity()
    except Exception:
        return None

def feed_response(pagination):
    results = []
    for post in pagination.items:
        data = post.to_dict()
        data['user_vote'] = getattr(post, 'user_vote', 0)
        results.append(data)

    return jsonify({
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
        "results": results
    })

class LatestFeedResource(Resource):
    def get(self):
        page = request.args.get("page", 1, int)
        per_page = request.args.get("per_page", 20, int)
        post_type = request.args.get("type")
        
        user_id = get_optional_user_id()
        
        return feed_response(
            FeedService.latest(page, per_page, post_type, user_id=user_id)
        )

class TopFeedResource(Resource):
    def get(self):
        page = request.args.get("page", 1, int)
        per_page = request.args.get("per_page", 20, int)
        
        user_id = get_optional_user_id()

        return feed_response(
            FeedService.top(page, per_page, user_id=user_id)
        )

class TrendingFeedResource(Resource):
    def get(self):
        page = request.args.get("page", 1, int)
        per_page = request.args.get("per_page", 20, int)
        
        user_id = get_optional_user_id()
        
        return feed_response(
            FeedService.trending(page, per_page, user_id=user_id)
        )

class ProposalFeedResource(Resource):
    def get(self):
        page = request.args.get("page", 1, int)
        per_page = request.args.get("per_page", 20, int)
        
        user_id = get_optional_user_id()
        
        return feed_response(
            FeedService.proposals(page, per_page, user_id=user_id)
        )

class CommunityFeedResource(Resource):
    def get(self, slug):
        page = request.args.get("page", 1, int)
        per_page = request.args.get("per_page", 20, int)
        
        user_id = get_optional_user_id()
        
        return feed_response(
            FeedService.community(slug, page, per_page, user_id=user_id)
        )

# Endpoints
api.add_resource(LatestFeedResource, "/latest/")
api.add_resource(TopFeedResource, "/top/")
api.add_resource(TrendingFeedResource, "/trending/")
api.add_resource(ProposalFeedResource, "/proposals/")
api.add_resource(CommunityFeedResource, "/community/<string:slug>/")