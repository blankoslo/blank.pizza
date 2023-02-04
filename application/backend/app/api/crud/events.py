from flask import views
from flask_smorest import Blueprint, abort
from app.models.event_schema import EventSchema, EventQueryArgsSchema
from flask_jwt_extended import jwt_required
from app.services.injector import injector
from app.services.event_service import EventService

bp = Blueprint("events", "events", url_prefix="/events", description="Operations on events")

@bp.route("/")
class Events(views.MethodView):
    @bp.arguments(EventQueryArgsSchema, location="query")
    @bp.response(200, EventSchema(many=True))
    @bp.paginate()
    def get(self, args, pagination_parameters):
        """List events"""
        event_service = injector.get(EventService)
        total, events = event_service.get(args, pagination_parameters.page, pagination_parameters.page_size)
        pagination_parameters.item_count = total
        return events

    @bp.arguments(EventSchema)
    @bp.response(201, EventSchema)
    @jwt_required()
    def post(self, new_data):
        """Add an event"""
        event_service = injector.get(EventService)
        new_event = event_service.add(new_data)
        return new_event

@bp.route("/<event_id>")
class EventsById(views.MethodView):
    @bp.response(200, EventSchema)
    def get(self, event_id):
        """Get event by ID"""
        event_service = injector.get(EventService)
        event = event_service.get_by_id(event_id)
        if event is None:
            abort(404, message = "Event not found.")
        return event

    @bp.response(204)
    @jwt_required()
    def delete(self, event_id):
        """Delete event"""
        event_service = injector.get(EventService)
        event_service.delete(event_id)
