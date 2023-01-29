from marshmallow import fields, Schema

class CreateInvitationsRequestSchema(Schema):
    user_ids = fields.List(fields.Str(), required=True)
    event_id = fields.UUID(required=True)

class CreateInvitationsResponseSchema(Schema):
    success = fields.Boolean(required=True)
