from marshmallow_jsonschema import JSONSchema
from marshmallow import fields, Schema

class MessageSchema(Schema):
    type = fields.Str(required=True)
    payload = fields.Raw(allow_none=True)

message_schema = JSONSchema().dump(MessageSchema())
