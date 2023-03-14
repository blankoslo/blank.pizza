from app.models.group_schema import GroupSchema
from app.models.slack_user import SlackUser
from app.models.slack_user_schema import SlackUserSchema
from app.repositories.group_repository import GroupRepository

class GroupService:
    def get(self, page, per_page, team_id, filters=None):
        return GroupRepository.get(filters=filters, page=page, per_page=per_page, team_id=team_id)

    def get_by_id(self, group_id, team_id=None):
        group = GroupRepository.get_by_id(group_id)
        if group is None or (team_id is not None and group.slack_organization_id != team_id):
            return None
        return group

    def add(self, data, team_id):
        slack_users = []
        for slack_user in SlackUser.query.filter(SlackUser.slack_id.in_(data['members'])).filter(SlackUser.slack_organization_id == team_id).all():
            dumped_slack_user = SlackUserSchema(exclude=['slack_organization']).dump(slack_user)
            slack_users.append(dumped_slack_user)
        data = {
            'name': data["name"],
            'members': slack_users,
            'slack_organization_id': team_id,
        }
        group = GroupSchema().load(data=data, partial=True)
        return GroupRepository.upsert(group)

    def update(self, group_id, data, team_id):
        group = GroupRepository.get_by_id(group_id)

        if group is None or group.slack_organization_id != team_id:
            return None

        slack_users = []
        for slack_user in SlackUser.query.filter(SlackUser.slack_id.in_(data['members'])).filter(SlackUser.slack_organization_id == team_id).all():
            dumped_slack_user = SlackUserSchema(exclude=['slack_organization']).dump(slack_user)
            slack_users.append(dumped_slack_user)
        data = {
            'name': data["name"],
            'members': slack_users,
        }
        updated_group = GroupSchema().load(data=data, instance=group, partial=True)
        return GroupRepository.upsert(updated_group)

    def delete(self, group_id, team_id):
        group = GroupRepository.get_by_id(group_id)

        if group is not None and group.slack_organization_id == team_id:
            GroupRepository.delete(group_id)
            return True
        return False
