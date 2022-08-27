from flask import views
from flask_smorest import Blueprint, abort
from app.models.invitation import Invitation, InvitationSchema, InvitationUpdateSchema, InvitationQueryArgsSchema
from flask_jwt_extended import jwt_required

bp = Blueprint("invitations", "invitations", url_prefix="/invitations", description="Operations on invitations")

@bp.route("/")
class Invitations(views.MethodView):
    @bp.arguments(InvitationQueryArgsSchema, location="query")
    @bp.response(200, InvitationSchema(many=True))
    @bp.paginate()
    def get(self, args, pagination_parameters):
        """List invitations"""
        total, invitations = Invitation.get(filters = args, page = pagination_parameters.page, per_page = pagination_parameters.page_size)
        pagination_parameters.item_count = total
        return invitations

@bp.route("/<event_id>")
class InvitationsById(views.MethodView):
    @bp.response(200, InvitationSchema(many=True))
    def get(self, event_id):
        """Get invitation by ID"""
        invitations = Invitation.get_by_filter({"event_id": event_id})
        return invitations

@bp.route("/<event_id>/<user_id>")
class InvitationsById(views.MethodView):
    @bp.response(200, InvitationSchema)
    def get(self, event_id, user_id):
        """Get invitation by ID"""
        invitation = Invitation.get_by_id((event_id, user_id))
        if invitation == None:
            abort(404, message = "Invitation not found.")
        return invitation
    
    @bp.arguments(InvitationUpdateSchema)
    @bp.response(200, InvitationSchema)
    @jwt_required()
    def put(self, update_data, event_id, user_id):
        """Update existing invitation"""
        invitation = Invitation.get_by_id((event_id, user_id))
        if invitation == None:
            abort(422, message = "Invitation not found.")
        updated_invitation = InvitationSchema().load(data=update_data, instance=invitation, partial=True)
        Invitation.upsert(updated_invitation)
        return updated_invitation