from marshmallow import fields, Schema

class FinalizeEventIfPossibleRequestSchema(Schema):
    people_per_event = fields.Int(required=True)

class FinalizeEventIfPossibleResponseDataSchema(Schema):
    event_id = fields.UUID(required=True)
    timestamp = fields.DateTime(required=True)
    restaurant_name = fields.Str(required=True)
    slack_ids = fields.List(fields.Str(), required=True)

class FinalizeEventIfPossibleResponseSchema(Schema):
    success = fields.Boolean(required=True)
    data = fields.Nested(FinalizeEventIfPossibleResponseDataSchema)
