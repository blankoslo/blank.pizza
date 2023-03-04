from app.models.slack_organization import SlackOrganization
from app.models.mixins import CrudMixin


class SlackOrganizationRepository(SlackOrganization, CrudMixin):
    pass
