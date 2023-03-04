from marshmallow import fields, Schema

class DeletedSlackOrganizationEventSchema(Schema):
    team_id = fields.Str(required=True)
    enterprise_id = fields.Str()
