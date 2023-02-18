from marshmallow import fields, Schema

class SlackMessage(Schema):
    ts = fields.Str(required=True)
    channel_id = fields.Str(required=True)
