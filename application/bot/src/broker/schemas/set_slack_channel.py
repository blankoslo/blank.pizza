from marshmallow import fields, Schema


class SetSlackChannelRequestSchema(Schema):
    channel_id = fields.Str(required=True)
    team_id = fields.Str(required=True)


class SetSlackChannelResponseSchema(Schema):
    success = fields.Boolean(required=True)
    old_channel_id = fields.Str()
