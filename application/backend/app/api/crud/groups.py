from flask import views
from flask_smorest import Blueprint, abort
from app.models.group_schema import GroupCreateSchema, GroupResponseSchema, GroupUpdateSchema
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from app.services.injector import injector
from app.services.group_service import GroupService

bp = Blueprint("groups", "groups", url_prefix="/groups", description="Operations on groups")

@bp.route("/")
class Groups(views.MethodView):
    @bp.response(200, GroupResponseSchema(many=True))
    @bp.paginate()
    @jwt_required()
    def get(self, pagination_parameters):
        """List groups"""
        group_service = injector.get(GroupService)
        total, groups = group_service.get(page=pagination_parameters.page, per_page=pagination_parameters.page_size, team_id=current_user.slack_organization_id)
        pagination_parameters.item_count = total
        return groups

    @bp.arguments(GroupCreateSchema)
    @bp.response(201, GroupResponseSchema)
    @jwt_required()
    def post(self, new_data):
        """Add a group"""
        group_service = injector.get(GroupService)
        new_group = group_service.add(data=new_data, team_id=current_user.slack_organization_id)
        return new_group

@bp.route("/<group_id>")
class GroupsById(views.MethodView):
    @bp.response(200, GroupResponseSchema)
    @jwt_required()
    def get(self, group_id):
        """Get group by ID"""
        group_service = injector.get(GroupService)
        group = group_service.get_by_id(group_id=group_id, team_id=current_user.slack_organization_id)
        if group is None:
            abort(404, message="Group not found.")
        return group

    @bp.arguments(GroupUpdateSchema)
    @bp.response(200, GroupResponseSchema)
    @jwt_required()
    def patch(self, update_data, group_id):
        """Update group by ID"""
        group_service = injector.get(GroupService)
        updated_group = group_service.update(group_id=group_id, data=update_data, team_id=current_user.slack_organization_id)
        if updated_group is None:
            abort(404, message="Group not found.")
        return updated_group

    @bp.response(204)
    @jwt_required()
    def delete(self, group_id):
        """Delete group"""
        group_service = injector.get(GroupService)
        success = group_service.delete(group_id=group_id, team_id=current_user.slack_organization_id)
        if not success:
            abort(400, message="Something went wrong.")
