from marshmallow import fields, Schema

class GetUsersResponseDataSchema(Schema):
    id = fields.Str(required=True)
    email = fields.Str(required=True)
    name = fields.Str(required=True)
    picture = fields.Str(required=True)

class GetUsersResponseSchema(Schema):
    users = fields.Nested(GetUsersResponseDataSchema, many=True)
