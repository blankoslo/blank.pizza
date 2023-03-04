from app.repositories.slack_organization_repository import SlackOrganizationRepository


class SlackOrganizationService:
    def get(self, filters=None, page=None, per_page=None):
        return SlackOrganizationRepository.get(filters=filters, page=page, per_page=per_page)

    def get_by_id(self, team_id):
        return SlackOrganizationRepository.get_by_id(id=team_id)

    def delete(self, team_id, enterprise_id=None):
        return SlackOrganizationRepository.delete(id=team_id)

    def upsert(self, schema):
        return SlackOrganizationRepository.upsert(schema=schema)
