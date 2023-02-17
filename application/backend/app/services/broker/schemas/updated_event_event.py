from marshmallow import fields, Schema

class UpdatedEventEventSchema(Schema):
    is_finalized = fields.Boolean(required=True)
    event_id = fields.UUID(required=True)
    old_timestamp = fields.DateTime(required=True)
    timestamp = fields.DateTime(required=True)
    old_restaurant_name = fields.Str(required=True)
    restaurant_name = fields.Str(required=True)
    slack_ids = fields.List(fields.Str(), required=True)
