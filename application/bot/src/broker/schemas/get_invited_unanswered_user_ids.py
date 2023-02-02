from marshmallow import fields, Schema

class GetInvitedUnansweredUserIdsResponseSchema(Schema):
    user_ids = fields.List(fields.Str(), many=True, required=True)
