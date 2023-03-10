from marshmallow import fields, Schema

class FinalizationEventEventSchema(Schema):
    is_finalized = fields.Boolean(required=True)
    event_id = fields.UUID(required=True)
    timestamp = fields.DateTime(required=True)
    restaurant_name = fields.Str(required=True)
    slack_ids = fields.List(fields.Str(), required=True)
    team_id = fields.Str(required=True)
    bot_token = fields.Str(required=True)
    channel_id = fields.Str(required=True)
