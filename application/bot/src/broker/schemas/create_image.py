from marshmallow import fields, Schema

class CreateImageRequestSchema(Schema):
    cloudinary_id = fields.Str(required=True)
    slack_id = fields.Str(required=True)
    team_id = fields.Str(required=True)
    title = fields.Str(required=True)

class CreateImageResponseSchema(Schema):
    success = fields.Boolean(required=True)
