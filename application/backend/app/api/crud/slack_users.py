from flask import views
from flask_smorest import Blueprint, abort
from app.models.slack_user import SlackUser, SlackUserSchema, SlackUserUpdateSchema, SlackUserQueryArgsSchema
from flask_jwt_extended import jwt_required

bp = Blueprint("users", "users", url_prefix="/users", description="Operations on users")

@bp.route("/")
class SlackUsers(views.MethodView):
    @bp.arguments(SlackUserQueryArgsSchema, location="query")
    @bp.response(200, SlackUserSchema(many=True))
    @bp.paginate()
    def get(self, args, pagination_parameters):
        """List slack_users"""
        total, slack_users = SlackUser.get(filters = args, order_by = SlackUser.current_username.asc, page = pagination_parameters.page, per_page = pagination_parameters.page_size)
        pagination_parameters.item_count = total
        return slack_users

@bp.route("/<slack_user_id>")
class SlackUsersById(views.MethodView):
    @bp.response(200, SlackUserSchema)
    def get(self, slack_user_id):
        """Get slack_user by ID"""
        slack_user = SlackUser.get_by_id(slack_user_id)
        if slack_user == None:
            abort(404, message = "User not found.")
        return slack_user

    @bp.arguments(SlackUserUpdateSchema)
    @bp.response(200, SlackUserSchema)
    @jwt_required()
    def put(self, update_data, slack_user_id):
        """Update existing user"""
        slack_user = SlackUser.get_by_id(slack_user_id)
        if slack_user == None:
            abort(422, message = "User not found.")
        updated_slack_user_id = SlackUserSchema().load(data=update_data, instance=slack_user, partial=True)
        SlackUser.upsert(updated_slack_user_id)
        return updated_slack_user_id