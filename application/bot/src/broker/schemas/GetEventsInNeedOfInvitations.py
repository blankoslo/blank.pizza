from marshmallow import fields, Schema

class GetEventsInNeedOfInvitationsSchema(Schema):
    days_in_advance_to_invite = fields.Int(required=True)
    people_per_event = fields.Int(required=True)
