from flask import views
from flask_smorest import Blueprint, abort
from app.models.slack_user_schema import SlackUserResponseSchema, SlackUserUpdateSchema, SlackUserQueryArgsSchema
from flask_jwt_extended import jwt_required, current_user
from app.services.injector import injector
from app.services.slack_user_service import SlackUserService

bp = Blueprint("users", "users", url_prefix="/users", description="Operations on users")

@bp.route("/")
class SlackUsers(views.MethodView):
    @bp.arguments(SlackUserQueryArgsSchema, location="query")
    @bp.response(200, SlackUserResponseSchema(many=True))
    @bp.paginate()
    @jwt_required()
    def get(self, args, pagination_parameters):
        """List slack_users"""
        slack_user_service = injector.get(SlackUserService)
        total, slack_users = slack_user_service.get(filters=args, page=pagination_parameters.page, per_page=pagination_parameters.page_size, order_by_ascending=True, team_id=current_user.slack_organization_id)
        pagination_parameters.item_count = total
        return slack_users

@bp.route("/<slack_user_id>")
class SlackUsersById(views.MethodView):
    @bp.response(200, SlackUserResponseSchema)
    @jwt_required()
    def get(self, slack_user_id):
        """Get slack_user by ID"""
        slack_user_service = injector.get(SlackUserService)
        slack_user = slack_user_service.get_by_id(slack_user_id=slack_user_id, team_id=current_user.slack_organization_id)
        if slack_user is None:
            abort(404, message = "User not found.")
        return slack_user

    @bp.arguments(SlackUserUpdateSchema)
    @bp.response(200, SlackUserResponseSchema)
    @jwt_required()
    def put(self, update_data, slack_user_id):
        """Update existing user"""
        slack_user_service = injector.get(SlackUserService)
        updated_slack_user = slack_user_service.update(slack_user_id=slack_user_id, data=update_data, team_id=current_user.slack_organization_id)
        if updated_slack_user is None:
            abort(422, message = "User not found.")
        return updated_slack_user
