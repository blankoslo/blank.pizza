from marshmallow import fields, Schema

class MessageRequestSchema(Schema):
    type = fields.Str(required=True)
    payload = fields.Raw(allow_none=True)
