from marshmallow import fields, Schema

class SlackUserUpdate(Schema):
    current_username = fields.Str()
    email = fields.Str()

class UpdateSlackUserRequestSchema(Schema):
    slack_id = fields.Str(required=True)
    update_data = fields.Nested(SlackUserUpdate, required=True)

class UpdateSlackUserResponseSchema(Schema):
    success = fields.Boolean(required=True)
