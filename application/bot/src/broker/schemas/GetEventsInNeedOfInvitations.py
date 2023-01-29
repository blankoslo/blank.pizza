from marshmallow import fields, Schema

class GetEventsInNeedOfInvitationsSchema(Schema):
    days_in_advance_to_invite = fields.Int(required=True)
    people_per_event = fields.Int(required=True)

class GetEventsInNeedOfInvitationsResponseDataSchema(Schema):
    event_id = fields.UUID(required=True)
    event_time = fields.DateTime(required=True)
    restaurant_name = fields.Str(required=True)
    number_of_already_invited = fields.Int(required=True)

class GetEventsInNeedOfInvitationsResponseSchema(Schema):
    events = fields.Nested(GetEventsInNeedOfInvitationsResponseDataSchema, many=True)
