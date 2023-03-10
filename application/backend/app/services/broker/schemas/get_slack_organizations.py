from marshmallow import fields, Schema

class GetSlackOrganizationsResponseDataSchema(Schema):
    team_id = fields.Str(required=True)
    bot_token = fields.Str(required=True)

class GetSlackOrganizationsResponseSchema(Schema):
    organizations = fields.List(fields.Nested(GetSlackOrganizationsResponseDataSchema), required=True)
