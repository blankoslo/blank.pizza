from marshmallow import fields, Schema

class UserWithdrewAfterFinalizationEventSchema(Schema):
    event_id = fields.UUID(required=True)
    timestamp = fields.DateTime(required=True)
    restaurant_name = fields.Str(required=True)
    slack_id = fields.Str(required=True)
    team_id = fields.Str(required=True)
    bot_token = fields.Str(required=True)
    channel_id = fields.Str(required=True)
