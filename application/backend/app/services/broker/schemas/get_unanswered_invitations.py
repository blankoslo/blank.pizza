from marshmallow import fields, Schema

class GetUnansweredInvitationsDataSchema(Schema):
    slack_id = fields.Str(required=True)
    event_id = fields.UUID(required=True)
    invited_at = fields.DateTime(required=True)
    reminded_at = fields.DateTime(required=True)

class GetUnansweredInvitationsResponseSchema(Schema):
    invitations = fields.Nested(GetUnansweredInvitationsDataSchema, many=True)
