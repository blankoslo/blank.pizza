from marshmallow import fields, Schema

class GetUsersToInviteRequestSchema(Schema):
    number_of_users_to_invite = fields.Int(required=True)
    event_id = fields.UUID(required=True)
    total_number_of_employees = fields.Int(required=True)
    employees_per_event = fields.Int(required=True)

class GetUsersToInviteResponseDataSchema(Schema):
    id = fields.Str(required=True)

class GetUsersToInviteResponseSchema(Schema):
    users = fields.Nested(GetUsersToInviteResponseDataSchema, many=True)
