from marshmallow import fields, Schema

class InviteMultipleIfNeededResponseDataSchema(Schema):
    event_time = fields.DateTime(required=True)
    event_id = fields.UUID(required=True)
    restaurant_name = fields.Str(required=True)
    invited_users = fields.List(fields.Str(), required=True)
    team_id = fields.Str(required=True)
    bot_token = fields.Str(required=True)

class InviteMultipleIfNeededResponseSchema(Schema):
    events = fields.List(fields.Nested(InviteMultipleIfNeededResponseDataSchema), required=True)
