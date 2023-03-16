from flask import views
from flask_smorest import Blueprint, abort
from app.models.event_schema import EventCreateSchema, EventResponseSchema, EventQueryArgsSchema, EventUpdateSchema
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from app.services.injector import injector
from app.services.event_service import EventService
import json

bp = Blueprint("events", "events", url_prefix="/events", description="Operations on events")

@bp.route("/")
class Events(views.MethodView):
    @bp.arguments(EventQueryArgsSchema, location="query")
    @bp.response(200, EventResponseSchema(many=True))
    @bp.paginate()
    @jwt_required()
    def get(self, args, pagination_parameters):
        """List events"""
        event_service = injector.get(EventService)
        total, events = event_service.get(filters=args, page=pagination_parameters.page, per_page=pagination_parameters.page_size, team_id=current_user.slack_organization_id)
        pagination_parameters.item_count = total
        return events

    @bp.arguments(EventCreateSchema)
    @bp.response(201, EventResponseSchema)
    @jwt_required()
    def post(self, new_data):
        """Add an event"""
        event_service = injector.get(EventService)
        new_event = event_service.add(data=new_data, team_id=current_user.slack_organization_id)
        if new_event is None:
            abort(400, message="Something went wrong.")
        return new_event

@bp.route("/<event_id>")
class EventsById(views.MethodView):
    @bp.response(200, EventResponseSchema)
    @jwt_required()
    def get(self, event_id):
        """Get event by ID"""
        event_service = injector.get(EventService)
        event = event_service.get_by_id(event_id=event_id, team_id=current_user.slack_organization_id)
        if event is None:
            abort(404, message="Event not found.")
        return event

    @bp.arguments(EventUpdateSchema)
    @bp.response(200, EventResponseSchema)
    @jwt_required()
    def patch(self, update_data, event_id):
        """Update event by ID"""
        event_service = injector.get(EventService)
        updated_event = event_service.update(event_id=event_id, data=update_data, team_id=current_user.slack_organization_id)
        if updated_event is None:
            abort(404, message="Event not found.")
        return updated_event

    @bp.response(204)
    @jwt_required()
    def delete(self, event_id):
        """Delete event"""
        event_service = injector.get(EventService)
        success = event_service.delete(event_id=event_id, team_id=current_user.slack_organization_id)
        if not success:
            abort(400, message="Something went wrong.")
