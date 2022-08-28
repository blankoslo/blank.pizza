from flask import views
from flask_smorest import Blueprint, abort
from app.models.event import Event, EventSchema, EventQueryArgsSchema
from flask_jwt_extended import jwt_required

bp = Blueprint("events", "events", url_prefix="/events", description="Operations on events")

@bp.route("/")
class Events(views.MethodView):
    @bp.arguments(EventQueryArgsSchema, location="query")
    @bp.response(200, EventSchema(many=True))
    @bp.paginate()
    def get(self, args, pagination_parameters):
        """List events"""
        total, events = Event.get(filters = args, page = pagination_parameters.page, per_page = pagination_parameters.page_size)
        pagination_parameters.item_count = total
        return events

    @bp.arguments(EventSchema)
    @bp.response(201, EventSchema)
    @jwt_required()
    def post(self, new_data):
        """Add an event"""
        Event.upsert(new_data)
        return new_data

@bp.route("/<event_id>")
class EventsById(views.MethodView):
    @bp.response(200, EventSchema)
    def get(self, event_id):
        """Get event by ID"""
        event = Event.get_by_id(event_id)
        if event == None:
            abort(404, message = "Event not found.")
        return event

    @bp.response(204)
    @jwt_required()
    def delete(self, event_id):
        """Delete event"""
        Event.delete(event_id)