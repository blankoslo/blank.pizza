from marshmallow import fields, Schema

class WithdrawInvitationRequestSchema(Schema):
    slack_id = fields.Str(required=True)
    event_id = fields.UUID(required=True)

class WithdrawInvitationResponseSchema(Schema):
    success = fields.Boolean(required=True)
