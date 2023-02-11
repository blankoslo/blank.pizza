from marshmallow import fields, Schema

class SlackUserUpdate(Schema):
    slack_id = fields.Str(required=True)
    current_username = fields.Str()
    email = fields.Str()

class UpdateSlackUserRequestSchema(Schema):
    users_to_update = fields.Nested(SlackUserUpdate, required=True, many=True)

class UpdateSlackUserResponseSchema(Schema):
    success = fields.Boolean(required=True)
    updated_users = fields.List(fields.Str(), required=True)
    failed_users = fields.List(fields.Str(), required=True)
