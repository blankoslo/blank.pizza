from marshmallow import fields, Schema

class MessageSchema(Schema):
    type = fields.Str(required=True)
    payload = fields.Raw(allow_none=True, required=False)
